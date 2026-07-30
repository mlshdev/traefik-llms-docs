"""Turn MkDocs-flavoured Markdown into plain Markdown an LLM reads correctly.

Ordering matters. Passes run as:

1. include resolution (``{% include-markdown %}``, ``--8<--``) -- these are MkDocs
   *preprocessors*, so like MkDocs we substitute them everywhere, fences included.
2. fence-tab conversion -- rewrites fence info strings, so it owns the fences.
3. ``=== "Tab"`` blocks, admonitions, ``{: .attr }`` lines, link rewriting -- all of
   these are fence-aware and must never touch a code fence's interior. That matters
   here: the Traefik docs embed 754 fenced examples containing Go templates (``{{ }}``)
   and shell text that would otherwise be mangled.
"""

from __future__ import annotations

import posixpath
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

import yaml

from traefik_llms_docs.models import Admonition, Upstream

if TYPE_CHECKING:
    from pathlib import Path

_FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)
_INCLUDE_MARKDOWN = re.compile(r"^[ \t]*\{%\s*include-markdown\s+\"([^\"]+)\"\s*%\}[ \t]*$", re.M)
_SNIPPET = re.compile(r"^[ \t]*--8<--\s+\"([^\"]+)\"[ \t]*$", re.M)
_FENCE_LINE = re.compile(r"^(?P<indent>[ \t]*)(?P<marker>`{3,}|~{3,})(?P<info>.*)$")
_TAB_ATTR = re.compile(r"""\btab=(["'])(?P<label>.*?)\1""")
_TABBED = re.compile(r"^(?P<indent>[ \t]*)===\+?\s+(?P<quote>[\"'])(?P<label>.*?)(?P=quote)\s*$")
# Upstream is inconsistent: the space after the marker is sometimes missing
# (`!!!info "Kubernetes"`) and titles are sometimes unquoted
# (`!!! note Referencing a certificate resolver`), so both are tolerated.
_ADMONITION = re.compile(
    r"^(?P<indent>[ \t]*)(?P<marker>!!!|\?\?\?\+?)[ \t]*(?P<kind>[\w-]+)"
    r"(?:[ \t]+(?:(?P<quote>[\"'])(?P<title>.*?)(?P=quote)|(?P<bare>\S.*?)))?[ \t]*$"
)
_ATTR_LINE = re.compile(r"^[ \t]*\{:[^}]*\}[ \t]*$")
_MD_LINK = re.compile(r"(!?)\[([^\]]*)\]\(([^)\s]+)(\s+\"[^\"]*\")?\)")
_HTML_SRC = re.compile(r"""(<img\b[^>]*?\bsrc=)(["'])([^"']+)\2""")

MAX_INCLUDE_DEPTH = 10


@dataclass(frozen=True, slots=True)
class Frontmatter:
    title: str
    description: str


@dataclass(frozen=True, slots=True)
class Fence:
    """A fenced code block located within a document."""

    start: int
    """Index of the opening fence line."""
    end: int
    """Index of the closing fence line, or the last line if unterminated."""
    indent: str
    marker: str
    info: str


def split_frontmatter(text: str) -> tuple[Frontmatter, str]:
    """Split YAML frontmatter from the body.

    22 of the 171 upstream pages have no frontmatter, so the title falls back to
    the first ``# `` heading and the description to empty.
    """
    match = _FRONTMATTER.match(text)
    meta: dict[str, object] = {}
    body = text
    if match:
        loaded = yaml.safe_load(match.group(1))
        if isinstance(loaded, dict):
            meta = loaded
        body = text[match.end() :]

    title = str(meta.get("title", "")).strip()
    if not title:
        for line in body.splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break
    return Frontmatter(title=title, description=str(meta.get("description", "")).strip()), body


def strip_frontmatter(text: str) -> str:
    return split_frontmatter(text)[1]


# --------------------------------------------------------------------------- #
# Fence scanning
# --------------------------------------------------------------------------- #


def fence_spans(lines: list[str]) -> list[Fence]:
    """Locate every fenced code block.

    A fence closes on a line using the same marker character, at least as long,
    and carrying no info string. Tracking spans explicitly (rather than inferring
    openers from a boolean mask) keeps back-to-back fences with no blank line
    between them from being misread as one block.
    """
    fences: list[Fence] = []
    i = 0
    while i < len(lines):
        match = _FENCE_LINE.match(lines[i])
        if match is None:
            i += 1
            continue
        indent, marker, info = match.group("indent", "marker", "info")
        j = i + 1
        while j < len(lines):
            closer = _FENCE_LINE.match(lines[j])
            if (
                closer is not None
                and not closer.group("info").strip()
                and closer.group("marker")[0] == marker[0]
                and len(closer.group("marker")) >= len(marker)
            ):
                break
            j += 1
        end = min(j, len(lines) - 1)
        fences.append(Fence(start=i, end=end, indent=indent, marker=marker, info=info))
        i = end + 1
    return fences


def fence_mask(lines: list[str]) -> list[bool]:
    """Per-line mask: ``True`` where a line belongs to a fence, delimiters included."""
    mask = [False] * len(lines)
    for fence in fence_spans(lines):
        for i in range(fence.start, fence.end + 1):
            mask[i] = True
    return mask


# --------------------------------------------------------------------------- #
# Pass 1: includes
# --------------------------------------------------------------------------- #


def resolve_includes(
    text: str,
    *,
    source: Path,
    content_dir: Path,
    docs_dir: Path,
    _depth: int = 0,
    _seen: frozenset[Path] = frozenset(),
) -> str:
    """Recursively expand ``include-markdown`` and ``--8<--`` snippet directives.

    Include paths are tried against the including file's directory, then
    ``content/``, then ``docs/``; upstream's three real targets all live under
    ``content/``. Cycles are broken by tracking the resolved-path chain.
    """
    if _depth > MAX_INCLUDE_DEPTH:
        msg = f"include depth exceeded at {source}"
        raise RecursionError(msg)

    def expand(target: str, bases: tuple[Path, ...]) -> str:
        resolved = next((c for b in bases if (c := b / target).is_file()), None)
        if resolved is None:
            msg = f"{source}: cannot resolve include {target!r}"
            raise FileNotFoundError(msg)
        resolved = resolved.resolve()
        if resolved in _seen:
            msg = f"circular include: {resolved}"
            raise RecursionError(msg)
        nested = strip_frontmatter(resolved.read_text(encoding="utf-8"))
        return resolve_includes(
            nested,
            source=resolved,
            content_dir=content_dir,
            docs_dir=docs_dir,
            _depth=_depth + 1,
            _seen=_seen | {resolved},
        ).strip("\n")

    text = _INCLUDE_MARKDOWN.sub(
        lambda m: expand(m.group(1), (source.parent, content_dir, docs_dir)), text
    )
    return _SNIPPET.sub(lambda m: expand(m.group(1), (docs_dir, content_dir, source.parent)), text)


# --------------------------------------------------------------------------- #
# Pass 2: fence tabs
# --------------------------------------------------------------------------- #


def convert_fence_tabs(text: str) -> str:
    """Convert `````yaml tab="File (YAML)"`` into a labelled plain fence.

    This is the highest-impact pass: 754 such blocks across 116 upstream pages.
    The label becomes a bold line above the fence and the language tag is kept, so
    the result stays valid Markdown with syntax information intact::

        **File (YAML)**

        ```yaml
        metrics:
          otlp: {}
        ```
    """
    lines = text.splitlines()
    rewrites: dict[int, tuple[str, str]] = {}
    for fence in fence_spans(lines):
        tab = _TAB_ATTR.search(fence.info)
        if tab is None:
            continue
        language = _TAB_ATTR.sub("", fence.info).strip()
        rewrites[fence.start] = (
            f"{fence.indent}**{tab.group('label')}**",
            f"{fence.indent}{fence.marker}{language}",
        )

    out: list[str] = []
    for i, line in enumerate(lines):
        rewrite = rewrites.get(i)
        if rewrite is None:
            out.append(line)
            continue
        label_line, fence_line = rewrite
        if out and out[-1].strip():
            out.append("")
        out.extend((label_line, "", fence_line))
    return "\n".join(out)


# --------------------------------------------------------------------------- #
# Pass 3: indented blocks (tabbed sets and admonitions)
# --------------------------------------------------------------------------- #


def _dedent_body(lines: list[str], start: int, base_indent: int) -> tuple[list[str], int]:
    """Collect the indented body of a block starting at *start*.

    Returns the de-indented body and the index of the first line after it.
    """
    body: list[str] = []
    i = start
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            body.append("")
            i += 1
            continue
        indent = len(line) - len(line.lstrip())
        if indent <= base_indent:
            break
        body.append(line[base_indent + 4 :] if indent >= base_indent + 4 else line.lstrip())
        i += 1
    while body and not body[0]:
        body.pop(0)
    while body and not body[-1]:
        body.pop()
    return body, i


def _admonition_heading(match: re.Match[str]) -> str:
    """Render the bold heading line for an admonition.

    An unquoted remainder after an *unrecognised* kind means the whole thing is a
    title with no type at all -- upstream's ``!!! Failover on Heathcheck Status``
    is a title, not a "failover" admonition -- so it degrades to a plain Note.
    """
    kind = match.group("kind")
    title = match.group("title")
    bare = match.group("bare")
    if title is None and bare:
        if kind.upper() in Admonition.__members__:
            title = bare
        else:
            title = f"{kind} {bare}".strip()
            kind = Admonition.NOTE.name
    label = Admonition.label_for(kind)
    return f"**{label} — {title}**" if title else f"**{label}**"


def convert_blocks(text: str) -> str:
    """Convert ``=== "Tab"`` sets and ``!!!``/``???`` admonitions, recursively.

    Admonitions become blockquotes -- unambiguous to a reader, and unable to
    collide with the heading hierarchy the way a promoted ``####`` would::

        > **Info — Default protocol**
        >
        > The OpenTelemetry exporter will export metrics to the collector.
    """
    lines = text.splitlines()
    mask = fence_mask(lines)
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        tabbed = None if mask[i] else _TABBED.match(line)
        admonition = None if mask[i] else _ADMONITION.match(line)
        block = tabbed if tabbed is not None else admonition
        if block is None:
            out.append(line)
            i += 1
            continue

        indent = block.group("indent")
        body_lines, next_i = _dedent_body(lines, i + 1, len(indent))
        body = convert_blocks("\n".join(body_lines))

        if out and out[-1].strip():
            out.append("")
        if tabbed is not None:
            out.append(f"{indent}**{tabbed.group('label')}**")
            out.append("")
            out.extend(f"{indent}{b}" if b else "" for b in body.splitlines())
        elif admonition is not None:
            out.append(f"{indent}> {_admonition_heading(admonition)}")
            if body:
                out.append(f"{indent}>")
                out.extend(f"{indent}> {b}".rstrip() for b in body.splitlines())
        out.append("")
        i = next_i
    return "\n".join(out)


# --------------------------------------------------------------------------- #
# Pass 4: attribute lists
# --------------------------------------------------------------------------- #


def strip_attr_lists(text: str) -> str:
    """Drop standalone ``{: .subtitle }`` styling lines (attr_list extension)."""
    lines = text.splitlines()
    mask = fence_mask(lines)
    return "\n".join(line for i, line in enumerate(lines) if mask[i] or not _ATTR_LINE.match(line))


# --------------------------------------------------------------------------- #
# Pass 5: links
# --------------------------------------------------------------------------- #


def rewrite_links(text: str, *, page_path: str, upstream: Upstream) -> str:
    """Fix up relative links so they still resolve from the generated tree.

    Three cases, decided against the real upstream tree rather than by guessing
    from the extension:

    * **Assets** (images and other non-Markdown files) are not copied into this
      repo, so they become absolute raw URLs pinned to the build's commit.
    * **Extension-less page links** are MkDocs "pretty URLs" pointing at another
      page. They gain the ``.md`` suffix so they resolve in the ``pages/`` tree.
    * **Plain ``.md`` links** are already correct, because ``pages/`` mirrors the
      upstream layout exactly.
    """
    page_dir = posixpath.dirname(page_path)
    content = upstream.content_dir
    # With MkDocs' default use_directory_urls, a page renders at <path-without-.md>/,
    # so a link the author wrote against the rendered URL sits one level deeper than
    # the source file. Both bases are tried, file-relative first.
    url_dir = page_dir if posixpath.basename(page_path) == "index.md" else page_path[: -len(".md")]

    def absolutise(target: str) -> str | None:
        if not target or target.startswith(("http://", "https://", "#", "mailto:", "//")):
            return None
        anchor = ""
        if "#" in target:
            target, _, anchor_part = target.partition("#")
            anchor = f"#{anchor_part}"
        if not target or target.endswith(".md"):
            return None
        for base in (page_dir, url_dir):
            resolved = posixpath.normpath(posixpath.join(base, target))
            if resolved.startswith(".."):
                continue
            if (content / resolved).is_file():
                return upstream.raw_url(resolved) + anchor
            # A pretty URL for a page: restore the suffix and keep the link relative.
            for candidate in (f"{resolved}.md", f"{resolved}/index.md"):
                if (content / candidate).is_file():
                    relative = posixpath.relpath(candidate, page_dir or ".")
                    return relative + anchor
        return None

    def sub_md(match: re.Match[str]) -> str:
        bang, label, target, title = match.groups()
        new = absolutise(target)
        return match.group(0) if new is None else f"{bang}[{label}]({new}{title or ''})"

    def sub_html(match: re.Match[str]) -> str:
        prefix, quote, target = match.groups()
        new = absolutise(target)
        return match.group(0) if new is None else f"{prefix}{quote}{new}{quote}"

    lines = text.splitlines()
    mask = fence_mask(lines)
    return "\n".join(
        line if mask[i] else _HTML_SRC.sub(sub_html, _MD_LINK.sub(sub_md, line))
        for i, line in enumerate(lines)
    )


# --------------------------------------------------------------------------- #
# Pipeline
# --------------------------------------------------------------------------- #


def normalise_blank_lines(text: str) -> str:
    """Collapse runs of 3+ blank lines and normalise the trailing newline."""
    return re.sub(r"\n{3,}", "\n\n", text).strip("\n") + "\n"


def transform(raw: str, *, page_path: str, upstream: Upstream) -> tuple[Frontmatter, str]:
    """Run the full pipeline for one page."""
    source = upstream.content_dir / page_path
    expanded = resolve_includes(
        raw,
        source=source,
        content_dir=upstream.content_dir,
        docs_dir=upstream.docs_dir,
    )
    meta, body = split_frontmatter(expanded)
    body = convert_fence_tabs(body)
    # Before convert_blocks: an attr_list line inside an admonition body would
    # otherwise come out prefixed with "> " and no longer match as standalone.
    body = strip_attr_lists(body)
    body = convert_blocks(body)
    body = rewrite_links(body, page_path=page_path, upstream=upstream)
    return meta, normalise_blank_lines(body)

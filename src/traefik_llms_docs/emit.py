"""Build one documentation version and write the generated tree.

Output layout::

    llms.txt                      root pointer index (all tracked versions)
    traefik/<label>/llms.txt      nav-ordered index, one link per page
    traefik/<label>/llms-full.txt whole corpus in one file
    traefik/<label>/SOURCE        provenance: upstream repo, branch, commit, build time
    traefik/<label>/pages/**.md   cleaned pages, mirroring upstream paths
"""

from __future__ import annotations

import warnings
from pathlib import Path

from traefik_llms_docs import __version__
from traefik_llms_docs.config import (
    OPTIONAL_SECTIONS,
    PARTIAL_GLOBS,
    TRACKED,
    UPSTREAM_SLUG,
    raw_url_for,
)
from traefik_llms_docs.models import BuildResult, NavEntry, Page, Upstream
from traefik_llms_docs.nav import load_nav, site_description
from traefik_llms_docs.transform import transform


def is_partial(path: str) -> bool:
    """True for include-only source files that must not be emitted standalone."""
    return any(Path(path).match(glob) for glob in PARTIAL_GLOBS)


def orphan_pages(upstream: Upstream, covered: set[str]) -> list[str]:
    """Non-partial source pages absent from the nav *and* carrying real content.

    Upstream currently has two such files (``cli-ref.md``, ``env-ref.md``) but both
    are empty stubs, so nothing is lost by following the nav. If upstream ever adds
    a real page without wiring it into the nav, we want to hear about it rather than
    silently drop it.
    """
    orphans: list[str] = []
    for path in sorted(upstream.content_dir.rglob("*.md")):
        rel = path.relative_to(upstream.content_dir).as_posix()
        if rel in covered or is_partial(rel):
            continue
        if path.read_text(encoding="utf-8").strip():
            orphans.append(rel)
    return orphans


def build_pages(upstream: Upstream) -> list[Page]:
    """Transform every nav-listed page."""
    pages: list[Page] = []
    for entry in load_nav(upstream.mkdocs_yml):
        if is_partial(entry.path):
            continue
        source = upstream.content_dir / entry.path
        if not source.is_file():
            msg = f"nav references missing page: {entry.path}"
            raise FileNotFoundError(msg)
        meta, body = transform(
            source.read_text(encoding="utf-8"), page_path=entry.path, upstream=upstream
        )
        pages.append(
            Page(
                nav=entry,
                title=meta.title or entry.title,
                description=meta.description,
                body=body,
            )
        )

    orphans = orphan_pages(upstream, {p.nav.path for p in pages})
    if orphans:
        warnings.warn(
            "upstream pages have content but are absent from mkdocs nav and will not "
            f"be emitted: {', '.join(orphans)}",
            stacklevel=2,
        )
    return pages


def _yaml_scalar(value: str) -> str:
    """Quote a scalar for the generated frontmatter."""
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def render_page(page: Page, upstream: Upstream) -> str:
    """A page with provenance frontmatter, ready for retrieval or direct reading."""
    entry: NavEntry = page.nav
    lines = [
        "---",
        f"title: {_yaml_scalar(page.title)}",
    ]
    if page.description:
        lines.append(f"description: {_yaml_scalar(page.description)}")
    lines += [
        f"section: {_yaml_scalar(entry.section)}",
        f"breadcrumb: {_yaml_scalar(entry.breadcrumb)}",
        f"traefik_version: {_yaml_scalar(upstream.spec.label)}",
        f"upstream_path: {_yaml_scalar('docs/content/' + entry.path)}",
        f"source_url: {_yaml_scalar(upstream.blob_url(entry.path))}",
        "---",
        "",
        page.body,
    ]
    return "\n".join(lines)


def render_llms_txt(pages: list[Page], upstream: Upstream, summary: str) -> str:
    """The llmstxt.org index: H1, blockquote summary, then link sections."""
    label = upstream.spec.label
    out = [
        f"# Traefik Proxy {label}",
        "",
        f"> {summary}",
        "",
        f"Generated from [{UPSTREAM_SLUG}](https://github.com/{UPSTREAM_SLUG}) "
        f"branch `{upstream.spec.branch}` at commit "
        f"[`{upstream.commit[:12]}`]"
        f"(https://github.com/{UPSTREAM_SLUG}/tree/{upstream.commit}/docs). "
        "MkDocs-specific syntax (tabbed code fences, admonitions, includes) has been "
        "converted to plain Markdown.",
        "",
    ]

    def section_block(items: list[Page]) -> list[str]:
        block: list[str] = []
        for page in items:
            url = raw_url_for(label, page.nav.path)
            note = f": {page.description}" if page.description else ""
            block.append(f"- [{page.nav.breadcrumb}]({url}){note}")
        return block

    ordered_sections: list[str] = []
    grouped: dict[str, list[Page]] = {}
    for page in pages:
        grouped.setdefault(page.nav.section, []).append(page)
        if page.nav.section not in ordered_sections:
            ordered_sections.append(page.nav.section)

    for section in ordered_sections:
        if section in OPTIONAL_SECTIONS:
            continue
        out += [f"## {section}", "", *section_block(grouped[section]), ""]

    optional = [s for s in ordered_sections if s in OPTIONAL_SECTIONS]
    if optional:
        out += ["## Optional", ""]
        for section in optional:
            out += section_block(grouped[section])
        out.append("")
    return "\n".join(out)


def render_llms_full(pages: list[Page], upstream: Upstream, summary: str) -> str:
    """Whole corpus in one file, nav-ordered, with per-page provenance headers."""
    label = upstream.spec.label
    out = [
        f"# Traefik Proxy {label} — Complete Documentation",
        "",
        f"> {summary}",
        "",
        f"Source: {UPSTREAM_SLUG}@{upstream.commit} (branch {upstream.spec.branch}), "
        f"docs/content. {len(pages)} pages.",
        "",
    ]
    for page in pages:
        out += [
            "---",
            "",
            f"# {page.nav.breadcrumb}",
            "",
            f"*Source: {upstream.blob_url(page.nav.path)}*",
            "",
            page.body.rstrip("\n"),
            "",
        ]
    return "\n".join(out) + "\n"


def render_source(upstream: Upstream, page_count: int) -> str:
    """Provenance for one version.

    Deliberately carries no build timestamp: the output is then a pure function of
    the upstream commit and the generator version, so a rebuild that finds nothing
    new produces a byte-identical tree and the automation commits nothing. When the
    build happened is already recorded by the commit date.
    """
    return (
        f"upstream_repo: https://github.com/{UPSTREAM_SLUG}\n"
        f"upstream_branch: {upstream.spec.branch}\n"
        f"upstream_commit: {upstream.commit}\n"
        f"upstream_tree: https://github.com/{UPSTREAM_SLUG}/tree/{upstream.commit}/docs\n"
        f"traefik_version: {upstream.spec.label}\n"
        f"pages: {page_count}\n"
        f"generator: traefik-llms-docs {__version__}\n"
    )


def render_root_index(results: list[BuildResult]) -> str:
    """Root llms.txt: a small pointer index, not a copy of the corpus."""
    latest = results[0]
    out = [
        "# Traefik Proxy Documentation (LLM-friendly)",
        "",
        "> The Traefik Proxy documentation converted from MkDocs Markdown into plain "
        "Markdown for LLM consumption. Traefik is an open-source application proxy that "
        "auto-discovers services and handles routing, TLS, middlewares and observability.",
        "",
        "Upstream publishes no llms.txt; this repository generates one and keeps it in "
        "sync automatically. Each version below has a nav-ordered index, a single-file "
        "corpus, and one cleaned Markdown file per page.",
        "",
        "## Documentation",
        "",
    ]
    for result in results:
        label = result.upstream.spec.label
        base = f"https://raw.githubusercontent.com/mlshdev/traefik-llms-docs/main/traefik/{label}"
        latest_note = " (latest stable)" if result is latest else ""
        out += [
            f"- [Traefik {label} — index]({base}/llms.txt): nav-ordered list of all "
            f"{len(result.pages)} pages with descriptions{latest_note}.",
            f"- [Traefik {label} — full corpus]({base}/llms-full.txt): every page "
            "concatenated into one file.",
            f"- [Traefik {label} — provenance]({base}/SOURCE): upstream commit this "
            "build was generated from.",
        ]
    out.append("")
    return "\n".join(out)


def build_version(upstream: Upstream, out_root: Path) -> BuildResult:
    """Build one version and write it under *out_root*."""
    pages = build_pages(upstream)
    summary = site_description(upstream.mkdocs_yml) or "Traefik Proxy documentation."
    version_dir = out_root / upstream.spec.output_dir
    pages_dir = version_dir / "pages"
    written: list[Path] = []

    for page in pages:
        target = pages_dir / page.out_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_page(page, upstream), encoding="utf-8")
        written.append(target)

    for name, content in (
        ("llms.txt", render_llms_txt(pages, upstream, summary)),
        ("llms-full.txt", render_llms_full(pages, upstream, summary)),
        ("SOURCE", render_source(upstream, len(pages))),
    ):
        target = version_dir / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        written.append(target)

    return BuildResult(upstream=upstream, pages=tuple(pages), written=tuple(written))


def prune_stale(out_root: Path, results: list[BuildResult]) -> list[Path]:
    """Delete generated files that this build no longer produces.

    Without this, a page renamed or dropped upstream would linger forever and the
    committed tree would drift from the source it claims to mirror.
    """
    kept = {p.resolve() for result in results for p in result.written}
    removed: list[Path] = []
    for spec in TRACKED:
        version_dir = out_root / spec.output_dir
        if not version_dir.is_dir():
            continue
        for path in sorted(version_dir.rglob("*")):
            if path.is_file() and path.resolve() not in kept:
                path.unlink()
                removed.append(path)
    for spec in TRACKED:
        version_dir = out_root / spec.output_dir
        if not version_dir.is_dir():
            continue
        for path in sorted(version_dir.rglob("*"), reverse=True):
            if path.is_dir() and not any(path.iterdir()):
                path.rmdir()
    return removed

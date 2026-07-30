"""Unit tests for the MkDocs-to-plain-Markdown passes."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from traefik_llms_docs.models import Upstream
from traefik_llms_docs.transform import (
    convert_blocks,
    convert_fence_tabs,
    fence_spans,
    normalise_blank_lines,
    resolve_includes,
    rewrite_links,
    split_frontmatter,
    strip_attr_lists,
    transform,
)


def dedent(text: str) -> str:
    return textwrap.dedent(text).strip("\n")


# --------------------------------------------------------------------------- #
# Frontmatter
# --------------------------------------------------------------------------- #


def test_split_frontmatter_reads_title_and_description():
    meta, body = split_frontmatter(
        dedent(
            """
            ---
            title: "Traefik Metrics Overview"
            description: "Metrics backends."
            ---

            # Metrics
            """
        )
    )
    assert meta.title == "Traefik Metrics Overview"
    assert meta.description == "Metrics backends."
    assert body.strip() == "# Metrics"


def test_split_frontmatter_falls_back_to_first_heading():
    """22 of 171 upstream pages carry no frontmatter."""
    meta, body = split_frontmatter("# Expose\n\nSome text.\n")
    assert meta.title == "Expose"
    assert meta.description == ""
    assert body.startswith("# Expose")


# --------------------------------------------------------------------------- #
# Fence scanning
# --------------------------------------------------------------------------- #


def test_fence_spans_handles_back_to_back_fences():
    """Adjacent fences with no blank line between must not merge into one span."""
    lines = ["```yaml", "a: 1", "```", "```toml", "b = 2", "```"]
    spans = fence_spans(lines)
    assert [(f.start, f.end) for f in spans] == [(0, 2), (3, 5)]
    assert [f.info for f in spans] == ["yaml", "toml"]


def test_fence_spans_ignores_shorter_inner_markers():
    lines = ["````markdown", "```yaml", "a: 1", "```", "````"]
    assert [(f.start, f.end) for f in fence_spans(lines)] == [(0, 4)]


# --------------------------------------------------------------------------- #
# Fence tabs -- the highest-volume construct (754 blocks upstream)
# --------------------------------------------------------------------------- #


def test_convert_fence_tabs_labels_and_keeps_language():
    out = convert_fence_tabs(
        dedent(
            """
            To enable metrics:

            ```yaml tab="File (YAML)"
            metrics:
              otlp: {}
            ```

            ```toml tab="File (TOML)"
            [metrics]
            ```
            """
        )
    )
    assert "**File (YAML)**" in out
    assert "**File (TOML)**" in out
    assert "```yaml" in out and "```toml" in out
    assert "tab=" not in out
    # Indentation inside the fence is untouched.
    assert "\n  otlp: {}" in out


def test_convert_fence_tabs_handles_missing_language():
    out = convert_fence_tabs('```tab="Labels"\nfoo\n```')
    assert out.splitlines()[0] == "**Labels**"
    assert "```\nfoo\n```" in out


def test_convert_fence_tabs_leaves_plain_fences_alone():
    source = "```bash\necho hi\n```"
    assert convert_fence_tabs(source) == source


# --------------------------------------------------------------------------- #
# Admonitions
# --------------------------------------------------------------------------- #


def test_admonition_becomes_blockquote_with_title():
    out = convert_blocks(
        dedent(
            """
            !!! info "Default protocol"

                The exporter uses HTTP by default.
            """
        )
    )
    assert "> **Info — Default protocol**" in out
    assert "> The exporter uses HTTP by default." in out
    # Exactly one blank blockquote separator, never two.
    assert ">\n>\n" not in out


def test_admonition_without_title():
    out = convert_blocks("!!! warning\n\n    Careful.\n")
    assert "> **Warning**" in out
    assert "> Careful." in out


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        # No space after the marker.
        ('!!!info "Kubernetes"\n\n    Body.\n', "> **Info — Kubernetes**"),
        # Unquoted title after a known kind.
        ("!!! note Referencing a resolver\n\n    Body.\n", "> **Note — Referencing a resolver**"),
        # No kind at all: the whole line is really a title.
        (
            "!!! Failover on Heathcheck Status\n\n    Body.\n",
            "> **Note — Failover on Heathcheck Status**",
        ),
        # Collapsible variants.
        ('??? example "Advanced"\n\n    Body.\n', "> **Example — Advanced**"),
        ('???+ tip "Open"\n\n    Body.\n', "> **Tip — Open**"),
    ],
)
def test_admonition_upstream_syntax_variants(source: str, expected: str):
    assert expected in convert_blocks(source)


def test_admonition_containing_a_fence():
    out = convert_blocks(
        dedent(
            """
            !!! note "Config"

                Use this:

                ```yaml
                a: 1
                ```
            """
        )
    )
    assert "> ```yaml" in out
    assert "> a: 1" in out


def test_nested_admonitions():
    out = convert_blocks(
        dedent(
            """
            !!! note "Outer"

                Intro.

                !!! tip "Inner"

                    Nested body.
            """
        )
    )
    assert "> **Note — Outer**" in out
    assert "> > **Tip — Inner**" in out
    assert "> > Nested body." in out


# --------------------------------------------------------------------------- #
# Tabbed blocks
# --------------------------------------------------------------------------- #


def test_tabbed_block_dedents_body():
    out = convert_blocks(
        dedent(
            """
            === "Docker"

                Run the container.

            === "Kubernetes"

                Apply the manifest.
            """
        )
    )
    assert "**Docker**" in out
    assert "\nRun the container." in out
    assert "**Kubernetes**" in out
    assert "===" not in out


# --------------------------------------------------------------------------- #
# Fence-awareness: the property that protects 754 fenced examples
# --------------------------------------------------------------------------- #


def test_constructs_inside_fences_are_never_rewritten():
    source = dedent(
        """
        ```go
        {{ normalize .Name }}
        !!! note "not an admonition"
        === "not a tab"
        {: .not-an-attr }
        ![img](assets/img/arch.png)
        ```
        """
    )
    assert convert_blocks(source) == source
    assert strip_attr_lists(source) == source


def test_fence_tab_syntax_inside_an_outer_fence_survives():
    source = '````markdown\n```yaml tab="Example"\na: 1\n```\n````'
    assert convert_fence_tabs(source) == source


# --------------------------------------------------------------------------- #
# attr_list
# --------------------------------------------------------------------------- #


def test_strip_attr_lists_removes_standalone_styling_lines():
    out = strip_attr_lists("# Title\n\nSubtitle text\n{: .subtitle }\n\nBody\n")
    assert "{: .subtitle }" not in out
    assert "Subtitle text" in out


def test_attr_list_inside_an_admonition_is_stripped(upstream: Upstream):
    """Regression: stripping after convert_blocks left a `> {: #anchor }` line."""
    page = upstream.content_dir / "page.md"
    page.write_text(
        dedent(
            """
            !!! warning "Security Note"

                Accessing the Docker API is a concern.
                {: #security-note }
            """
        )
        + "\n"
    )
    _, body = transform(page.read_text(), page_path="page.md", upstream=upstream)
    assert "{:" not in body
    assert "> Accessing the Docker API is a concern." in body


# --------------------------------------------------------------------------- #
# Includes
# --------------------------------------------------------------------------- #


def test_resolve_include_markdown_strips_nested_frontmatter(docs_tree: Path):
    content = docs_tree / "content"
    (content / "includes" / "blurb.md").write_text(
        '---\ntitle: "Blurb"\n---\n\n## Business\n\nCall us.\n'
    )
    page = content / "page.md"
    page.write_text('# Page\n\n{% include-markdown "includes/blurb.md" %}\n')

    out = resolve_includes(page.read_text(), source=page, content_dir=content, docs_dir=docs_tree)
    assert "## Business" in out
    assert "title:" not in out
    assert "include-markdown" not in out


def test_resolve_snippet_directive(docs_tree: Path):
    content = docs_tree / "content"
    (content / "shared.md").write_text("Shared body.\n")
    page = content / "page.md"
    page.write_text('--8<-- "content/shared.md"\n')

    out = resolve_includes(page.read_text(), source=page, content_dir=content, docs_dir=docs_tree)
    assert out.strip() == "Shared body."


def test_recursive_include(docs_tree: Path):
    content = docs_tree / "content"
    (content / "b.md").write_text("Deepest.\n")
    (content / "a.md").write_text('{% include-markdown "b.md" %}\n')
    page = content / "page.md"
    page.write_text('{% include-markdown "a.md" %}\n')

    out = resolve_includes(page.read_text(), source=page, content_dir=content, docs_dir=docs_tree)
    assert out.strip() == "Deepest."


def test_circular_include_is_detected(docs_tree: Path):
    content = docs_tree / "content"
    (content / "a.md").write_text('{% include-markdown "b.md" %}\n')
    (content / "b.md").write_text('{% include-markdown "a.md" %}\n')
    page = content / "a.md"

    with pytest.raises(RecursionError):
        resolve_includes(page.read_text(), source=page, content_dir=content, docs_dir=docs_tree)


def test_missing_include_raises(docs_tree: Path):
    content = docs_tree / "content"
    page = content / "page.md"
    page.write_text('{% include-markdown "nope.md" %}\n')

    with pytest.raises(FileNotFoundError):
        resolve_includes(page.read_text(), source=page, content_dir=content, docs_dir=docs_tree)


# --------------------------------------------------------------------------- #
# Links
# --------------------------------------------------------------------------- #


def test_asset_links_become_pinned_raw_urls(upstream: Upstream):
    out = rewrite_links(
        "![Architecture](../assets/img/arch.png)",
        page_path="setup/docker.md",
        upstream=upstream,
    )
    assert out == (
        "![Architecture](https://raw.githubusercontent.com/traefik/traefik/"
        f"{upstream.commit}/docs/content/assets/img/arch.png)"
    )


def test_html_img_src_is_rewritten(upstream: Upstream):
    out = rewrite_links(
        '<img src="../assets/img/arch.png" alt="x">',
        page_path="setup/docker.md",
        upstream=upstream,
    )
    assert f"/{upstream.commit}/docs/content/assets/img/arch.png" in out


def test_relative_md_links_are_left_alone(upstream: Upstream):
    source = "See [routers](../routing/routers.md#rule)."
    assert rewrite_links(source, page_path="setup/docker.md", upstream=upstream) == source


def test_pretty_url_gains_md_suffix(upstream: Upstream):
    """MkDocs page links omit the extension; restore it so it resolves for us."""
    content = upstream.content_dir
    (content / "routing").mkdir(parents=True, exist_ok=True)
    (content / "routing" / "routers.md").write_text("# Routers\n")

    out = rewrite_links(
        "See [routers](../routing/routers#rule).",
        page_path="setup/docker.md",
        upstream=upstream,
    )
    assert out == "See [routers](../routing/routers.md#rule)."


def test_directory_style_url_resolves_against_the_rendered_url(upstream: Upstream):
    """`use_directory_urls` puts the page at `<path>/`, one level below the file."""
    content = upstream.content_dir
    (content / "reference" / "routing").mkdir(parents=True, exist_ok=True)
    (content / "reference" / "routing" / "nginx.md").write_text("# Nginx\n")
    page = "reference/install/providers/nginx.md"

    out = rewrite_links(
        "See [nginx](../../../reference/routing/nginx/#opt).",
        page_path=page,
        upstream=upstream,
    )
    assert out == "See [nginx](../../routing/nginx.md#opt)."


def test_self_referencing_directory_url(upstream: Upstream):
    content = upstream.content_dir
    (content / "tcp").mkdir(parents=True, exist_ok=True)
    (content / "tcp" / "tls.md").write_text("# TLS\n")

    out = rewrite_links(
        "[here](./#certificate-resolver)", page_path="tcp/tls.md", upstream=upstream
    )
    assert out == "[here](tls.md#certificate-resolver)"


def test_external_and_anchor_links_untouched(upstream: Upstream):
    source = "[ext](https://example.com/x.png) [a](#section) [m](mailto:a@b.c)"
    assert rewrite_links(source, page_path="index.md", upstream=upstream) == source


# --------------------------------------------------------------------------- #
# Whole pipeline
# --------------------------------------------------------------------------- #


def test_normalise_blank_lines():
    assert normalise_blank_lines("a\n\n\n\n\nb\n\n\n") == "a\n\nb\n"


def test_transform_end_to_end(upstream: Upstream):
    content = upstream.content_dir
    (content / "includes" / "blurb.md").write_text("Contact sales.\n")
    page = content / "setup" / "docker.md"
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text(
        dedent(
            """
            ---
            title: "Docker"
            description: "Run Traefik on Docker."
            ---

            # Docker

            Subtitle
            {: .subtitle }

            !!! info "Heads up"

                Read this first.

            ```yaml tab="File (YAML)"
            entryPoints:
              web: {}
            ```

            ![arch](../assets/img/arch.png)

            {% include-markdown "includes/blurb.md" %}
            """
        )
        + "\n"
    )

    meta, body = transform(page.read_text(), page_path="setup/docker.md", upstream=upstream)

    assert meta.title == "Docker"
    assert meta.description == "Run Traefik on Docker."
    assert "> **Info — Heads up**" in body
    assert "**File (YAML)**" in body
    assert "```yaml" in body and "tab=" not in body
    assert "  web: {}" in body
    assert "{: .subtitle }" not in body
    assert "Contact sales." in body
    assert f"/{upstream.commit}/docs/content/assets/img/arch.png" in body
    assert body.endswith("\n") and "\n\n\n" not in body

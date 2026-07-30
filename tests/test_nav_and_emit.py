"""Tests for nav parsing and the emitted artefacts."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from traefik_llms_docs.emit import (
    build_version,
    is_partial,
    orphan_pages,
    render_llms_txt,
    render_root_index,
)
from traefik_llms_docs.models import Upstream
from traefik_llms_docs.nav import clean_label, load_nav

MKDOCS = """
site_name: Traefik
site_description: Traefik Documentation
docs_dir: 'content'
nav:
  - 'What is Traefik': 'index.md'
  - 'Getting Started':
      - 'Overview': 'getting-started/index.md'
      - 'Quick Start':
        - 'Docker': 'getting-started/docker.md'
  - '<span class="nav-link-with-icon">Secure with JWT <img src="x.svg"></span>': 'secure/jwt.md'
  - 'Contributing':
      - 'Thank You!': 'contributing/thank-you.md'
  - 'Duplicate': 'index.md'
"""


@pytest.fixture
def nav_tree(docs_tree: Path) -> Path:
    (docs_tree / "mkdocs.yml").write_text(textwrap.dedent(MKDOCS).lstrip())
    content = docs_tree / "content"
    for rel, title in (
        ("index.md", "What is Traefik"),
        ("getting-started/index.md", "Overview"),
        ("getting-started/docker.md", "Docker"),
        ("secure/jwt.md", "JWT"),
        ("contributing/thank-you.md", "Thank You"),
    ):
        path = content / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f'---\ntitle: "{title}"\ndescription: "About {title}."\n---\n\n# {title}\n')
    return docs_tree


def test_clean_label_strips_icon_markup():
    raw = '<span class="nav-link-with-icon">Secure Access with JWT <img src="x.svg"></span>'
    assert clean_label(raw) == "Secure Access with JWT"


def test_clean_label_leaves_plain_text():
    assert clean_label("Getting Started") == "Getting Started"


def test_load_nav_flattens_and_keeps_order(nav_tree: Path):
    nav = load_nav(nav_tree / "mkdocs.yml")
    assert [e.path for e in nav] == [
        "index.md",
        "getting-started/index.md",
        "getting-started/docker.md",
        "secure/jwt.md",
        "contributing/thank-you.md",
    ]


def test_load_nav_deduplicates_repeated_pages(nav_tree: Path):
    """Upstream lists tlsoption.md and tlsstore.md under two sections each."""
    nav = load_nav(nav_tree / "mkdocs.yml")
    assert [e.path for e in nav].count("index.md") == 1


def test_nav_carries_section_breadcrumb(nav_tree: Path):
    nav = {e.path: e for e in load_nav(nav_tree / "mkdocs.yml")}
    docker = nav["getting-started/docker.md"]
    assert docker.trail == ("Getting Started", "Quick Start")
    assert docker.section == "Getting Started"
    assert docker.breadcrumb == "Getting Started / Quick Start / Docker"
    assert nav["index.md"].section == "Overview"


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("operations/include-api-examples.md", True),
        ("https/include-acme-single-domain-example.md", True),
        ("includes/service-by-label.md", True),
        ("setup/docker.md", False),
        ("reference/install-configuration/api-dashboard.md", False),
    ],
)
def test_is_partial(path: str, expected: bool):
    assert is_partial(path) is expected


def test_orphan_pages_ignores_empty_stubs(nav_tree: Path):
    """cli-ref.md and env-ref.md are empty upstream, so they are not orphans."""
    content = nav_tree / "content"
    (content / "reference").mkdir(parents=True, exist_ok=True)
    (content / "reference" / "cli-ref.md").write_text("")
    covered = {e.path for e in load_nav(nav_tree / "mkdocs.yml")}
    upstream_stub = Upstream.__new__(Upstream)
    object.__setattr__(upstream_stub, "docs_dir", nav_tree)
    assert orphan_pages(upstream_stub, covered) == []

    (content / "reference" / "real.md").write_text("# Real content\n")
    assert orphan_pages(upstream_stub, covered) == ["reference/real.md"]


@pytest.mark.usefixtures("nav_tree")
def test_build_version_writes_expected_tree(upstream: Upstream, tmp_path: Path):
    out_root = tmp_path / "out"
    result = build_version(upstream, out_root)

    version_dir = out_root / "traefik" / "v3.7"
    assert len(result.pages) == 5
    assert (version_dir / "llms.txt").is_file()
    assert (version_dir / "llms-full.txt").is_file()
    assert (version_dir / "SOURCE").is_file()
    assert (version_dir / "pages" / "getting-started" / "docker.md").is_file()

    page = (version_dir / "pages" / "getting-started" / "docker.md").read_text()
    assert 'title: "Docker"' in page
    assert 'breadcrumb: "Getting Started / Quick Start / Docker"' in page
    assert upstream.commit in page

    source = (version_dir / "SOURCE").read_text()
    assert f"upstream_commit: {upstream.commit}" in source
    assert "pages: 5" in source


@pytest.mark.usefixtures("nav_tree")
def test_llms_txt_puts_contributing_under_optional(upstream: Upstream):
    from traefik_llms_docs.emit import build_pages

    pages = build_pages(upstream)
    out = render_llms_txt(pages, upstream, "Traefik Documentation")

    assert out.startswith("# Traefik Proxy v3.7")
    assert "> Traefik Documentation" in out
    assert "## Optional" in out
    optional_body = out.split("## Optional", 1)[1]
    assert "Thank You" in optional_body
    assert "Getting Started / Quick Start / Docker" not in optional_body
    assert out.count("\n- [") == 5


@pytest.mark.usefixtures("nav_tree")
def test_llms_txt_links_are_absolute_raw_urls(upstream: Upstream):
    from traefik_llms_docs.emit import build_pages

    out = render_llms_txt(build_pages(upstream), upstream, "summary")
    assert (
        "https://raw.githubusercontent.com/mlshdev/traefik-llms-docs/main/"
        "traefik/v3.7/pages/getting-started/docker.md" in out
    )


@pytest.mark.usefixtures("nav_tree")
def test_root_index_is_a_pointer_not_a_copy(upstream: Upstream, tmp_path: Path):
    result = build_version(upstream, tmp_path / "out")
    out = render_root_index([result])
    assert "traefik/v3.7/llms.txt" in out
    assert "traefik/v3.7/llms-full.txt" in out
    assert "# Docker" not in out  # no page bodies inlined
    assert len(out) < 2000


@pytest.mark.usefixtures("nav_tree")
def test_prune_removes_files_a_rebuild_no_longer_produces(upstream: Upstream, tmp_path: Path):
    from traefik_llms_docs.emit import prune_stale

    out_root = tmp_path / "out"
    result = build_version(upstream, out_root)
    stale = out_root / "traefik" / "v3.7" / "pages" / "gone" / "old.md"
    stale.parent.mkdir(parents=True, exist_ok=True)
    stale.write_text("dropped upstream\n")

    removed = prune_stale(out_root, [result])

    assert stale in removed
    assert not stale.exists()
    assert (out_root / "traefik" / "v3.7" / "pages" / "index.md").is_file()

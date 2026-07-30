"""Build configuration.

Adding a documentation version is a one-line change to ``TRACKED``.
"""

from __future__ import annotations

from typing import Final

from traefik_llms_docs.models import VersionSpec

UPSTREAM_REPO: Final = "https://github.com/traefik/traefik.git"
UPSTREAM_SLUG: Final = "traefik/traefik"

THIS_REPO_SLUG: Final = "mlshdev/traefik-llms-docs"
THIS_REPO_BRANCH: Final = "main"

#: Versions built and kept in sync. Order matters: the first entry is "latest"
#: and is what the root llms.txt points at.
TRACKED: Final[tuple[VersionSpec, ...]] = (VersionSpec(branch="v3.7", label="v3.7"),)

#: Source files that are include-only partials: they are pulled into other pages
#: and must never be emitted as standalone pages. Mirrors the mkdocs ``exclude``
#: plugin glob plus the ``includes/`` helper directory.
PARTIAL_GLOBS: Final[tuple[str, ...]] = ("**/include-*.md", "includes/*.md")

#: Pages under these top-level nav sections go under the llms.txt ``## Optional``
#: heading, per the llmstxt.org spec: useful, but skippable under context pressure.
OPTIONAL_SECTIONS: Final[frozenset[str]] = frozenset({"Contributing", "Deprecation Notices"})


def raw_url_for(version_label: str, page_path: str) -> str:
    """Absolute raw URL for a generated page in *this* repo."""
    return (
        f"https://raw.githubusercontent.com/{THIS_REPO_SLUG}/{THIS_REPO_BRANCH}"
        f"/traefik/{version_label}/pages/{page_path}"
    )

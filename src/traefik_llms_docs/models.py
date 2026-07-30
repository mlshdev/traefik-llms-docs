"""Typed data structures shared across the build pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class Admonition(StrEnum):
    """MkDocs admonition kinds that appear in the Traefik docs.

    The value is the label rendered into the blockquote heading.
    """

    NOTE = "Note"
    INFO = "Info"
    TIP = "Tip"
    WARNING = "Warning"
    DANGER = "Danger"
    CAUTION = "Caution"
    IMPORTANT = "Important"
    EXAMPLE = "Example"
    QUESTION = "Question"
    QUOTE = "Quote"
    ABSTRACT = "Abstract"
    SUCCESS = "Success"
    FAILURE = "Failure"
    BUG = "Bug"

    @classmethod
    def label_for(cls, raw: str) -> str:
        """Map a raw admonition type to a display label, falling back to title case."""
        try:
            return cls[raw.upper()].value
        except KeyError:
            return raw.replace("-", " ").title()


@dataclass(frozen=True, slots=True)
class VersionSpec:
    """A tracked upstream documentation version."""

    branch: str
    label: str

    @property
    def output_dir(self) -> Path:
        return Path("traefik") / self.label


@dataclass(frozen=True, slots=True)
class Upstream:
    """A resolved upstream checkout: which commit, and where it lives on disk."""

    spec: VersionSpec
    commit: str
    docs_dir: Path
    """Path to the ``docs/`` directory of the upstream checkout."""

    @property
    def content_dir(self) -> Path:
        return self.docs_dir / "content"

    @property
    def mkdocs_yml(self) -> Path:
        return self.docs_dir / "mkdocs.yml"

    def blob_url(self, relative: str) -> str:
        """Permalink to an upstream file, pinned to the resolved commit."""
        return f"https://github.com/traefik/traefik/blob/{self.commit}/docs/content/{relative}"

    def raw_url(self, relative: str) -> str:
        """Raw content URL for an upstream file, pinned to the resolved commit."""
        return (
            "https://raw.githubusercontent.com/traefik/traefik/"
            f"{self.commit}/docs/content/{relative}"
        )


@dataclass(frozen=True, slots=True)
class NavEntry:
    """A single page in the mkdocs ``nav`` tree, flattened but order-preserving."""

    title: str
    path: str
    """Page path relative to ``docs/content``, e.g. ``getting-started/index.md``."""
    trail: tuple[str, ...]
    """Section breadcrumb, outermost first. Empty for top-level pages."""

    @property
    def section(self) -> str:
        return self.trail[0] if self.trail else "Overview"

    @property
    def breadcrumb(self) -> str:
        return " / ".join((*self.trail, self.title))


@dataclass(frozen=True, slots=True)
class Page:
    """A fully transformed documentation page, ready to emit."""

    nav: NavEntry
    title: str
    description: str
    body: str

    @property
    def out_path(self) -> Path:
        return Path(self.nav.path)


@dataclass(frozen=True, slots=True)
class BuildResult:
    """Summary of one version build."""

    upstream: Upstream
    pages: tuple[Page, ...]
    written: tuple[Path, ...]

"""Parse the mkdocs ``nav`` tree into a flat, order-preserving page list.

The nav is authoritative for both ordering and page titles. Upstream verification
showed 162 nav entries covering every non-partial page, so nav traversal alone is
complete -- there is no orphan-page fallback to worry about.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from traefik_llms_docs.models import NavEntry

_HTML_TAG = re.compile(r"<[^>]+>")
_WHITESPACE = re.compile(r"\s+")


def clean_label(raw: str) -> str:
    """Strip HTML from a nav label and collapse whitespace.

    14 upstream labels wrap the text in markup for icon badges, e.g.::

        <span class="nav-link-with-icon">Secure Access with JWT <img ...></span>

    which must reduce to ``Secure Access with JWT``.
    """
    return _WHITESPACE.sub(" ", _HTML_TAG.sub("", raw)).strip()


def _walk(node: Any, trail: tuple[str, ...]) -> list[NavEntry]:
    entries: list[NavEntry] = []
    if not isinstance(node, list):
        return entries
    for item in node:
        if isinstance(item, str):
            # Bare path with no title; derive one from the filename.
            entries.append(
                NavEntry(title=Path(item).stem.replace("-", " ").title(), path=item, trail=trail)
            )
            continue
        if not isinstance(item, dict):
            continue
        for raw_label, value in item.items():
            label = clean_label(str(raw_label))
            if isinstance(value, str):
                if value.endswith(".md"):
                    entries.append(NavEntry(title=label, path=value, trail=trail))
            else:
                entries.extend(_walk(value, (*trail, label)))
    return entries


def load_nav(mkdocs_yml: Path) -> list[NavEntry]:
    """Read ``mkdocs.yml`` and return its nav as a flat ordered list.

    ``yaml.safe_load`` is sufficient: the upstream config carries no custom tags.
    """
    config = yaml.safe_load(mkdocs_yml.read_text(encoding="utf-8"))
    if not isinstance(config, dict) or "nav" not in config:
        msg = f"{mkdocs_yml} has no 'nav' section"
        raise ValueError(msg)
    entries = _walk(config["nav"], ())

    # A page may legitimately appear twice in the nav; emit it once, first-wins.
    seen: set[str] = set()
    unique: list[NavEntry] = []
    for entry in entries:
        if entry.path in seen:
            continue
        seen.add(entry.path)
        unique.append(entry)
    return unique


def site_description(mkdocs_yml: Path) -> str:
    config = yaml.safe_load(mkdocs_yml.read_text(encoding="utf-8"))
    if isinstance(config, dict):
        return str(config.get("site_description", "")).strip()
    return ""

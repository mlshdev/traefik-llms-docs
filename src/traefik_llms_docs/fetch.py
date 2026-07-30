"""Resolve and fetch the upstream Traefik docs.

Only ``docs/`` is fetched, via a blobless sparse clone: ~15 MB instead of the
~500 MB a full clone of the Go repository would cost.
"""

from __future__ import annotations

import shutil
import subprocess
from typing import TYPE_CHECKING

from traefik_llms_docs.config import UPSTREAM_REPO
from traefik_llms_docs.models import Upstream, VersionSpec

if TYPE_CHECKING:
    from pathlib import Path


def _run(args: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def resolve_commit(spec: VersionSpec) -> str:
    """Resolve a branch to its current commit SHA without cloning anything."""
    out = _run(["git", "ls-remote", UPSTREAM_REPO, f"refs/heads/{spec.branch}"])
    if not out:
        msg = f"upstream branch {spec.branch!r} not found"
        raise ValueError(msg)
    return out.split()[0]


def sparse_clone(spec: VersionSpec, dest: Path) -> Upstream:
    """Blobless sparse clone of ``docs/`` at the tip of ``spec.branch``."""
    if dest.exists():
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    _run(
        [
            "git",
            "clone",
            "--filter=blob:none",
            "--sparse",
            "--depth=1",
            "--branch",
            spec.branch,
            UPSTREAM_REPO,
            str(dest),
        ]
    )
    _run(["git", "sparse-checkout", "set", "docs"], cwd=dest)
    commit = _run(["git", "rev-parse", "HEAD"], cwd=dest)
    return Upstream(spec=spec, commit=commit, docs_dir=dest / "docs")


def from_existing(spec: VersionSpec, checkout: Path) -> Upstream:
    """Build an :class:`Upstream` from an already-present checkout.

    Used for local iteration so a rebuild does not re-clone.
    """
    docs_dir = checkout / "docs"
    if not docs_dir.is_dir():
        msg = f"{checkout} does not look like a traefik checkout (no docs/)"
        raise ValueError(msg)
    commit = _run(["git", "rev-parse", "HEAD"], cwd=checkout)
    return Upstream(spec=spec, commit=commit, docs_dir=docs_dir)

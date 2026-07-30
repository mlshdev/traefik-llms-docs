from __future__ import annotations

from pathlib import Path

import pytest

from traefik_llms_docs.models import Upstream, VersionSpec

COMMIT = "43dd7e1e03c843860ea728adee0edbc0c009b3a0"


@pytest.fixture
def docs_tree(tmp_path: Path) -> Path:
    """A minimal stand-in for the upstream ``docs/`` directory."""
    content = tmp_path / "docs" / "content"
    (content / "includes").mkdir(parents=True)
    (content / "assets" / "img").mkdir(parents=True)
    (content / "assets" / "img" / "arch.png").write_bytes(b"png")
    return tmp_path / "docs"


@pytest.fixture
def upstream(docs_tree: Path) -> Upstream:
    return Upstream(
        spec=VersionSpec(branch="v3.7", label="v3.7"),
        commit=COMMIT,
        docs_dir=docs_tree,
    )

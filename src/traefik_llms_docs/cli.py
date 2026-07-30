"""Command line entry point."""

from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
from pathlib import Path

from traefik_llms_docs import __version__
from traefik_llms_docs.config import TRACKED
from traefik_llms_docs.emit import build_version, prune_stale, render_root_index
from traefik_llms_docs.fetch import from_existing, resolve_commit, sparse_clone
from traefik_llms_docs.models import BuildResult, Upstream, VersionSpec

ROOT_INDEX = "llms.txt"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _upstreams(args: argparse.Namespace, work: Path) -> list[Upstream]:
    specs = list(TRACKED)
    if args.branch:
        specs = [VersionSpec(branch=args.branch, label=args.branch)]
    if args.checkout:
        checkout = Path(args.checkout).resolve()
        return [from_existing(specs[0], checkout)]
    return [sparse_clone(spec, work / spec.label) for spec in specs]


def _committed_sha(out_root: Path, spec: VersionSpec) -> str | None:
    source = out_root / spec.output_dir / "SOURCE"
    if not source.is_file():
        return None
    for line in source.read_text(encoding="utf-8").splitlines():
        if line.startswith("upstream_commit:"):
            return line.split(":", 1)[1].strip()
    return None


def cmd_resolve(args: argparse.Namespace) -> int:
    """Print each tracked branch's upstream SHA and whether it differs from ours."""
    out_root = Path(args.out).resolve()
    changed = False
    for spec in TRACKED:
        remote = resolve_commit(spec)
        local = _committed_sha(out_root, spec)
        differs = remote != local
        changed = changed or differs
        print(f"{spec.label}\t{remote}\tlocal={local or 'none'}\tchanged={str(differs).lower()}")
    print(f"changed={str(changed).lower()}")
    return 0


def _build(args: argparse.Namespace, out_root: Path) -> list[BuildResult]:
    with tempfile.TemporaryDirectory(prefix="traefik-llms-docs-") as tmp:
        upstreams = _upstreams(args, Path(tmp))
        results = [build_version(u, out_root) for u in upstreams]
    prune_stale(out_root, results)
    (out_root / ROOT_INDEX).write_text(render_root_index(results), encoding="utf-8")
    return results


def cmd_build(args: argparse.Namespace) -> int:
    out_root = Path(args.out).resolve()
    out_root.mkdir(parents=True, exist_ok=True)
    results = _build(args, out_root)
    for result in results:
        print(
            f"built {result.upstream.spec.label}: {len(result.pages)} pages "
            f"from {result.upstream.commit[:12]}"
        )
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    """Rebuild into a scratch tree and diff against the committed one.

    SOURCE carries a build timestamp, so it is compared on its upstream_commit
    line only -- otherwise every check would report a spurious difference.
    """
    committed = Path(args.out).resolve()
    with tempfile.TemporaryDirectory(prefix="traefik-llms-check-") as tmp:
        fresh = Path(tmp) / "out"
        fresh.mkdir(parents=True)
        _build(args, fresh)

        def relevant(root: Path) -> dict[str, str]:
            files: dict[str, str] = {}
            for path in sorted(root.rglob("*")):
                if not path.is_file():
                    continue
                rel = str(path.relative_to(root))
                if not (rel == ROOT_INDEX or rel.startswith("traefik/")):
                    continue
                text = path.read_text(encoding="utf-8")
                if path.name == "SOURCE":
                    text = "\n".join(
                        line
                        for line in text.splitlines()
                        if not line.startswith(("built_at:", "generator:"))
                    )
                files[rel] = text
            return files

        want, have = relevant(fresh), relevant(committed)
        added = sorted(set(want) - set(have))
        removed = sorted(set(have) - set(want))
        modified = sorted(k for k in set(want) & set(have) if want[k] != have[k])

    if not (added or removed or modified):
        print("up to date")
        return 0
    for label, items in (("missing", added), ("stale", removed), ("modified", modified)):
        for item in items:
            print(f"{label}: {item}", file=sys.stderr)
    print(
        f"\n{len(added) + len(removed) + len(modified)} file(s) differ; run "
        "`uv run traefik-llms-docs build`",
        file=sys.stderr,
    )
    return 1


def main(argv: list[str] | None = None) -> int:
    # Shared options live on a parent parser so they are accepted both before and
    # after the subcommand.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "--out",
        default=str(_repo_root()),
        help="repository root to write the generated tree into (default: repo root)",
    )
    common.add_argument(
        "--branch",
        help="override the tracked branch (default: every entry in config.TRACKED)",
    )
    common.add_argument(
        "--checkout",
        help="use an existing traefik checkout instead of cloning (local iteration)",
    )

    parser = argparse.ArgumentParser(
        prog="traefik-llms-docs",
        description="Convert the Traefik Proxy documentation into LLM-friendly Markdown.",
        parents=[common],
    )
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("build", parents=[common], help="generate the tree (default)").set_defaults(
        func=cmd_build
    )
    sub.add_parser(
        "check", parents=[common], help="fail if the committed tree is stale"
    ).set_defaults(func=cmd_check)
    sub.add_parser(
        "resolve", parents=[common], help="print upstream SHAs without building"
    ).set_defaults(func=cmd_resolve)

    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        args.func = cmd_build
    if shutil.which("git") is None and not args.checkout:
        print("git is required", file=sys.stderr)
        return 2
    result: int = args.func(args)
    return result


if __name__ == "__main__":
    raise SystemExit(main())

# traefik-llms-docs

The [Traefik Proxy](https://github.com/traefik/traefik) documentation, converted from MkDocs
Markdown into plain Markdown that an LLM can read correctly — and kept in sync automatically.

Upstream publishes no `llms.txt`. This repository generates one, plus a single-file corpus and one
cleaned file per page, and rebuilds whenever the upstream docs change.

## What's here

| Path | What it is |
|---|---|
| [`llms.txt`](llms.txt) | Root pointer index across all tracked versions ([llmstxt.org](https://llmstxt.org) format) |
| `traefik/<version>/llms.txt` | Nav-ordered index: one link per page, with the upstream description |
| `traefik/<version>/llms-full.txt` | Every page concatenated into one file (~250k tokens) |
| `traefik/<version>/pages/**/*.md` | One cleaned page per upstream page, mirroring upstream paths |
| `traefik/<version>/SOURCE` | Provenance: the exact upstream commit this build came from |

Generated files are committed to the repository tree, not attached to releases, so any tool can
fetch them by raw URL without authentication:

```
https://raw.githubusercontent.com/mlshdev/traefik-llms-docs/main/traefik/v3.7/llms.txt
```

Every page carries YAML frontmatter with `title`, `description`, `section`, `breadcrumb`,
`traefik_version`, `upstream_path` and a `source_url` permalink pinned to the build commit — enough
metadata to chunk and cite the corpus in a RAG pipeline.

## What the conversion does

MkDocs Markdown is not plain Markdown. Left as-is, an LLM reads the extension syntax as content.
Each pass below is fence-aware, so code blocks are never rewritten — which matters here, because
these docs embed hundreds of fenced Go-template (`{{ ... }}`) and shell examples.

| Upstream syntax | Becomes | Scale |
|---|---|---|
| ` ```yaml tab="File (YAML)" ` | `**File (YAML)**` above a plain ` ```yaml ` fence | 754 blocks / 116 files |
| `!!! info "Title"` / `??? note` | `> **Info — Title**` blockquote | 123 files |
| `{% include-markdown "..." %}` | Inlined, recursively, with cycle detection | 55 files |
| `--8<-- "content/..."` | Inlined | 1 |
| `=== "Tab"` | `**Tab**` + de-indented body | 5 files |
| `{: .subtitle }` | Removed | 22 |
| `../assets/img/x.png` | Absolute raw URL pinned to the build commit | all |
| `../routing/nginx/#anchor` | `../routing/nginx.md#anchor` | 948 internal links, 0 broken |

Directory-style links deserve a note: with MkDocs' default `use_directory_urls`, a page renders one
path level below its source file, so links an author wrote against the rendered URL do not resolve
against the file tree. Both bases are tried against the real upstream tree, file-relative first — the
target is never guessed from its extension.

Page order and titles come from the upstream `mkdocs.yml` `nav` tree, which is authoritative and
covers every non-partial page. Nav labels containing icon markup are stripped to their text.

## Why no MkDocs, and no Docker

The build never renders the site. Rendering to HTML and converting back would destroy exactly what
makes this source valuable: the tabbed fences lose their language tags inside `<div class="tabbed-set">`
markup. Working Markdown-to-Markdown preserves fences, languages and frontmatter intact.

That drops the dependency set to **PyYAML alone**, so there is nothing to containerise. Upstream's
own `docs.Dockerfile` exists to install `gcc`/`musl-dev`/`python3-dev` for building MkDocs wheels;
none of that applies. A GitHub runner is already an ephemeral sandbox, so a container would add pull
latency and a Dockerfile to maintain for no isolation benefit. Reproducibility comes from the
committed `uv.lock` instead.

Upstream is fetched with a blobless sparse clone of `docs/` only — about 15 MB, against roughly
500 MB for a full clone of the Go repository. There is no submodule: a submodule pointer can only
track one branch, and provenance is already recorded exactly in `SOURCE`.

## Automation

`.github/workflows/build.yml` runs daily and on demand:

1. `resolve` — `git ls-remote` the tracked branch and compare against the SHA in `SOURCE`. No clone,
   so polling is nearly free.
2. `build` — only if the SHA moved: sparse-clone, regenerate, commit and push. The commit message
   records the upstream SHA.

The output is a pure function of the upstream commit and the generator version — no build timestamp
anywhere — so a rebuild that finds nothing new leaves the tree byte-identical and pushes nothing.

Pull requests run `check` (rebuild into a scratch tree and diff) plus `pytest`, `ruff` and `ty`
instead of pushing.

Dependabot covers the two ecosystems that have a manifest here, `github-actions` and `uv`, weekly and
grouped. Its PRs merge automatically once CI goes green — gated on the CI run finishing rather than
on a required status check, since a required check on `main` would also block the build workflow's
own commit, and a user-owned repository cannot grant the Actions app a ruleset bypass.

## Local use

```bash
uv sync
uv run traefik-llms-docs build       # clone upstream and regenerate
uv run traefik-llms-docs check       # fail if the committed tree is stale
uv run traefik-llms-docs resolve     # print upstream SHAs, no clone
uv run pytest
```

Iterate against an existing checkout instead of re-cloning:

```bash
uv run traefik-llms-docs build --checkout ../traefik
```

Track another version by appending one `VersionSpec` to `TRACKED` in
`src/traefik_llms_docs/config.py`.

## Licence

The build tooling in `src/` and `tests/` is MIT. The generated documentation under `traefik/` is
derived from [traefik/traefik](https://github.com/traefik/traefik) and remains under its original
MIT licence, copyright Traefik Labs.

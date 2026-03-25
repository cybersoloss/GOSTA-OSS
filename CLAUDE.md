# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

GOSTA is a **specification and protocol framework** — not a software application. The primary artifacts are markdown files. There are no build steps, no test runner, and no compilation. The only executable artifact is `cowork/tools/pool-agent.py` (a Python CLI for offline semantic search over reference pools).

## Running Sessions

**Starting a new GOSTA session:**
```
Read cowork/startup.md and start a new session.
```
This triggers the interactive bootstrapper, which scaffolds `sessions/[name]/` and produces a Governor-approved Operating Document.

**Resuming an existing session:** Navigate to the session directory and read `00-BOOTSTRAP.md` first — it is the orientation file for every re-entry. Then load files in the Context Loading Order it specifies.

**Session directories** are created under `sessions/` and are gitignored — they are working directories, not publishable content.

## Pre-commit Hook

The hook lives at `.github/hooks/pre-commit` but must be installed manually:

```bash
cp .github/hooks/pre-commit .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
```

It blocks commits that:
- Stage files from private or working directories (sessions, internal tooling, etc.)
- Contain references that belong in internal repositories rather than the public project

Do not attempt to work around this hook. If it fires, remove the offending content before committing.

## Gitignore Rules (Key Ones)

- `sessions/` — working session directories, never committed
- `*.onnx` — the embedding model file for pool-agent. Download separately; do not commit
- `reference-pool*.yaml` — reference pool indexes (rebuild locally)
- `*.pdf`, `.claude/` — uploaded content and local config

## Architecture and Document Relationships

```
GOSTA-agentic-execution-architecture.md    ← The specification (8,100+ lines, 22 sections)
                                               Source of truth. Protocols derive from it.
cowork/
  gosta-cowork-protocol.md                 ← Tier 0 execution protocol. Governs session lifecycle,
                                               phase gates, health computation, signal format, etc.
  startup.md                               ← Interactive session bootstrapper (entry point)
  deliberation-protocol.md                 ← Multi-agent deliberation (3 roles, round mechanics)
  od-drafting-protocol.md                  ← OD authoring (structured questions → OD)
  sync-manifest.md                         ← Derivation map: spec section → protocol section.
                                               Consult this after any spec edit to find what needs review.
  CLAUDE.md                                ← Per-session Claude Code directive. Copied into
                                               sessions/[name]/ during bootstrap, then customized.
  templates/                               ← 13 stub templates (OD, domain model, health report, etc.)
  tools/pool-agent.py                      ← Offline semantic search over reference pools
domain-models/examples/                    ← Shared reusable domain models
docs/                                      ← Walkthrough, quick start, worked examples
sessions/[name]/                           ← Live session directories (gitignored)
  00-BOOTSTRAP.md                          ← Session orientation file. Read this first every time.
  operating-document.md                    ← The 5-layer OD being executed
  domain-models/                           ← Session-specific domain models
  signals/, health-reports/, decisions/    ← Append-only execution artifacts
  deliverables/, session-logs/             ← Output artifacts
```

The spec is the source of truth. `sync-manifest.md` tracks every point where a protocol section derives from a spec section — use it when updating either to find what else needs to change.

## The pool-agent Tool

`cowork/tools/pool-agent.py` provides offline semantic search using all-MiniLM-L6-v2 (quantized ONNX). The model file (`model.onnx`, 22MB) lives at `cowork/tools/pool-agent/models/` and is gitignored — download it separately.

**Dependencies:** `numpy`, `pyyaml`, `onnxruntime`

```bash
# Install dependencies
pip3 install numpy pyyaml onnxruntime

# Build a vector store
python3 cowork/tools/pool-agent.py build --pool reference-pool.yaml --articles ./sources/ --store ./pool-store/

# Query during a session
python3 cowork/tools/pool-agent.py query "your query" --store ./pool-store/ --top 10

# Update or delete entries
python3 cowork/tools/pool-agent.py update --pool reference-pool.yaml --dir ./new-sources/ --store ./pool-store/
python3 cowork/tools/pool-agent.py delete --pool reference-pool.yaml --store ./pool-store/ --ids RP-042
```

The protocol uses score thresholds: ≥0.58 = read full article, 0.50–0.57 = excerpt only, <0.50 = ignore.

## Contributing

See `CONTRIBUTING.md`. Key constraints:
- GOSTA is **provider-agnostic** — do not add dependencies on specific AI providers or orchestration frameworks
- Domain models contributed to `domain-models/examples/` must cite their primary source and be original analysis, not structured extractions of copyrighted material
- AI-assisted contributions are welcome but must be disclosed in the PR description (tool used, what it generated, what was edited)

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

GOSTA is a **specification and protocol framework** — not a software application. The primary artifacts are markdown files. There are no build steps, no test runner, and no compilation. Executable artifacts are `cowork/tools/pool-agent.py` (a Python CLI for offline semantic search over reference pools) and the shell scripts in `cowork/hooks/` (Claude Code hooks for automatic dispatch logging and closeout auditing).

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
GOSTA-agentic-execution-architecture.md    ← The specification (8,500+ lines, 22 sections)
                                               Source of truth. Protocols derive from it.
cowork/
  gosta-cowork-protocol.md                 ← Tier 0 execution protocol. Governs session lifecycle,
                                               phase gates, health computation, signal format, etc.
  startup.md                               ← Interactive session bootstrapper (entry point)
  deliberation-protocol.md                 ← Multi-agent deliberation (3 roles, round mechanics)
  evidence-collection-protocol.md          ← Evidence collection (§14.8 operationalization, quality gates,
                                               engagement audit, archive lifecycle)
  domain-model-authoring-protocol.md        ← Source-to-domain-model extraction procedure
  od-drafting-protocol.md                  ← OD authoring for complex/vague scopes (structured
                                               decomposition questions → OD). Used when direct
                                               authoring is insufficient; see startup.md Step 9.
  sync-manifest.md                         ← Derivation map: spec section → protocol section.
                                               Consult this after any spec edit to find what needs review.
  CLAUDE.md                                ← Per-session Claude Code directive. Copied into
                                               sessions/[name]/ during bootstrap, then customized.
  templates/                               ← 14 stub templates + hooks configuration (OD, domain model, health report, etc.)
  hooks/                                   ← Claude Code hooks for automatic dispatch logging
                                               and closeout auditing (§19.7). Shell scripts.
  tools/pool-agent.py                      ← Offline semantic search over reference pools
  evidence-archive/                        ← Promoted evidence items with aging/re-verification
domain-models/examples/                    ← Shared reusable domain models
docs/                                      ← Walkthrough, quick start, worked examples
sessions/[name]/                           ← Live session directories (gitignored)
  00-BOOTSTRAP.md                          ← Session orientation file. Read this first every time.
  operating-document.md                    ← The 5-layer OD being executed
  domain-models/                           ← Session-specific domain models
  signals/, health-reports/, decisions/    ← Append-only execution artifacts
  deliverables/, session-logs/             ← Output artifacts
  osint/                                   ← Evidence items, manifest, config (when enabled)
```

The spec is the source of truth. `sync-manifest.md` tracks every point where a protocol section derives from a spec section — use it when updating either to find what else needs to change.

## Fresh Framework Read (FFR)

The source of truth is `GOSTA-agentic-execution-architecture.md` (the spec). All other `.md` files in this repo derive from it and may contain errors or lag behind.

**Before any spec or protocol work:**

1. Scan all `##`-level headings in the spec to build a complete section map. Note every section, its number, and its title. This is your table of contents.
2. For your specific task, identify which sections are relevant from the heading scan, then read those sections in full from the spec itself. If no specific task is given, read all sections sequentially.
3. If the task touches protocols (`cowork/`, deliberation, OD drafting), read the relevant spec section first, then the corresponding protocol section. The spec defines intent; the protocol defines operationalization.

**Rules:**
- Do NOT use sync-manifest.md, changelogs, reading guides, or other derivative files to decide what to read. Use them only after forming your own understanding from the spec, and only to find protocol sections that need updating.
- Do NOT trust component counts, version numbers, or feature lists from any file other than the spec. If a derivative file disagrees with the spec, the spec wins.
- When editing protocols, read the relevant spec section first, then the protocol section. Never edit a protocol based solely on another protocol's description of what the spec says.

## Change Authoring Principles

Changes to the spec, protocols, or templates originate from session-specific observations (shortfalls, feedback, PCCAs), but the changes themselves must be **domain-agnostic and generic**. The framework is domain-agnostic by design (spec §0.1) — domain models are content, not framework structure.

When editing any file in this repo (excluding `sessions/`):
- Frame mechanisms in terms of roles (Governor, orchestrator, agent), structural concepts (guardrails, phase gates, signals), and abstract examples — not in terms of specific vendors, products, domains, or session types.
- If examples are needed, use diverse domains (e.g., regulatory analysis, product roadmap, hiring pipeline) rather than drawing all examples from the session that motivated the change.
- Test the change mentally: would this text make sense to a Governor running a completely different type of session? If the text assumes a vendor assessment, a deliberation-heavy scope, or any other specific session shape, generalize it.

## Post-Change Consistency Audit (PCCA)

After any spec or protocol change, perform an FFR for the affected sections, then check every `.md` file in the repo (excluding `sessions/`) for inconsistencies with the changes. This includes but is not limited to: the framework spec, cowork protocol, deliberation protocol, all templates, all other `.md` files in `cowork/`, sync-manifest, OD drafting protocol, `docs/` (walkthroughs, architecture guide, examples), and `README.md`. Report what needs updating, then either apply the fixes directly or add them to the current plan.

## The pool-agent Tool

`cowork/tools/pool-agent.py` provides offline semantic search using all-MiniLM-L6-v2 (quantized ONNX). The model file (`model.onnx`, ~22MB) lives at `cowork/tools/pool-agent/models/` and is gitignored — it is downloaded and quantized automatically via the `setup-model` command.

**Runtime dependencies:** `numpy`, `pyyaml`, `onnxruntime`
**Setup-model dependencies (one-time):** `tokenizers`, `huggingface-hub`, `onnx`

```bash
# Install runtime dependencies
pip3 install numpy pyyaml onnxruntime

# First-time setup: download and quantize the embedding model
# (requires additional packages: tokenizers, huggingface-hub, onnx)
pip3 install tokenizers huggingface-hub onnx
python3 cowork/tools/pool-agent.py setup-model

# Build a vector store from a pool YAML
python3 cowork/tools/pool-agent.py build --pool reference-pool.yaml --articles ./sources/ --store ./pool-store/

# Index a single large document by section headings
python3 cowork/tools/pool-agent.py index-doc --doc spec.md --store ./spec-store/ --heading-level 2

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

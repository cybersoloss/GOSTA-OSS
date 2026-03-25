# GOSTA-Cowork Protocol v3.8

> **Status:** Specification stable. Tier 0 validated. Tier 1 implementation next.

Run the GOSTA framework with session-based AI (Claude Cowork or Claude Code) as orchestrator/executor.

## Quick Start

### New Session (Interactive — Recommended)

1. Open Claude Code or Cowork
2. Say: "Read cowork/startup.md and start a new session."
3. The AI will ask you questions, then scaffold, copy, and bootstrap automatically

### New Session (Manual Template)

1. **Copy and fill:** `cowork/session-launcher-template.md` — replace all `{{PLACEHOLDER}}` values
2. **Paste** the filled prompt into a fresh Cowork or Code session
3. The AI will scaffold `sessions/[name]/`, copy templates, load context, and begin Phase 0

### New Session (Manual — Cowork mode)

1. Create session folder: `mkdir -p sessions/my-session/{domain-models,reference,signals,health-reports,decisions,deliverables,session-logs}`
2. Copy templates: `cp cowork/templates/* sessions/my-session/`
3. Copy protocol: `cp cowork/gosta-cowork-protocol.md sessions/my-session/`
4. Open Claude Cowork, paste `00-BOOTSTRAP.md` and `gosta-cowork-protocol.md`
5. Say: "Bootstrap this session. Here's the scope: [describe what you're doing]"

### New Session (Manual — Code mode)

1. Create session folder: `mkdir -p sessions/my-session/{domain-models,reference,signals,health-reports,decisions,deliverables,session-logs}`
2. Copy templates: `cp cowork/templates/* sessions/my-session/`
3. Copy protocol + directive: `cp cowork/gosta-cowork-protocol.md cowork/CLAUDE.md sessions/my-session/`
4. Open Claude Code in the session directory
5. Say: "Bootstrap this session. Read the protocol and templates."

**Note:** `sessions/` (at repo root) is the standard location for new scopes. Legacy scopes remain in `experiments/`.

## What's in the Box

```
cowork/
├── CLAUDE.md                          ← Claude Code directive (copy to session)
├── gosta-cowork-protocol.md           ← The protocol (v3.8)
├── startup.md                         ← Interactive bootstrap (recommended)
├── session-launcher-template.md       ← Manual template bootstrap (alternative)
├── README.md                          ← This file
├── simulation-protocol-prompt.md      ← Structured simulation runner (v3.0)
├── sync-manifest.md                   ← Framework-to-Protocol derivation map
├── protocol-assessment-prompt.md      ← Six-dimension protocol assessment tool
└── templates/
    ├── 00-BOOTSTRAP.md                ← Session continuity file
    ├── operating-document.md          ← OD template (5-layer hierarchy)
    ├── scope-definition.md            ← What/why/constraints
    ├── domain-model.md                ← Domain model template
    ├── session-log.md                 ← Per-session record
    ├── learnings.md                   ← Structural memory
    ├── gosta-framework-feedback.md    ← Framework improvement log
    ├── decision-entry.md              ← Governor decision format
    ├── health-report.md               ← Health computation output
    └── signal-entry.md                ← Signal recording format
```

## What Changed from v2.2

- **Sessions directory:** Standard location changed from `experiments/` to `sessions/` (legacy scopes remain in `experiments/`)
- **Session launcher template:** New recommended bootstrap method with `{{PLACEHOLDER}}` syntax
- **Protocol v2.4:** Aligned with GOSTA — deliberation integration (§7.5 three-tier escalation, §18.5 multi-agent parallelism), analytical scope support, analytical guardrails, domain model replacement protocol, guardrail evaluation timing
- **CLAUDE.md:** Updated to reference v2.4, sessions/ language

## Protocol Reference

| Section | What It Covers |
|---|---|
| §1-2 | Actors, scope types |
| §3 | File structure + domain model authoring |
| §4 | OD format + staleness triggers + guardrail architecture |
| §5 | Session protocol (lifecycle, types, phase gates, retrospective) |
| §6 | Signal format |
| §7 | Health computation (tactic, strategy, scoring, dependencies) |
| §8 | Decision recording |
| §9 | Context management (bootstrap, session logs, structural memory) |
| §10 | Framework feedback mechanism |
| §11 | Graduation stages |
| §12 | Quality checks |
| §13 | Closing a scope |
| §14 | Parallelism rules |
| §15 | Claude Code mode specifics |

## Framework Reference

- **GOSTA** — Agentic Execution Architecture (`GOSTA-agentic-execution-architecture.md` at repo root)
- **GOSTA-Cowork Protocol** — This directory
- **Deliberation Protocol** — `cowork/deliberation-protocol.md`
- **OD Drafting Protocol** — `cowork/od-drafting-protocol.md`
- **Sync Manifest** — `cowork/sync-manifest.md` — Maps every Framework-to-Protocol derivation point. Consult after any Framework edit to identify which protocol sections need review.

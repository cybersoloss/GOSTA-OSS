# 00-BOOTSTRAP: Vendor-Product Continuity Assessment

**Session Type:** Finite — analytical assessment with deliverable
**Template Version:** 2.0 (Talk-2 aligned)
**Status:** Template — replace [Target Vendor] / [Target Product] placeholders before executing

---

## What This Session Does

Assesses whether continued dependency on a specific vendor's product represents material third-party risk. Produces a six-signal viability assessment structured around three observable categories:

1. **Business Model Signals** — Is the vendor structurally viable? (Signals 1-3)
2. **Contractual Position** — Are you protected if they fail? (Signals 4-5)
3. **Dependency Exposure** — How much operational risk do you carry? (Signal 6)

Plus **leading indicators** (governance quality, talent trajectory, adaptation capacity) that predict viability deterioration before the six signals manifest.

This session is aligned 100% with the analytical framework from "Breach Risk Is Scored. Survival Risk Is Not." — the six signals, three categories, and action-oriented risk determination structure match exactly.

---

## Before You Start

1. **Replace placeholders:** Search for `[Target Vendor]` and `[Target Product]` across all session files and replace with your assessment target.
2. **Review domain models:** The 8 domain models in `domain-models/` are vendor-type-agnostic. If your target is not a SaaS vendor, see the adaptation guidance in README.md.
3. **Review hypotheses:** The 8 hypotheses in `session-config/hypotheses.md` encode Talk-2's specific claims. Adjust or add hypotheses based on what you already know about your target vendor.

---

## Context Loading Order

When entering or re-entering this session, load files in this order:

| Order | File | Purpose |
|---|---|---|
| 1 | `00-BOOTSTRAP.md` (this file) | Session orientation |
| 2 | `session-config/operating-document.md` | Goal, AFC, guardrails, six-signal framework, objectives, strategies, tactics |
| 3 | `session-config/constraints.md` | Hard/soft constraints and scope exclusions |
| 4 | `session-config/hypotheses.md` | 8 testable hypotheses mapping Talk-2 claims |
| 5 | `session-config/deliberation-config.md` | 4 agents, signal coverage map, tension requirements |
| 6-13 | `domain-models/*.md` | 8 domain models (load all before evidence collection) |

After evidence collection (Phase 1), also load:
- Evidence manifest (generated during Phase 1)
- Signal-tagged evidence items

---

## Session Phases

| Phase | What Happens | Exit Criteria |
|---|---|---|
| **1. Evidence Collection** | Parallel dispatch across 8 domains. Evidence tagged by tier and signal relevance. | ≥15 Tier 1/2 items; all 6 signals covered; directional balance check passed |
| **2. Six-Signal Deliberation** | 4-agent deliberation (3 rounds + synthesis). Each agent covers assigned signals. | All 6 signals scored at vendor + product levels; tension map produced |
| **3. Risk Synthesis** | Coordinator synthesizes. Leading indicators confirm/contradict. Governor reviews. | Governor accepts deliverable (max 3 revision cycles) |

---

## Domain Models (8)

| Code | Domain | Talk-2 Signal Coverage | Agent |
|---|---|---|---|
| ECON-1 | Economic Health | Signals 1, 3 | Agent A |
| DISP-1 | Competitive Displacement | Signals 2, 3 | Agent A |
| ADAPT-1 | Adaptation Capacity | Leading indicator | Agent B |
| SAAS-1 | SaaS Structural Viability | Signal 1 | Agent B |
| STICK-1 | Structural Stickiness | Signal 6 | Agent C |
| REG-1 | Regulatory Entrenchment | Signals 4, 5 | Agent C |
| GOV-1 | Governance & Strategic Coherence | Leading indicator | Agent D |
| TAL-1 | Talent & Workforce | Leading indicator | Agent D |

---

## Deliberation Agents

Default: one agent per domain model (8 agents + coordinator). Each agent operates independently with maximum isolation.

| Agent | Domain | Signal Category |
|---|---|---|
| ECON-1 | Financial & Business Health | Business Model Signals (1, 3) |
| DISP-1 | Competitive Displacement | Business Model Signal (2) |
| ADAPT-1 | Adaptation Capacity | Leading indicator |
| SAAS-1 | SaaS Structural Viability | Business Model Signal (1) |
| STICK-1 | Structural Stickiness | Dependency Exposure (6) |
| REG-1 | Regulatory Entrenchment | Contractual Position (4, 5) |
| GOV-1 | Governance & Strategic Coherence | Leading indicator |
| TAL-1 | Talent & Workforce | Leading indicator |
| COORD-1 | — (Coordinator) | Synthesis across all signals |

Optional 4-agent pairing is documented in `session-config/deliberation-config.md`.

---

## Quality Progression Demonstration

The `outputs/` directory contains four output levels showing how each layer of AI architecture improves assessment quality when applied to a generic vendor assessment:

- `level1-generic-prompt.md` — Generic AI prompt, no context
- `level2-extended-reasoning.md` — Extended reasoning (thinking mode), no context
- `level3-domain-knowledge.md` — Single prompt + 8 domain model files
- `level4-deliberation-assessment.md` — Full GOSTA multi-agent deliberation

These are supplementary — they demonstrate why the full session approach matters. Your session produces a Level 4+ assessment.

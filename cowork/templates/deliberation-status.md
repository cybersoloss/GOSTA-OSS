# Deliberation Status — DELIB-[NNN]
**Updated:** [timestamp — overwrite after every round]
**Trigger:** [what initiated this deliberation — e.g., "strategy review cadence", "Governor request", "kill decision on TAC-3"]
**Scope:** [scope-name] | **Items Under Deliberation:** [what agents are evaluating]

## Round Progress
- **Current Round:** [N of max M]
- **Status:** [in_progress | converged | stalled | governor_review | terminated: [reason]]
- **Round started:** [timestamp]

## Agent Status
| Agent | Domain | Status | Confidence | Key Position (1 line) |
|---|---|---|---|---|
| VC-1 | Value Creation | [responding | completed | timed_out | failed | degraded | refused] | [1-10 or —] | [summary or —] |
| MKT-1 | Marketing | | | |
| SLS-1 | Sales | | | |
| VD-1 | Value Delivery | | | |
| NIS2-1 | NIS2 | | | |
| DORA-1 | DORA | | | |
| GDPR-1 | GDPR | | | |
| COORD-1 | Coordinator | [synthesizing | waiting | idle] | — | [synthesis status] |

*Adapt roster to match OD Deliberation section. Remove unused rows.*

## Convergence Tracker
- **Agreement spread:** [N points — distance between most divergent agent positions]
- **Hard disagreements:** [N active — list: Agent-A vs Agent-B on [topic]]
- **New arguments this round:** [yes: [list] | no]
- **Concessions this round:** [yes: [list] | no]

## Termination Assessment
- **Convergence threshold met:** [yes | no — spread is N, threshold is M]
- **New argument gate (Round 4+):** [not yet active | active: [passed — new argument: X | failed — no new arguments]]
- **Stall counter:** [N of 2 consecutive rounds without progress]
- **Projected outcome:** [converging | stable disagreement | stalling]

## Issue Ledger Summary
- **Total issues:** [N]
- **Open:** [N]
- **Narrowed:** [N]
- **Provisionally resolved:** [N]
- **Resolved:** [N]
- **Escalated:** [N]

## Epistemic Tracker
- **Information gaps surfaced:** [N — list: "Agent X flags missing [data]"]
- **Conditional assumptions:** [N — list: "Agent X: recommendation depends on [condition]"]

## Independence Assessment (§14.3.9)
- **Round 1 unanimity:** [yes/no]
- **OD-anchoring indicator:** [low / moderate / high]
- **Convergence probe:** [not triggered | triggered — result: substantive_dissent / weak_dissent / genuine_alignment]
- **Cumulative dissent rate (this scope):** [N hard disagreements across M deliberation cycles = N/M average]

## Artifacts This Deliberation
- [Round 1 position papers: [delivered/pending] — deliberation/DELIB-NNN/round-1/]
- [Round N response papers: [delivered/pending]]
- [Interim assessment: [delivered/pending]]
- [Synthesis report: [delivered/pending]]
- [Verification checklist: [delivered/pending]]
- [Pre-Deliberation Review: [completed/pending] — [N] updates made]

## Governor Actions Needed
- [list — e.g., "Review synthesis report and accept/modify/override/remand" | "Resolve hard disagreement between VC-1 and NIS2-1 on regulatory timing" | "None — deliberation in progress"]

---
*This file is overwrite-only. Updated by the Coordinator after every round and at deliberation close. For historical records, see session-logs/ and deliberation/ artifacts.*

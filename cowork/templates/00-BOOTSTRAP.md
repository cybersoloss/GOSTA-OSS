# BOOTSTRAP — [Session Name]

**Last Updated:** [date] | **Session:** [number] | **Governor:** [name]

## Current State
- **Scope Type:** [finite | ongoing]
- **Current Phase/Cycle:** [where we are]
- **Status:** [active | paused | completed | killed]
- **Graduation Stage:** 1
- **Autonomy Constraints:** [none | degraded-mode: [component] | condition fired: [COND-N] | none active]
- **Deliberation Mode:** [enabled | disabled]
- **Analytical Frame Contract:** [stance] / [output verb] / [failure mode] / [prohibited: X] — or "N/A" if non-analytical scope
- **OD Last Updated:** [date] — [stale? check triggers in protocol §4]

## Context Loading Order
Read these files in this order to understand the current state. For any unfamiliar status value, decision type, or signal type, consult Framework Appendix B (Vocabulary & Taxonomy Index).
1. This file (00-BOOTSTRAP.md)
2. gosta-cowork-protocol.md (if first time in this session)
3. deliberation-protocol.md (if deliberation enabled and first time in this session)
4. operating-document.md
5. [specific domain models needed for current phase]
6. [most recent health report, if any]
7. [most recent deliberation synthesis report, if any] (deliberation mode only)
8. [most recent session log]

## Execution Capabilities (from GOSTA §14.3.6)
What the AI can actually do in this execution environment. The AI checks proposed actions against this list before presenting them to the Governor. Update when tools/platforms are added or removed.
- **Tools/Platforms Available:** [e.g., Cowork file system, web search, no marketing automation, no CRM]
- **Data Sources Governor Can Provide:** [e.g., monthly sales reports (spreadsheet), website analytics (screenshots), verbal market observations]
- **Actions Requiring Governor Execution:** [e.g., sending emails, making phone calls, posting to social media, any action requiring account access the AI doesn't have]
- **Scale Constraints:** [e.g., solo Governor with ~10 hrs/week, audience of ~500, no paid advertising budget]

## Next Reviews Due (ongoing scopes only)
- **Action cycle:** [date — computed from OD review cadence + last action cycle date]
- **Tactic review:** [date]
- **Strategy review:** [date]

## Session-Start Integrity (from GOSTA §7.13.3)
AI fills this section at session start before substantive work:
- **Bootstrap validation:** [pass | fail: [details]]
- **Temporal consistency:** [pass | fail: last session date mismatch]
- **Learnings coherence:** [pass | no contradictions | contradictions: [entities]]
- **Cross-file references:** [pass | orphaned references: [list]]
- **Signal freshness (§7.13.1):** [pass — all active tactics have signals within expected cadence | tactic_gap: TAC-[N] last signal [date], expected cadence [frequency], gap [N days] — Governor: confirm source active? | pipeline_degradation: [M of T] active tactics stale (>50%) — health scores carry staleness warning | pipeline_failure: no new signals for >[N] cycles — autonomous decisions halted, all require Governor approval]
- **Recovery status:** [no active recoveries | recovering: [component] — cycle [N/M] | chronic: [component]]
- **Context utilization:** [~N% after Priority 1-2 loading | shed: [list]]
- **Kill condition evaluability:** `[ROBUST]` [pass — all active tactics have evaluable kill conditions, including completion-based defaults for execution-only tactics | flag: TAC-[N] kill condition references unavailable metric [X] | flag: TAC-[N] execution-only tactic with Kill Condition: N/A — C1 violation, apply default per §8.1.1]
- **Governor capacity alignment:** `[ROBUST]` [declared: N reviews/week | projected this cycle: M reviews | status: sustainable | approaching limit | exceeded — recommend cadence adjustment per §6.1]
- **Cost guardrail status:** `[ROBUST]` [no cost categories declared | cost_exceeded flags: [list] | cost_data_missing flags: [list] | all on_track]
- **OD fingerprint:** `[ROBUST]` [goals: N, objectives: N, strategies: N, tactics (active): N, total allocation sum: X.X, guardrails: N — compared against last session's fingerprint. Match | mismatch: [describe detected changes, surface for Governor confirmation]]

**Pre-Flight Validation Gates (from GOSTA §8.7) — bootstrap-entry boundary:**
- V5 Runtime Imports: import-test for declared tools in orchestrator runtime (e.g., `python3 -c "from tokenizers import Tokenizer; import onnxruntime, yaml, numpy"` for pool-agent). PASS / FAIL.
- V6 Declared Artifact Existence and Population: Layer A — `test -s` per artifact declared in CLAUDE.md / OD / scope as a phase deliverable; list missing-or-empty. Layer B — for templated artifacts, run `grep -c "\[POPULATE:"` (must return 0) plus per-section word-count floor (default 20); list any artifact failing Layer B as template-shaped. **At closeout phase gate, V6 fires explicitly on closeout-mandated artifacts** (learnings.md, session-logs/session-NNN.md, gosta-framework-feedback.md, plus session-specific closeout deliverables).
- V7 Vertical-Fit: concept-coverage on inherited domain models against session concept set. Coverage % per inherited model.
- V8 Subagent Dispatch Capability Smoke-Test (conditional — only if scope/OD/CLAUDE.md declares subagent dispatch): probe subagent writes marker file at session directory + runs no-op tool call; orchestrator independently verifies marker via Read tool. PASS / BLOCK / N/A. On BLOCK, surface the failure trace and chosen mitigation path (reroute-path / extend-sandbox / collapse-to-orchestrator).
- V9 Inheritance Framework-Residue Audit (conditional — only if session inherits artifacts from prior session or example library): extract framework-concept tokens from inheriting session's OD/scope/CLAUDE.md and from each inherited artifact; compute set difference as residue list. PASS (residue list empty) / WARN (N residue tokens surfaced; per-token Governor disposition: update / acknowledge-as-historical / extend-declarations) / N/A (session does not inherit artifacts).

Any FAIL or sub-threshold result blocks Phase 0 closure.

## Tier 0 State Persistence (from GOSTA §7.7, §7.13, §18.2.5)

*At Tier 0, the AI is stateless between sessions. These fields carry cross-session state that would be automatic at Tier 1+. The AI updates them at session end; the next session reads them at session start. Without these fields, retry logic resets every session, recovery tracking is lost, and approaching deadlines are invisible.*

- **Action Retry Counters:** [none active | TAC-[N] action [type]: [N of 3] consecutive failures (§7.7 — at 2 consecutive: escalate to Governor; at 3: emit `agent_degradation` critical) | all retries clear]
- **Kill Deadline Proximity:** [none approaching | TAC-[N]: kill condition deadline [date], [N cycles] remaining, kill_condition_status: [safe | approaching | met] | TAC-[N]: kill timer extended by [N cycles] due to [pause | infrastructure_outage | data_quality_degraded] — new deadline: [date]]
- **Recovery Oscillation Tracking (§7.13.2):** [no recoveries | [component]: recovery cycle [N of M] stability window — if stable at M: VERIFIED, transition to NORMAL | relapse history: [N relapses — at 3: chronic, escalate to Governor per §7.13.2]]
- **Deferred Decisions:** [none | DEC-[N] deferred [date], reason: [data_quality_degraded | Governor unavailable], max deferral: [1 additional cycle — second deferral prohibited per §7.7]]
- **Signal Absence Tracking (§7.7):** [none | TAC-[N] action type [X]: [N] consecutive silent completions — at 2: severity significant; at 3: severity critical, tactic `data_quality: degraded`]

## What Happened Last Session
[2-3 sentence summary]

## What Is Pending
- [Governor decisions needed]
- [Actions in progress]
- [Blockers]

## Next Session Expectations
[What the Governor is likely to ask for next]

## Key Files Modified Last Session
- [file path — what changed]

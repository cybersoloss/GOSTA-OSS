# Framework Feedback Dispositions

**Purpose.** Append-only record of framework feedback entries (from downstream implementations or session-execution observations) that have been verified through `cowork/verification-patterns.md` Patterns 1–15 and assigned a disposition other than PROCEED-and-execute. Entries here name the originating observation, the verifier verdict, the patterns that triggered, the reactivation trigger, and the canonical reference for future re-proposal.

**Discipline.** Entries are append-only by date order. When a deferred FB becomes eligible for reactivation (its trigger fires), append a new entry naming the reactivation with the empirical anchor that satisfied the trigger; the original deferral entry is preserved for audit. When a dropped FB is reconsidered under new framing (Pattern 7 reconsideration discipline), append a new entry naming the reconsideration with what changed.

**Relationship to sync-manifest.** This log carries entries that did NOT produce a framework modification (DEFER or DROP). The sync-manifest carries entries that DID produce a framework modification (PROCEED or SIMPLIFY-to-modification). Together they form the complete framework-feedback trace.

---

## DISP-001 — FB-2: Calendar-Anchored Expected-Event Triggers (DEFER)

**Originating observation.** GOSTA-Watch Service, spinout-discovery Monitor, Cycle 2 deliverable / DEC-3 ratification, 2026-06-03. The Monitor's CAND-1 (Director Personal Liability Dashboard) carried revival conditions gated on an external disposition expected at 2026-08-01. Spec §7.14 environmental signals scope to detection-only ("detects changes that have occurred, not changes that will occur"); `cowork/diff-agent-protocol.md` §3 input contract operationalizes the same detection-only semantic. Neither mechanism supports known-in-advance, calendar-anchored expected external events whose occurrence at a specific future date is the signal worth firing. §7.4 `absence` signals are the closest existing primitive but have different semantics: absence = "expected X did not happen, alert"; arrival-at-trigger = "X scheduled for date Y, fire signal AT date Y so downstream reasoning re-evaluates."

**Cross-reference.** Full FB content at `~/dev/GOSTA-Watch/watches/spinout-discovery/gosta-framework-feedback.md` FB-2. Consolidated in `~/dev/GOSTA-Watch/proposals/gosta-dev-cross-project-briefing.md` §2.

**Verdict (GOSTA-DEV-side framework verifier, 2026-06-03).** DEFER.

**Patterns triggered:**
- **Pattern 4 (problem real?)** — Single Monitor instance; one specific calendar trigger (CAND-1 revival on 2026-08-01). Pattern recurrence inferred from "common in monitoring scopes (regulatory deadlines, contract terms, election dates, fiscal milestones)" — INFERENCE, not OBSERVATION.
- **Pattern 7 (second observed-drop class)** — Single-session demonstration of the gap, without even a Service-level reference implementation. Workaround is Governor-authored DIR-1 mechanism in direction-inbox.md.
- **Pattern 10 (dropped-plan shape match)** — Speculative motivating observation; partial shape-match with prior dropped plans (infrastructure-layer response to a workaround-handled gap).
- **Pattern 11/12 (existing mechanism + convenience-gap)** — DIR-1 already provides the workaround at fragile-but-functional cost; the framework's existing mechanisms collectively handle the case. The proposed §7.4 extension would provide more robust handling but the information itself isn't lost via DIR-1.
- **Pattern 14 (session-need vs framework-need)** — Demand-population currently 1 user / 1 Monitor / 1 future calendar trigger. Per Pattern 14 refinement "reusable-but-unused infrastructure is still over-engineering. Verify the demand-population, not just the mechanism's reusability."

**Why DEFER rather than DROP.** The underlying gap is structurally real: §7.14's detection-only scope and §7.4's absence-semantic both differ from arrival-at-trigger semantic. The three proposed resolution sketches (extend §7.4 absence semantics / new `scheduled_environmental` signal subtype / watch-list entry extension in §7.14.1) are progressively scoped; sketch 1 is the smallest possible intervention. If empirical demand materializes, sketch 1 is the right size for the gap. DROP would close the door on a structurally distinct mechanism; DEFER keeps it open pending evidence.

**Reactivation trigger (any one):**
- A second non-GOSTA-Watch project / Monitor family surfaces the same calendar-anchored expected-event gap with documented friction at session-execution time, OR
- The GOSTA-Watch CAND-1 calendar trigger (2026-08-01) empirically demonstrates DIR-1 fragility — silently-missed trigger with operational consequence (e.g., revival window passes without re-evaluation; Governor confirms the silently-missed case), OR
- A different domain class (regulatory analysis, compliance audit, contract-driven Monitor) authors a Monitor with calendar-anchored dependencies and surfaces the gap with their own workaround.

When the trigger fires, re-propose to GOSTA-DEV with the empirical anchor. The re-proposal should arrive proposal-shaped (not plan-shaped per Pattern 15) and should specify which of the three resolution sketches the empirical observations support. GOSTA-DEV re-verifies under Patterns 1–15 at re-proposal time.

**Until trigger fires.** GOSTA-Watch continues using DIR-1 as session-level mechanism. No framework files modified.

---

## DISP-002 — FB-5: OD Authoring Discipline Gates (OA-1..5) (DEFER)

**Originating observation.** GOSTA-Watch Service, EP-004 ratification, 2026-06-03. Three runs of a Monitor family produced identical multi-item Cycle 1 deliverables with identical verdicts. Root-cause analysis: the Monitor's Goal sentence accepted 4 candidate-origin classes (one source-delta-driven; one external-signal-driven; one combinatorial-synthesis; one Governor-hypothesis-driven); the implementing Strategy covered only the first origin; the OD-drafting protocol did not catch the narrowing at drafting time; autonomous-handoff inheritance propagated the narrowing through descendant Monitor authorings without re-evaluation. Six specific protocol gaps identified (1-5 at `cowork/od-drafting-protocol.md`; 6 at GOSTA spec §6.4). Reference implementation at `~/dev/GOSTA-Watch/od-authoring-conventions.md` v1 (OA-1 Goal Decomposition Gate + OA-2 Goal Claim × Strategy Coverage Matrix + OA-3 Tactic Hypothesis Audit + OA-4 Cascade Trace + OA-5 Drift Detection at Strategy Review), ratified at EP-004 with sim-corrected scope (6 findings applied).

**Cross-reference.** Full FB content at `~/dev/GOSTA-Watch/watches/spinout-fresh-cbp-2026-06/gosta-framework-feedback.md` FB-5. Consolidated in `~/dev/GOSTA-Watch/proposals/gosta-dev-cross-project-briefing.md` §2.

**Verdict (GOSTA-DEV-side framework verifier, 2026-06-03).** DEFER.

**Patterns triggered:**
- **Pattern 5 (right intervention level)** — The empirical 3-run failure mode is specifically caught by OA-2 (Coverage Matrix) + OA-3 (Tactic Hypothesis Audit). OA-1 is upstream prep that makes OA-2 mechanical. OA-4 (Cascade Trace) is audit infrastructure that catches different failure mode (broken layer transitions); no empirical observation of broken cascade in the 3-run dataset. OA-5 (Drift at Strategy Review) operates at different lifecycle stage and addresses a different failure mode (Goal-Strategy drift over time); no empirical observation in the 3-run dataset (no Strategy Review yet executed under EP-004 reference implementation). OA-4 and OA-5 each warrant independent empirical anchor before framework promotion.
- **Pattern 7 (second observed-drop class)** — Reference implementation BUILT 2026-06-03 but UNEXERCISED. Session B re-authoring under EP-004 reference implementation is pending Governor disposition; first empirical exercise of OA-1..5 in operational mode has not yet occurred.
- **Pattern 9 (foundation challenge)** — At framework-promotion scope, the foundation challenge is: does this generalize beyond GOSTA-Watch? Currently 1 implementation; FB-5 itself self-mitigates by proposing empirical-validation path (≥1 documented OA-catch per ≥4 Monitor authorings; cross-Monitor-family generalization signal as stronger anchor). The self-mitigation is honest but the validation has not yet occurred.
- **Pattern 10 (dropped-plan shape match)** — OA-1, OA-2, OA-3, OA-4 are OD-time forcing functions. Prior dropped plans of this shape: Plan #28 (framework-template promotion), Plan #32 (single-session demonstration → framework default), Plan #36 (per-phase scaffolding → framework template) — all involved OD-time forcing functions over concerns the framework's existing mechanisms cover via other channels. "Promotion-of-pattern disguised as gap-fill" anti-pattern (Pattern 7 anti-pattern ii) shape-matches FB-5's Service-level → framework-level promotion path.
- **Pattern 14 (session-need vs framework-need)** — Demand-population currently 1 user, 1 Monitor family, 0 validated re-authorings. The pattern IS framework-general in principle (OD drafting failure modes recur across implementations), but the demand-population evidence does not yet support framework modification cost.

**Why DEFER rather than DROP.** The underlying failure mode is empirically real (3-run same-candidates output is observable), and the proposed solution architecture (OA-1..5) is structurally sound. FB-5 self-mitigates Pattern 7 risk by proposing the empirical-validation path explicitly. DROP would discard the structurally sound proposal entirely; DEFER keeps it open pending the validation evidence FB-5 itself proposed.

**Specific scope reductions noted for future re-proposal (when trigger fires).** If empirical validation supports re-proposal:
- OA-1+OA-2+OA-3 is the cohesive cluster directly caught by the empirical anchor. Re-proposal should lead with these three.
- OA-4 (Cascade Trace) is OD-authoring-time audit infrastructure parallel to spec §8.7 V3 Decision Spine Consistency (which runs at Phase 1 entry); empirical anchor needed independently before promoting.
- OA-5 (Drift at Strategy Review) operates at different lifecycle stage; empirical anchor at Strategy Review needed independently. Could be promoted as separate FB at re-proposal time.

**Reactivation triggers (combine OR):**
- Session B re-authoring under EP-004 reference implementation completes successfully with documented OA-catches (≥1 per OA-1..3 across the re-authoring) AND the re-authoring produces different output than the original 3-run baseline (demonstrates the discipline catches the specific failure mode it claims), AND
- Cross-Monitor-family generalization signal: ≥1 non-spinout-discovery Monitor family authored under EP-004 reference implementation, surfaces material OA-2 catch.
- OR: Independent project (non-GOSTA-Watch) surfaces same failure mode and authors similar discipline gates at Service level.

When the trigger fires, re-propose to GOSTA-DEV with the empirical anchor. The re-proposal should arrive proposal-shaped, should lead with the OA-1..3 cluster (the cohesive set with strongest empirical anchor), and should treat OA-4 and OA-5 as separate empirical sub-cases requiring their own anchor evidence. GOSTA-DEV re-verifies under Patterns 1–15 at re-proposal time, with particular attention to Pattern 14's demand-population question now that the validation period has elapsed.

**Until trigger fires.** GOSTA-Watch continues using `od-authoring-conventions.md` at Service level. No framework files modified. `cowork/od-drafting-protocol.md` and `GOSTA-agentic-execution-architecture.md` §6.4 remain at their pre-FB-5 state.

---

## How to use this log

**Reading.** When evaluating a new FB or framework-change proposal, scan this log for shape-match. If the new proposal matches a prior DROP or DEFER shape, reference the relevant DISP-N entry in the new proposal's verification — name what changed that justifies different verdict (per Pattern 7 reconsideration discipline).

**Appending.** When a future GOSTA-DEV session receives an FB with DEFER or DROP verdict, append a new DISP-N entry to this log naming the originating observation, the verdict, the patterns triggered, and (for DEFER) the reactivation trigger. Keep entries terse and pattern-cited; the verifier-pattern walk is the load-bearing reasoning.

**Disposition transitions.** When a deferred FB's reactivation trigger fires and the re-proposal lands at PROCEED or SIMPLIFY-to-modification, the resulting framework change is recorded in `sync-manifest.md` (the modification record) AND a new entry appended here naming the disposition transition (DEFER → PROCEED) with the empirical anchor that satisfied the trigger. The original DISP-N entry is preserved for audit.

---

## Index

| DISP | Date | FB / Source | Verdict | Status |
|---|---|---|---|---|
| DISP-001 | 2026-06-03 | GOSTA-Watch FB-2 (calendar-anchored expected-event triggers) | DEFER | Awaiting reactivation trigger |
| DISP-002 | 2026-06-03 | GOSTA-Watch FB-5 (OD authoring discipline gates OA-1..5) | DEFER | Awaiting empirical-validation path completion (Session B re-authoring or cross-Monitor-family signal) |

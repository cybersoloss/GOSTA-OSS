# Verification Patterns for Framework Changes

**Purpose.** Codifies the verify-before-apply discipline that emerged from a sequence of framework-change executions. Each pattern is generic across session types and rule-edit types. Apply these patterns when drafting, verifying, or post-change auditing any framework rule, hook, template, or mechanical check.

**Audience.** The orchestrator (or human Governor) preparing to execute a framework change derived from session-execution observations.

**Origin.** Patterns surfaced empirically across multiple plan executions — drafts that initially looked sound revealed defects under verification (misdiagnosed motivating concerns, over-engineered fixes, leaked session-private content, duplication of existing mechanisms). Each pattern names a class of failure mode the verification step is designed to catch.

**This document is a living record.** When new failure modes surface from future plan executions, append patterns here. Patterns deprecated by changes elsewhere in the framework should be marked `[DEPRECATED]` rather than deleted, with the deprecating change cited.

---

## Pattern 1 — Verify Before Apply

**Statement.** Every framework change must pass an explicit verification step before any file edit is performed. The verification produces either an "execute" verdict (proceed with edits, optionally with corrections), a "simplify" verdict (apply a smaller-scope variant), or a "drop" verdict (the change should not be executed).

**Mechanism.** Read the actual files the change would touch. Replay the originating observation against the proposed fix. Challenge the proposed fix's assumptions. Test session-agnosticism. Check for duplication of existing framework mechanisms.

**Outcomes observed.** Of plans verified under this discipline, a substantial fraction terminated in either drop or simplify rather than execute — preventing wasted execution rounds.

**Failure mode this catches.** Drafting confidence inflating under attention pressure, leading to execution of fixes that don't actually fix anything or that fix the wrong problem.

---

## Pattern 2 — Replay the Originating Observation

**Statement.** Take the specific session-execution observation that motivated the proposed change. Walk through what the proposed fix would have done under that exact scenario. If the fix wouldn't have prevented the original observation, the fix is misdirected.

**Mechanism.** Read the relevant session log entries, signal records, deliverable text, or audit output. Mentally execute the proposed fix's mechanism against the observed scenario. Trace whether the new rule would have changed the outcome.

**Failure mode this catches.** Fixes that operate at the wrong layer (e.g., OD-time forcing function for a problem rooted in deliberation-time discipline; deliverable-annotation for a problem in evidence-collection methodology).

**Concrete example.** A proposed fix targeting "agent must classify each below-threshold case at audit time" was verified by replaying the observed audit output. The replay revealed that the existing rule already required "logged rationale" for auto-resolution — and agents had been ignoring that rule. The proposed tightening would likely be ignored too. Verdict: simplify to remove the auto-resolve shortcut entirely (structural fix), not add more procedural rules.

---

## Pattern 3 — Test Session-Agnosticism by Enumeration

**Statement.** Per the change-authoring principle, every framework rule must be domain-agnostic. Test the proposed rule against four to five diverse session types: regulatory analysis, hiring rubric, vendor evaluation, product roadmap, discovery sweep, compliance audit. If the rule "feels awkward" when applied to any of those, the rule is not generic.

**Mechanism.** For each test session type, ask: "What does this rule do here? Does the vocabulary fit? Does the mechanism apply? Is the failure mode it catches relevant?" If the answer requires significant translation or the rule loses bite, the proposed fix is session-specific and needs reframing.

**Failure mode this catches.** Rules that bake in session-type assumptions (e.g., "buyer signal floor" — feature-evaluation-specific; "ADOPT-band" — specific to feature-evaluation; "G-N" guardrail labels — session-specific).

**Concrete example.** A proposed "buyer signal floor for buyer-receptivity discovery sessions" was tested against regulatory-analysis (regulator-acceptance), hiring (candidate-fit), vendor-eval (vendor-delivery). Initial framing was feature-evaluation-specific. Reframed to a generic abstraction: "claims about Party-X reception require Party-X-sourced or Party-X-about evidence." The reframed version generalized cleanly.

---

## Pattern 4 — Challenge Whether the Problem Is Real

**Statement.** Don't only refine the fix; challenge the premise. Ask: "What would happen if we did NOTHING? Is the observed pattern actually a defect, or is it the framework correctly producing a transparent edge-case output?" Some observed patterns are misdiagnosed (category error in shortfall analysis) or speculative (fix proposed for a hypothetical defect not actually observed).

**Mechanism.** Re-examine the source observation. Verify that the framework rule was actually violated, not that the observation was incorrectly characterized. Check whether the framework already has a mechanism that handles the case correctly. Distinguish "the framework failed" from "the framework correctly handled an edge case the observer didn't anticipate." **Apply this challenge equally to inherited categorizations from prior session analyses, not only to new observations** — accepting an earlier session's root-cause framing without empirical re-verification against current evidence is itself a Pattern 4 failure. Inherited categorizations may have been correctly named for the session that produced them but may not transfer to other sessions; verify before propagating.

**Failure mode this catches.** Drafting fixes for problems that don't exist. Premature pattern-matching from one session's friction to a framework-rule deficiency when the framework rule was correctly applied.

**Concrete example.** A proposed fix targeted "candidate self-acknowledged absence-of-trigger-condition shipped without consistent verdict-band treatment." Verification re-examined the trigger condition's operational definition: it was a conjunctive AND condition. The candidate's self-acknowledgment satisfied only one of the two terms. The trigger correctly did NOT fire. The motivating shortfall conflated two distinct concepts. Verdict: drop.

---

## Pattern 5 — Find the Right Intervention Level

**Statement.** For any observed defect, multiple intervention levels exist: structural (remove the failure path), mechanical (hook-enforced check), procedural (rule that requires discipline), annotation-only (transparency at consumption point), drop (accept the defect as scope-bounded). Prefer structural fixes when discipline is the failure surface. Prefer annotation-only when reader-cognition is the failure surface. Avoid procedural rules that depend on discipline that's already been observed to fail.

**Mechanism.** Enumerate the intervention options. For each, ask: "Does this fix the failure mode at the source, or does it add machinery to compensate for the failure mode?" Source-fixes beat compensation. Surface-only fixes beat invisible enforcement.

**Failure mode this catches.** Adding rules on top of rules that have already failed. Building enforcement infrastructure to police a discipline that the next attention-pressure cycle will bypass anyway.

**Concrete example.** A proposed fix had three intervention candidates: F1 (remove auto-resolve shortcut entirely), F2 (require structured classification before auto-resolve), F3 (F2 + mechanical hook + reviewer audit). F1 was structurally simplest — eliminated the failure path. F2 and F3 added procedural and enforcement layers on top of a discipline that had already been observed to fail. Verdict: F1 (structural) preferred.

---

## Pattern 6 — Look for Orphan References and Propagation (PCCA)

**Statement.** After any framework rule change, perform Post-Change Consistency Audit: grep for references to what was changed across all framework files (excluding session directories). Identify any documentation surfaces that mention the changed concept and verify they're still accurate. Apply propagation edits where needed.

**Mechanism.** Use grep with multiple search patterns covering the changed concept's name, related terminology, and cross-reference sites. Check the spec, the cowork-protocol, the deliberation-protocol, all templates, the protocol-assessment-prompt, README, docs/. Propagate the change to any surface that referenced the prior state.

**Failure mode this catches.** Stale references in documentation that confuse future readers or that the framework's own audit checklists rely on. Documentation drift.

---

## Pattern 7 — Honest Drop Recommendation

**Statement.** When verification surfaces that the motivating concern was misdiagnosed, speculative, or already handled by existing framework mechanisms, the honest verdict is to drop the proposed change rather than execute a watered-down version. Recording the drop as `[CORRECTED-IN-LATER-TURN]` annotation in the originating shortfall log preserves the verification finding for future reference.

**Mechanism.** When verification produces a drop verdict, annotate the source shortfall with the verification finding. Update any plan-tracking document. Do not execute partial-credit edits to feel productive.

**Failure mode this catches.** Sunk-cost continuation on plans that verification has invalidated. Producing rule-text that adds complexity without addressing real defects.

**Pattern observed across drops.** Plans that propose OD-time forcing functions over speculative or vaguely-defined concerns have been particularly likely to drop after verification. The verification typically reveals that the framework already provides the underlying mechanism through other channels (existing parameters, existing scope-bound declarations, existing audit machinery).

---

## Pattern 8 — Strip Session-Private Content from Generic Framework

**Statement.** Framework files (anything outside `sessions/`) must not contain session names, session-specific shortfall IDs, candidate IDs, domain-model abbreviations, product names, vendor names, or other content tied to a specific session execution. The pre-commit hook enforces this; authoring discipline catches it earlier.

**Mechanism.** Before any commit to framework files, scan the new content for: session-name patterns (e.g., `*-discovery-v*`, `*-roadmap-v*`), shortfall ID patterns (e.g., `SF-N`), candidate ID patterns (e.g., `AL-N`, `RL-N`), domain-model abbreviation patterns (e.g., 2-4-letter abbreviations followed by `-N`), product/company names that appear in session reference materials. Replace specific tokens with abstract placeholders or describe the structural pattern without naming the session.

**Failure mode this catches.** Domain-genericity violations that leak private/commercial references into the public framework. The pre-commit hook BLOCKs these — surfacing them at commit time costs a remediation cycle. Catching during authoring saves the cycle.

**Concrete example.** Sync-manifest entries documenting plan derivations initially included session-name tokens (matching session-name patterns) and candidate-ID tokens (matching candidate-list-item patterns) inherited from the drafting session's vocabulary. The pre-commit hook BLOCKed the commit with the offending lines highlighted. Remediation: replace specific tokens with abstract descriptions ("originating session," "HIGH-band single-cluster defect," "unresolved verdict-band split"). Re-staged commit passed.

**Recursive lesson.** This pattern's documentation initially contained the exact tokens it warned against (in a "concrete example" section that quoted real session/candidate identifiers verbatim). The pre-commit hook BLOCKed the commit. The fix was to abstract the example itself — describing the violation pattern without instantiating it. Lesson: even teaching examples in framework files must use placeholders, not specific session/candidate tokens. The hook is the last line of defense; authoring discipline must catch this earlier.

---

## Pattern 9 — Multi-Pass Verification for High-Stakes Changes

**Statement.** For framework changes that affect multiple files or introduce new mechanical infrastructure, single-pass verification is insufficient. Use a three-pass pattern: first pass drafts the change, second pass refines based on initial verification feedback, third pass actually challenges the foundations (the most aggressive challenge).

**Mechanism.** First pass: produce the draft. Second pass: read the relevant framework files, replay the originating observation, propose corrections. Third pass: question whether the problem is real, whether the fix is at the right level, whether existing mechanisms handle the underlying need. If the third pass surfaces unresolved concerns, prefer drop or simplify over execute.

**Failure mode this catches.** Verification fatigue producing approval-by-default after one or two passes. The third pass is where motivated reasoning gets tested.

---

## Pattern 10 — Compare to Dropped Plans for Shape Match

**Statement.** When verifying a new proposed change, compare its shape to the shape of plans that were dropped after prior verifications. If the new change is in the same shape as a dropped plan (same intervention level, same type of motivating observation, same proposed mechanism class), the verification should be especially aggressive about challenging the premise.

**Mechanism.** Maintain a list of dropped plans with their drop-reasons. For each new proposed change, ask: "Does this match any dropped plan's shape? OD-time forcing function? Speculative motivating observation? Duplication of existing mechanisms?" If yes, the verification needs to specifically address why this case differs.

**Pattern observed in shapes that tend to drop.**
- OD-time forcing functions over concerns the framework's existing mechanisms already cover
- Speculative motivating observations (no empirical defect, only "might happen" reasoning)
- Procedural rules layered on top of disciplines that have already been observed to fail
- Category errors where the motivating shortfall conflated two distinct concepts
- Infrastructure-layer responses to convenience-gaps (where information exists in alternate canonical artifacts and the proposal centralizes rather than captures-new-information)

---

## Pattern 11 — Existing-Mechanism Check Before Adding Infrastructure

**Statement.** Before proposing new framework infrastructure (hooks, templates, mechanical checks, new protocol sections), verify whether existing framework artifacts already capture the underlying information or behavior through alternate channels. If they do, the gap may be a convenience-issue rather than a correctness-issue, and the proposed infrastructure may be over-engineering.

**Mechanism.** Enumerate the existing framework surfaces that touch the concern. Check whether the underlying need is met through any existing surface (signals, decisions log, debug logs, deliverables, evidence manifest, OD declarations, etc.). If yes, ask: "Does the proposed new infrastructure provide value beyond reformatting the existing information?"

**Failure mode this catches.** Building parallel infrastructure when existing infrastructure already covers the need. Adding new audit dimensions that duplicate existing audit dimensions in different vocabulary.

---

## Pattern 12 — Distinguish Convenience-Gap from Correctness-Gap

**Statement.** Documentation or coverage gaps come in two shapes. A correctness-gap means information is lost — no surface in the framework captures the relevant data. A convenience-gap means the information exists but is distributed across multiple surfaces and harder to consume from a single canonical location. Correctness-gaps warrant infrastructure-level fixes. Convenience-gaps warrant clarification or accept-as-design rather than infrastructure.

**Mechanism.** When evaluating an observed gap, ask: "Is the information missing entirely, or is it in alternate locations that the consumer doesn't know to consult?" If the latter, the fix may be documentation-of-the-canonical-locations, not new-infrastructure-to-centralize-them.

**Failure mode this catches.** Building unified-narrative artifacts when distributed artifacts already carry the canonical information. Forcing single-source-of-truth at high infrastructure cost when multi-source-with-cross-references would suffice.

---

## How to Use This Document

Before drafting a framework change:
1. Read the originating shortfall or observation
2. Apply Pattern 4 — challenge whether the problem is real
3. Apply Pattern 11 — check whether existing framework mechanisms already cover the need
4. If both pass, draft the change

After drafting:
1. Apply Pattern 2 — replay the originating observation against the draft
2. Apply Pattern 3 — test session-agnosticism by enumeration
3. Apply Pattern 5 — verify the intervention level is right (structural over procedural where possible)
4. Apply Pattern 10 — compare to dropped plans for shape match
5. Apply Pattern 12 — classify the gap as correctness or convenience
6. If high-stakes, apply Pattern 9 — three-pass verification

Before committing:
1. Apply Pattern 6 — PCCA across framework files
2. Apply Pattern 8 — strip session-private content

Producing a verdict:
1. Honest verdict per Pattern 7 — execute, simplify, or drop
2. Record drop verdicts as `[CORRECTED-IN-LATER-TURN]` annotations in the source shortfall log

---

*This document is itself subject to verification. If applying these patterns to a new plan surfaces a failure mode not captured here, append a new pattern. Patterns that prove redundant or superseded by framework changes should be marked `[DEPRECATED]` with the deprecating change cited.*

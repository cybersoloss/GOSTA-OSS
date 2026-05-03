# Decision Verification Patterns

**Purpose.** Codifies the verify-before-apply discipline that emerged from a sequence of framework-change executions and broader decision-evaluation work. Two sections below: **Section A — Universal Decision Patterns** apply to any decision or recommendation evaluation (framework changes, plan assessment, session-internal decisions, recommendation review); **Section B — Framework-Change-Specific Patterns** apply specifically when the decision being evaluated is a change to framework files (spec, protocols, templates, hooks).

**Audience.** The orchestrator (or human Governor) evaluating any decision, recommendation, or proposed change. Both sections apply when the decision is a framework change; only Section A applies when the decision is something else (e.g., evaluating a session-internal disposition recommendation, choosing between strategy options, selecting an intervention approach for a non-framework problem).

**Origin.** Patterns surfaced empirically across multiple plan executions — drafts that initially looked sound revealed defects under verification (misdiagnosed motivating concerns, over-engineered fixes, leaked session-private content, duplication of existing mechanisms, sunk-cost bias from premature plan-drafting). Each pattern names a class of failure mode the verification step is designed to catch.

**This document is a living record.** When new failure modes surface from future plan executions or decision evaluations, append patterns here in the appropriate section. Patterns deprecated by changes elsewhere in the framework should be marked `[DEPRECATED]` rather than deleted, with the deprecating change cited. Pattern numbers are stable for cross-reference even if section grouping changes.

**Applicability summary:**

| Decision type being evaluated | Section A patterns | Section B patterns |
|---|---|---|
| Framework change (spec / protocol / template / hook edit) | All apply | All apply |
| Framework-change plan assessment (evaluating a proposed plan) | All apply | All apply |
| Session-internal decision (in-session disposition, deliberation choice) | All apply | Skip |
| Recommendation evaluation (assessing a recommendation received) | All apply | Skip |
| Strategy / intervention selection for non-framework problem | All apply | Skip |

---

# Section A — Universal Decision Patterns

The following patterns apply to any decision or recommendation evaluation, regardless of whether the decision involves framework files.

---

## Pattern 1 — Verify Before Apply

**Statement.** Every change must pass an explicit verification step before any file edit is performed. The verification produces either an "execute" verdict (proceed with edits, optionally with corrections), a "simplify" verdict (apply a smaller-scope variant), or a "drop" verdict (the change should not be executed).

**Mechanism.** Read the actual files the change would touch. Replay the originating observation against the proposed fix. Challenge the proposed fix's assumptions. Test session-agnosticism (Section B Pattern 3 — when the decision is a framework change). Check for duplication of existing mechanisms (Pattern 11).

**Outcomes observed.** Of plans verified under this discipline, a substantial fraction terminated in either drop or simplify rather than execute — preventing wasted execution rounds.

**Failure mode this catches.** Drafting confidence inflating under attention pressure, leading to execution of fixes that don't actually fix anything or that fix the wrong problem.

---

## Pattern 2 — Replay the Originating Observation

**Statement.** Take the specific session-execution observation that motivated the proposed change. Walk through what the proposed fix would have done under that exact scenario. If the fix wouldn't have prevented the original observation, the fix is misdirected.

**Mechanism.** Read the relevant session log entries, signal records, deliverable text, or audit output. Mentally execute the proposed fix's mechanism against the observed scenario. Trace whether the new rule would have changed the outcome.

**Failure mode this catches.** Fixes that operate at the wrong layer (e.g., OD-time forcing function for a problem rooted in deliberation-time discipline; deliverable-annotation for a problem in evidence-collection methodology).

**Concrete example.** A proposed fix targeting "agent must classify each below-threshold case at audit time" was verified by replaying the observed audit output. The replay revealed that the existing rule already required "logged rationale" for auto-resolution — and agents had been ignoring that rule. The proposed tightening would likely be ignored too. Verdict: simplify to remove the auto-resolve shortcut entirely (structural fix), not add more procedural rules.

---

## Pattern 4 — Challenge Whether the Problem Is Real

**Statement.** Don't only refine the fix; challenge the premise. Ask: "What would happen if we did NOTHING? Is the observed pattern actually a defect, or is it the framework correctly producing a transparent edge-case output?" Some observed patterns are misdiagnosed (category error in shortfall analysis) or speculative (fix proposed for a hypothetical defect not actually observed).

**Mechanism.** Re-examine the source observation. Verify that the rule was actually violated, not that the observation was incorrectly characterized. Check whether the framework already has a mechanism that handles the case correctly. Distinguish "the framework failed" from "the framework correctly handled an edge case the observer didn't anticipate." **Apply this challenge equally to inherited categorizations from prior session analyses, not only to new observations** — accepting an earlier session's root-cause framing without empirical re-verification against current evidence is itself a Pattern 4 failure. Inherited categorizations may have been correctly named for the session that produced them but may not transfer to other sessions; verify before propagating.

**Failure mode this catches.** Drafting fixes for problems that don't exist. Premature pattern-matching from one session's friction to a rule deficiency when the rule was correctly applied.

**Concrete example.** A proposed fix targeted "candidate self-acknowledged absence-of-trigger-condition shipped without consistent verdict-band treatment." Verification re-examined the trigger condition's operational definition: it was a conjunctive AND condition. The candidate's self-acknowledgment satisfied only one of the two terms. The trigger correctly did NOT fire. The motivating shortfall conflated two distinct concepts. Verdict: drop.

---

## Pattern 5 — Find the Right Intervention Level

**Statement.** For any observed defect, multiple intervention levels exist: structural (remove the failure path), mechanical (hook-enforced check), procedural (rule that requires discipline), annotation-only (transparency at consumption point), drop (accept the defect as scope-bounded). Prefer structural fixes when discipline is the failure surface. Prefer annotation-only when reader-cognition is the failure surface. Avoid procedural rules that depend on discipline that's already been observed to fail.

**Mechanism.** Enumerate the intervention options. For each, ask: "Does this fix the failure mode at the source, or does it add machinery to compensate for the failure mode?" Source-fixes beat compensation. Surface-only fixes beat invisible enforcement.

**Failure mode this catches.** Adding rules on top of rules that have already failed. Building enforcement infrastructure to police a discipline that the next attention-pressure cycle will bypass anyway.

**Concrete example.** A proposed fix had three intervention candidates: F1 (remove auto-resolve shortcut entirely), F2 (require structured classification before auto-resolve), F3 (F2 + mechanical hook + reviewer audit). F1 was structurally simplest — eliminated the failure path. F2 and F3 added procedural and enforcement layers on top of a discipline that had already been observed to fail. Verdict: F1 (structural) preferred.

---

## Pattern 7 — Honest Drop Recommendation

**Statement.** When verification surfaces that the motivating concern was misdiagnosed, speculative, or already handled by existing mechanisms, the honest verdict is to drop the proposed change rather than execute a watered-down version. Recording the drop as `[CORRECTED-IN-LATER-TURN]` annotation in the originating shortfall log preserves the verification finding for future reference.

**Mechanism.** When verification produces a drop verdict, annotate the source shortfall with the verification finding. Update any plan-tracking document. Do not execute partial-credit edits to feel productive.

**Reconsideration of dropped plans.** If a previously-dropped plan is being reconsidered (because new framing, new evidence, or a different intervention angle has emerged), the verification must explicitly identify what changed that justifies un-dropping. Don't reverse a drop verdict silently — name what the prior drop missed and why the new framing addresses it. The reconsideration verification produces a fresh verdict (apply / simplify / drop-again) under the new framing. This discipline prevents flip-flopping and maintains audit-trail clarity for why drops are reversed.

**Failure mode this catches.** Sunk-cost continuation on plans that verification has invalidated. Producing rule-text that adds complexity without addressing real defects.

**Pattern observed across drops.** Plans that propose OD-time forcing functions over speculative or vaguely-defined concerns have been particularly likely to drop after verification. The verification typically reveals that the framework already provides the underlying mechanism through other channels (existing parameters, existing scope-bound declarations, existing audit machinery).

---

## Pattern 9 — Multi-Pass Verification for High-Stakes Changes

**Statement.** For changes that affect multiple files or introduce new mechanical infrastructure, single-pass verification is insufficient. Use a three-pass pattern: first pass drafts the change, second pass refines based on initial verification feedback, third pass actually challenges the foundations (the most aggressive challenge).

**Mechanism.** First pass: produce the draft. Second pass: read the relevant files, replay the originating observation, propose corrections. Third pass: question whether the problem is real, whether the fix is at the right level, whether existing mechanisms handle the underlying need. If the third pass surfaces unresolved concerns, prefer drop or simplify over execute.

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

**Statement.** Before proposing new infrastructure (hooks, templates, mechanical checks, new protocol sections, new artifacts of any kind), verify whether existing artifacts already capture the underlying information or behavior through alternate channels. If they do, the gap may be a convenience-issue rather than a correctness-issue, and the proposed infrastructure may be over-engineering. This applies to framework infrastructure specifically and to any infrastructure proposal more broadly.

**Mechanism.** Enumerate the existing surfaces (framework or otherwise) that touch the concern. Check whether the underlying need is met through any existing surface (signals, decisions log, debug logs, deliverables, evidence manifest, OD declarations, scope-definition fields, custom CLAUDE.md directives, etc.). If yes, ask: "Does the proposed new infrastructure provide value beyond reformatting the existing information?"

**Failure mode this catches.** Building parallel infrastructure when existing infrastructure already covers the need. Adding new audit dimensions that duplicate existing audit dimensions in different vocabulary.

---

## Pattern 12 — Distinguish Convenience-Gap from Correctness-Gap

**Statement.** Documentation or coverage gaps come in two shapes. A correctness-gap means information is lost — no surface captures the relevant data. A convenience-gap means the information exists but is distributed across multiple surfaces and harder to consume from a single canonical location. Correctness-gaps warrant infrastructure-level fixes. Convenience-gaps warrant clarification or accept-as-design rather than infrastructure.

**Mechanism.** When evaluating an observed gap, ask: "Is the information missing entirely, or is it in alternate locations that the consumer doesn't know to consult?" If the latter, the fix may be documentation-of-the-canonical-locations, not new-infrastructure-to-centralize-them.

**Failure mode this catches.** Building unified-narrative artifacts when distributed artifacts already carry the canonical information. Forcing single-source-of-truth at high infrastructure cost when multi-source-with-cross-references would suffice.

---

## Pattern 13 — Resolve Scope Extension Explicitly

**Statement.** When a proposed change extends an existing rule's, policy's, or mechanism's scope to a new artifact class, surface, or boundary that the rule did not previously cover, the verification must explicitly justify the extension. Don't frame scope extension as mere "propagation" without answering: "Why should this rule apply at the new surface? What changes if it doesn't?"

**Mechanism.** Identify whether the proposed change is (a) propagation of an existing rule to a surface where the rule already implicitly applied (consistency-only fix), or (b) extension of the rule's scope to a surface where the rule did not previously apply (semantic-scope fix). Propagation requires no semantic justification beyond consistency. Extension requires explicit answer to three questions: (i) what is the rule's current scope; (ii) why does the new surface warrant inclusion; (iii) what failure mode does the extension catch that the current scope doesn't.

**Failure mode this catches.** Implicit scope creep — adding rules to new surfaces under "propagation" framing without explicit justification, leading to over-application of rules in cases where they don't fit OR under-application in cases where the original scoping was an oversight that should be corrected.

**Distinction from Pattern 11.** Pattern 11 asks "does the framework already have this mechanism?" Pattern 13 asks "is this extending an existing mechanism's scope to a surface it didn't previously cover?" The two are complementary: Pattern 11 catches duplication; Pattern 13 catches semantic scope extension that should be explicit rather than implicit.

**Concrete example.** A proposed plan adds a rule from one artifact class to another (e.g., from deliverable artifacts to synthesis-report artifacts). Verification asks: was synthesis report previously in this rule's scope? If no, the change is extension, not propagation. Justification required: why does synthesis report warrant the rule (e.g., consumed by Governor, propagates to deliverables, frame-drift at synthesis cascades downstream)? If justification is sound, extension is warranted; if not, the proposed change is over-applying the rule.

---

## Pattern 15 — Verify Before Plan, Not After

**Statement.** Verification gates plan-drafting, not just file-editing. Pattern 1 covers verify-before-apply (no file edits without verification). Pattern 15 extends this earlier in the cycle: when a user expresses an intent ("go with X"), the response should verify X first, then draft the plan only if verification passes. Drafting first creates a structured plan whose mere existence biases subsequent verification toward approval — the sunk-cost bias of "I just wrote this; surely it's worth executing."

**Mechanism.** When a user says "go with X," "create a plan for X," or otherwise expresses intent to proceed with a proposed change, treat that as a request for verification + plan-or-decline, not as approval to draft a plan. Order:
1. Run verification patterns against X (the proposal, before any plan structure exists)
2. If verification passes: draft the plan
3. If verification surfaces concerns: report them and recommend drop, simplify, or proceed-with-caveats; do not draft a plan that pretends the concerns don't exist

The discipline is to keep verification UPSTREAM of plan-drafting, not downstream. Plans are cheap to draft but cognitively expensive to discard once drafted; verification before drafting prevents that wasted cognitive investment.

**Failure mode this catches.** Forward-progress bias at the planning stage. The user's stated intent ("go with X") is interpreted as authorization rather than as a question requiring verification. The orchestrator drafts a plan to demonstrate productivity, then verification (if it happens at all) becomes a check on the plan rather than on the underlying proposal. The plan's structure makes its weaknesses harder to see and harder to walk back from.

**Relationship to Pattern 1.** Pattern 1 says verify before APPLY. Pattern 15 says verify before PLAN. The distinction matters because plans are themselves a kind of cognitive commitment that biases later verification, even when no files have been edited. A drafted plan creates anchoring: the verifier looks for ways to make the plan work rather than looking at whether the underlying proposal should exist.

**Distinction from Pattern 9.** Pattern 9 says high-stakes changes warrant multiple verification passes. Pattern 15 says the FIRST pass should occur before plan-drafting, not after. Pattern 9 is about pass-count; Pattern 15 is about pass-ordering relative to plan-drafting. They're complementary: Pattern 15 says the first pass is upstream; Pattern 9 says additional passes follow downstream as the change progresses toward execution.

**Concrete example.** A user, after a verification round dropped Option 2 of a proposal, said "let's go with F5 instead." The orchestrator immediately drafted a structured plan for F5 with steps, time estimates, and decision points. Only when subsequently asked to verify the F5 plan did the verification reveal F5 had similar pattern-failures to the dropped Option 2 — but the existing plan structure made the verification feel like "fixing the plan" rather than "questioning whether F5 should exist." The discipline failure: F5 should have been verified before the plan was drafted, not after. Adding Pattern 15 names this failure mode.

**Recursive lesson.** This pattern was itself surfaced in a session where the orchestrator twice drafted plans before verifying their underlying proposals (once for Option 2, once for F5). Both required subsequent verification rounds that surfaced material concerns that should have been caught upstream. The cost: extra verification passes; the avoidable waste: plan-drafting effort for proposals that didn't survive verification.

---

# Section B — Framework-Change-Specific Patterns

The following patterns apply specifically when the decision being evaluated is a change to framework files (spec, protocols, templates, hooks). Skip these when evaluating session-internal decisions, recommendations, or non-framework strategy choices.

---

## Pattern 3 — Test Session-Agnosticism by Enumeration

**Statement.** Per the change-authoring principle, every framework rule must be domain-agnostic. Test the proposed rule against four to five diverse session types: regulatory analysis, hiring rubric, vendor evaluation, product roadmap, discovery sweep, compliance audit. If the rule "feels awkward" when applied to any of those, the rule is not generic.

**Mechanism.** For each test session type, ask: "What does this rule do here? Does the vocabulary fit? Does the mechanism apply? Is the failure mode it catches relevant?" If the answer requires significant translation or the rule loses bite, the proposed fix is session-specific and needs reframing.

**Failure mode this catches.** Rules that bake in session-type assumptions (e.g., "buyer signal floor" — feature-evaluation-specific; "ADOPT-band" — specific to feature-evaluation; "G-N" guardrail labels — session-specific).

**Concrete example.** A proposed "buyer signal floor for buyer-receptivity discovery sessions" was tested against regulatory-analysis (regulator-acceptance), hiring (candidate-fit), vendor-eval (vendor-delivery). Initial framing was feature-evaluation-specific. Reframed to a generic abstraction: "claims about Party-X reception require Party-X-sourced or Party-X-about evidence." The reframed version generalized cleanly.

---

## Pattern 6 — Look for Orphan References and Propagation (PCCA)

**Statement.** After any framework rule change, perform Post-Change Consistency Audit: grep for references to what was changed across all framework files (excluding session directories). Identify any documentation surfaces that mention the changed concept and verify they're still accurate. Apply propagation edits where needed.

**Mechanism.** Use grep with multiple search patterns covering the changed concept's name, related terminology, and cross-reference sites. Check the spec, the cowork-protocol, the deliberation-protocol, all templates, the protocol-assessment-prompt, README, docs/. Propagate the change to any surface that referenced the prior state.

**Failure mode this catches.** Stale references in documentation that confuse future readers or that the framework's own audit checklists rely on. Documentation drift.

**Relationship to PCCA directive.** This pattern operationalizes the **Documentation PCCA mode** of the project-level PCCA directive (see project root `CLAUDE.md` § Post-Change Consistency Audit). The PCCA directive defines two modes — Documentation PCCA (the orphan-reference grep this pattern describes) and Code PCCA (smoke-tests for executable framework files). When a framework change touches executable code (`cowork/hooks/*.sh`, `cowork/tools/*.py`), Pattern 6 is necessary but not sufficient — Code PCCA mode (smoke-test) catches behavioral bugs that pure grep misses.

---

## Pattern 8 — Strip Session-Private Content from Generic Framework

**Statement.** Framework files (anything outside `sessions/`) must not contain session names, session-specific shortfall IDs, candidate IDs, domain-model abbreviations, product names, vendor names, or other content tied to a specific session execution. The pre-commit hook enforces this; authoring discipline catches it earlier.

**Mechanism.** Before any commit to framework files, scan the new content for: session-name patterns (e.g., `*-discovery-v*`, `*-roadmap-v*`), shortfall ID patterns (e.g., `SF-N`), candidate ID patterns (e.g., `AL-N`, `RL-N`), domain-model abbreviation patterns (e.g., 2-4-letter abbreviations followed by `-N`), product/company names that appear in session reference materials. Replace specific tokens with abstract placeholders or describe the structural pattern without naming the session.

**Failure mode this catches.** Domain-genericity violations that leak private/commercial references into the public framework. The pre-commit hook BLOCKs these — surfacing them at commit time costs a remediation cycle. Catching during authoring saves the cycle.

**Concrete example.** Sync-manifest entries documenting plan derivations initially included session-name tokens (matching session-name patterns) and candidate-ID tokens (matching candidate-list-item patterns) inherited from the drafting session's vocabulary. The pre-commit hook BLOCKed the commit with the offending lines highlighted. Remediation: replace specific tokens with abstract descriptions ("originating session," "HIGH-band single-cluster defect," "unresolved verdict-band split"). Re-staged commit passed.

**Recursive lesson.** This pattern's documentation initially contained the exact tokens it warned against (in a "concrete example" section that quoted real session/candidate identifiers verbatim). The pre-commit hook BLOCKed the commit. The fix was to abstract the example itself — describing the violation pattern without instantiating it. Lesson: even teaching examples in framework files must use placeholders, not specific session/candidate tokens. The hook is the last line of defense; authoring discipline must catch this earlier.

---

## Pattern 14 — Distinguish Session-Need from Framework-Need

**Statement.** A user's preference about a specific session execution is not automatically a framework-level need. Before proposing a framework change in response to a session-specific preference, distinguish between (a) every session that runs this framework would benefit from the change, and (b) only THIS session's circumstances make the change valuable. If the answer is (b), the right intervention is per-session arrangement, not framework modification. If the answer is (a), framework modification is warranted but cost-benefit must still favor it (Pattern 12).

**Mechanism.** When a session-execution observation motivates a proposed framework change, ask three questions:
1. Is the underlying need general (every session has it) or session-specific (only some sessions have it)?
2. If session-specific, can it be addressed by per-session arrangement (scope declarations, custom CLAUDE.md directive, supporting policy file) without modifying framework artifacts?
3. If only framework modification suffices, is the framework modification worth its cost given how many future sessions would actually use it?

If question 2 has an affirmative answer, prefer per-session arrangement. Framework changes carry PCCA cost, increase framework surface area, and add cognitive load for all future Governors reading the framework — those costs are justified only when the need is actually framework-general.

**Critical refinement: distinguish "mechanism reusable" from "demand population large."** A framework change can produce a mechanism that is technically reusable (any future session could opt-in to use it) while the realistic demand population remains very small (only one user under specific circumstances will actually invoke it). Reusable-but-unused infrastructure is still over-engineering. Verify the demand-population, not just the mechanism's reusability.

**Failure mode this catches.** Treating a single user's session-specific preference as if it were a universal framework requirement. This produces over-engineered framework changes that add complexity without benefiting most future sessions. The user's per-session preference is real and addressable — but not at framework level.

**Distinction from Pattern 4.** Pattern 4 challenges whether the observed problem is real. Pattern 14 accepts the problem is real but challenges whether it's a framework problem versus a per-session problem. The two are complementary: Pattern 4 catches non-problems; Pattern 14 catches real problems mis-classified as framework-level.

**Distinction from Pattern 12.** Pattern 12 distinguishes correctness-gap from convenience-gap as a property of the gap itself. Pattern 14 distinguishes framework-level need from session-level need as a property of the audience. A change can be a convenience-gap that's still framework-level (Plans #17 and #19 both qualify); a change can also be a correctness-fix that's session-level (e.g., a custom CLAUDE.md directive correcting a domain-specific framing for one session). The two patterns are independent dimensions.

**Concrete example.** A proposed framework change extended a disposition policy mechanism into the bootstrap process so a session could run truly unattended. Verification asked: does every session need autonomous bootstrap, or does this session need it under THIS user's current circumstances? Answer: only some sessions need it; many Governors actively want bootstrap interactivity for high-stakes setup review. Per-session arrangement (pre-staging scope-definition + accepting the bounded interactive period) addresses the need without framework modification. Verdict: drop the framework change; recommend per-session arrangement.

---

# How to Use This Document

**Choose the applicable subset.** If the decision being evaluated is a framework change (or a plan that would produce one), apply both Section A and Section B patterns. For other decisions (session-internal disposition, recommendation evaluation, non-framework strategy), apply only Section A.

**Before any plan-drafting (per Pattern 15 — verification gates plan-drafting, not just file-editing):**
1. Read the originating shortfall, observation, or user-stated intent
2. Apply Pattern 4 — challenge whether the problem is real
3. Apply Pattern 11 — check whether existing mechanisms already cover the need
4. Apply Pattern 12 — classify the gap as correctness or convenience
5. (Framework changes only) Apply Pattern 14 — distinguish session-need from framework-need
6. Only if all pass: draft the change

**After drafting:**
1. Apply Pattern 2 — replay the originating observation against the draft
2. (Framework changes only) Apply Pattern 3 — test session-agnosticism by enumeration
3. Apply Pattern 5 — verify the intervention level is right (structural over procedural where possible)
4. Apply Pattern 10 — compare to dropped plans for shape match
5. Apply Pattern 13 — if scope-extending an existing rule, justify the extension explicitly
6. If high-stakes, apply Pattern 9 — three-pass verification (third pass is the foundation challenge — most aggressive)

**Before committing (framework changes only):**
1. Apply Pattern 6 — PCCA across framework files (Documentation PCCA + Code PCCA per project CLAUDE.md)
2. Apply Pattern 8 — strip session-private content

**Producing a verdict:**
1. Honest verdict per Pattern 7 — execute, simplify, or drop
2. Record drop verdicts as `[CORRECTED-IN-LATER-TURN]` annotations in the source shortfall log
3. If reconsidering a previously-dropped plan, explicitly identify what changed (Pattern 7 reconsideration discipline)

---

*This document is itself subject to verification. If applying these patterns to a new decision surfaces a failure mode not captured here, append a new pattern in the appropriate section. Patterns that prove redundant or superseded by other changes should be marked `[DEPRECATED]` with the deprecating change cited. Pattern numbers are stable for cross-reference.*

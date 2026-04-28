# GOSTA OD Drafting Protocol v0.1

**Purpose:** Defines how AI agents draft high-quality Operating Documents from vague or incomplete Governor inputs. The protocol ensures the AI has current, comprehensive framework knowledge before drafting, uses domain agents to decompose the problem space, and produces an OD that the Governor understands and the downstream execution system can operate on.

**Problem this solves:** The OD is the single most important artifact in GOSTA — everything downstream inherits its assumptions, decomposition choices, and structural decisions. Yet the framework currently expects the Governor to author the OD (or the AI to draft it at bootstrap with no structured process). This creates two failure modes: (1) a competent Governor produces a structurally valid OD that reflects their biases rather than optimal decomposition, and (2) an AI drafts an OD without current framework knowledge, producing something that passes structural validation but doesn't leverage the framework's full capabilities.

**When to use this protocol:**
- **Always recommended** when the Governor's inputs are vague, incomplete, or expressed as a question rather than a structured brief ("I want to figure out X", "help me plan Y", "what should we do about Z")
- **Strongly recommended** for analytical scopes with 5+ domains, or any scope expecting deliberation
- **Optional** when the Governor provides a fully structured OD draft that only needs validation (use the cowork protocol's quality gate directly)
- **Required** for multi-tier operations where OD complexity exceeds what a single author can reliably produce

**Relationship to other documents:**
- **Framework:** The specification. Defines layers, tiers, complexity markers, scope types, guardrails, domain models, graduation, autonomy.
- **Cowork Protocol:** How a single agent operates sessions. This protocol produces the OD that the cowork protocol then executes against. The OD Drafting Protocol sits BEFORE the cowork protocol's bootstrap session — it replaces the "Create OD" step in Bootstrap Session (§5.2) with a structured, multi-agent process.
- **Deliberation Protocol:** How multiple agents coordinate through structured rounds. This protocol uses deliberation mechanics for OD decomposition but is not itself a deliberation — it borrows the round structure and synthesis pattern.
- **Sync-Manifest:** Tracks framework-to-protocol dependencies. This protocol will have its own derivation entries.

**Implementation-agnostic:** Like the Deliberation Protocol, this protocol defines mechanics, not implementation. The Governor Commission, Decomposition Proposals, and Draft OD are logical artifacts that can be files, conversation turns, or structured data.

---

## 1. The OD Architect Role

**Definition:** The OD Architect is the AI agent (or agent ensemble) that transforms Governor intent into a structurally sound, framework-compliant Operating Document. It is a distinct role from the Governor, the AI executor, and the Coordinator.

**What the OD Architect does:**
- Reads the framework, cowork protocol, and deliberation protocol to understand current capabilities and requirements
- Translates vague Governor inputs into structured GOSTA elements
- Determines optimal scope type, tier, complexity level, and domain model selection
- Proposes the five-layer decomposition (Goal → Objectives → Strategies → Tactics → Actions)
- Configures deliberation parameters if applicable
- Produces an OD that passes the quality gate and serves downstream execution

**What the OD Architect does NOT do:**
- Make strategic decisions — it proposes, the Governor decides
- Override Governor intent — even if a different goal would be "better"
- Skip framework ingestion — reading is a hard gate, not a recommendation
- Produce an OD the Governor doesn't understand — comprehension is a gate

**Reading perspective:** The OD Architect reads the framework from three angles simultaneously:

1. **Governor perspective** (from §0.3 Governor reading path): What strategic choices exist? What authority boundaries are defined? What guardrail structures does the Governor need to set? What review cadences are appropriate? This perspective tells the OD Architect what to *ask* the Governor and what Governor decisions the OD must capture.

2. **AI executor perspective** (from §0.3 AI system reading path): What does downstream execution require from the OD? What fields does the quality gate check? What does health computation expect? What does deliberation need in the OD's Deliberation section? What does the signal architecture need from attribution chains? This perspective tells the OD Architect what the OD must contain to *function*.

3. **Framework architect perspective** (structural sections §0.3, §2, §3-5, §6): What tiers exist and what does each require? What complexity markers ([CORE]/[ROBUST]/[ADVANCED]) apply to this scope? What scope types (finite/ongoing) fit? What independence levels and deliberation modes are available? This perspective tells the OD Architect what the *optimal configuration* is for this specific commission.

The OD Architect is not pretending to be the Governor or the AI executor. It is a structural architect who understands both what the Governor wants and what the system needs, and bridges the gap through informed decomposition.

---

## 2. Framework Ingestion Phase (Mandatory)

**This phase is a hard gate.** OD drafting MUST NOT begin until all mandatory reading steps are completed. The agent MUST record which documents were read and their version numbers in the Ingestion Log (§2.2).

### 2.1 Mandatory Reading Sequence

The OD Architect reads the following documents in order. Each step builds on the prior step's context.

**Step 1 — Reading Guide (§0.3).** Read the framework's §0.3 (Reading Guide — Document Map, Implementation Tiers, Selection Guide). This orients the agent to where everything lives, what the tier structure is, and what complexity markers mean. Read BOTH the Governor reading path and the AI system reading path — the OD Architect needs both perspectives.

**Step 2 — Architecture Overview (§2).** Read §2.1 (Five Layers), §2.2 (Dual Reading), §2.3 (Control Loop), §2.4 (Layer Transformation Model). This establishes the structural vocabulary for decomposition. The Layer Transformation Model (§2.4) is particularly important — it defines the boundaries between layers, which is exactly what the OD Architect must get right.

**Step 3 — Layer Definitions (§3-5).** Read §3 (Goal, Objective definitions, structural rules, litmus tests), §4 (Strategy, Tactic definitions, kill/pivot/persevere, A/B testing), §5 (Guardrail architecture — hard/soft, severity, inheritance, calibration). Focus on the litmus tests and structural rules — these are the constraints the decomposition must satisfy.

**Step 4 — Cowork Protocol (full).** Read the current cowork protocol. This defines:
- OD format and template (§4)
- Field complexity determination ([CORE]/[ROBUST]/[ADVANCED] — §4)
- Quality gate criteria (§5.2)
- Session lifecycle that the OD must support (§5.1)
- Signal architecture the OD must feed (§6)
- Guardrail architecture the OD must configure (§4.1)
- Scoring protocol (§7.6)
- Phase gate enforcement (§5.1)

**Step 5 — Deliberation Protocol (full, if scope may involve deliberation).** Read if: Governor mentions multiple perspectives, domains, stakeholders, or trade-offs; or scope complexity suggests 3+ domain models; or Governor explicitly requests multi-agent analysis. This tells the OD Architect how to configure the Deliberation section, agent roster, cadence parameters, convergence thresholds, and min rounds.

**Step 6 — OD Template.** Read `cowork/templates/operating-document.md`. This is the structural target — the OD Architect must produce output that conforms to this template.

**Step 7 — Sycophancy awareness (from Framework §14.3.9).** When drafting an OD for a scope that will use deliberation mode, the OD Architect should be aware that the OD's strategy rationale becomes shared context for domain agents and can serve as an anchoring source for sycophancy. The OD Architect should: (a) write strategy rationale that states the Governor's reasoning without prescribing the conclusion, (b) avoid language that signals the "expected" outcome of deliberation, (c) configure the kill proximity alert threshold in Failure Resilience Thresholds.

**Step 8 — Sync-Manifest.** Read `cowork/sync-manifest.md`. This catches recent protocol changes that may not be reflected in the main framework document yet. Check the "Last Verified" column for any rows showing a version newer than the framework version read in Step 1.

**Step 9 — Existing Domain Models (if available).** If the scope has pre-existing domain models in `domain-models/`, read them. They constrain and inform the decomposition.

### 2.2 Ingestion Log

After completing the reading sequence, the OD Architect produces an Ingestion Log before any drafting begins:

```markdown
## Ingestion Log
- **Framework version:** [version read]
- **Cowork Protocol version:** [version read]
- **Deliberation Protocol version:** [version read, or "N/A — not applicable to this scope"]
- **OD Template version:** [date of template file]
- **Sync-Manifest version:** [version line from manifest]
- **Domain models read:** [list, or "none available"]
- **Recent changes noted:** [any sync-manifest entries with version newer than framework, or "none"]
- **Tier determination:** [Tier 0/1/2/3 — based on Governor's environment]
- **Complexity determination:** [CORE/ROBUST/ADVANCED — based on scope characteristics identified so far]
- **Scope type determination:** [finite/ongoing — preliminary, may be revised after Commission Clarification]
```

This log is included in the final OD as a metadata section (or as a separate `od-drafting-log.md` file in the session directory). It makes the ingestion auditable — the Governor or any reviewer can verify the OD Architect had current knowledge.

### 2.3 When to Re-Ingest

The OD Architect must re-read the framework and protocols (full ingestion sequence) when:
- Starting a new OD drafting session after a break (context may have been lost)
- The Governor reports that protocols have been updated since the last ingestion
- The sync-manifest shows changes not reflected in the prior Ingestion Log
- A quality gate failure traces to a structural issue that the current framework addresses

Re-ingestion is not required within a single continuous drafting session, but the OD Architect should re-read specific sections if a decomposition choice depends on a section it read early and may have compressed in memory.

---

## 3. Governor Commission

The Governor Commission is the input to the OD Drafting Protocol. It captures the Governor's intent — which may be vague, incomplete, contradictory, or expressed as a question. The protocol is designed to work with minimal input and elicit structure through the drafting process.

### 3.1 Commission Template (Governor-facing)

The OD Architect presents this template to the Governor. Every field is optional except the Problem Statement. The more the Governor provides, the fewer clarification rounds are needed — but the protocol works with just a problem statement.

```markdown
## Governor Commission

### Problem Statement (required)
[What you want to accomplish, analyze, decide, or build. Can be a question, a goal, a challenge, or a vague aspiration. Examples: "Figure out our AI regulation strategy", "Should we build or buy a compliance platform?", "I want to grow our newsletter to 10K subscribers", "What's the best approach to entering the European market?"]

### Context (optional)
[What you already know. Constraints, prior decisions, resources available, timeline, organizational context. The more you share, the better the OD decomposition.]

### Domains / Perspectives (optional)
[If you already know which perspectives matter — e.g., "legal, technical, financial" or "GDPR, NIS2, DORA". Leave blank if you want the OD Architect to propose domains.]

### Success Criteria (optional)
[How you'll know this worked. Can be vague ("I need a clear recommendation") or precise ("achieve 10K subscribers by Q3 with < €5K spend").]

### Constraints (optional)
[Hard boundaries — budget limits, timeline deadlines, regulatory requirements, ethical boundaries, things you explicitly will NOT do.]

### Autonomy Preferences (optional)
[How much do you want to approve vs. delegate? "I want to approve everything" = Stage 1. "Run with it and show me results" = Stage 3. If unsure, leave blank — the OD Architect will recommend.]

### Prior Work (optional)
[Point to existing files, prior session learnings, domain models from other scopes, or external documents that inform this scope.]

### Hypotheses (optional)
[If you already suspect something — "I think we should prioritize compliance over features", "I believe the European market requires a local partner" — state it. These become testable hypotheses in the OD.]

### Analytical Frame (auto-derived — OD Architect confirms with Governor)
[The OD Architect derives the Analytical Frame Contract (AFC) from the Problem Statement and presents it for confirmation before decomposition begins. This ensures decomposition agents receive the correct analytical frame. Omit for non-analytical scopes.]
```

### 3.2 Commission Clarification

After receiving the commission, the OD Architect performs a structured clarification pass. This is NOT open-ended conversation — it is a targeted elicitation to fill gaps that the decomposition requires.

**Mandatory clarifications** (ask only if the commission doesn't address them):
1. **Scope type:** "Is this a bounded project with a defined end (finite), or an ongoing operation with recurring cycles (ongoing)?" — Required because scope type determines phase structure vs. cycle cadence.
2. **Decision horizon:** "When do you need the output? Days, weeks, months?" — Required because it constrains decomposition depth and tier selection.
3. **Domain ambiguity:** If the Governor's keywords map to multiple possible domain models (per cowork protocol §5.2 keyword disambiguation), present the options: "Your topic touches [A], [B], and [C] as potential analytical perspectives. Which matter most?" Do not silently choose.

**Conditional clarifications** (ask only if relevant):
4. **Multi-stakeholder scope:** If the problem involves multiple stakeholders or perspectives → "Should different perspectives be independently evaluated (deliberation) or sequentially analyzed?"
5. **Prior failures:** If the Governor mentions prior attempts → "What went wrong before? This helps set guardrails and kill conditions."
6. **Governor capacity:** If the scope appears complex → "How much time can you dedicate to reviewing and deciding? This affects how we structure review cadences and autonomy."
7. **Analytical frame (for analytical scopes):** Derive the AFC from the Problem Statement. Present: "Based on your problem statement, the assessor stands alongside [stance], the deliverable will [output verb], and the assessment protects against [failure mode]. The deliverable will NOT be a [prohibited frame]. Is this correct?" If the Governor corrects, re-derive before proceeding to decomposition. Skip for non-analytical scopes.

**Do not ask more than 5 clarification questions.** If the commission is too vague for even basic decomposition after 5 questions, the OD Architect proposes a minimal viable OD (single goal, single objective, 2-3 strategies) and presents it for iteration rather than asking more questions.

**Relationship to Pre-Deliberation Review.** The Governor Commission for OD drafting is architecturally parallel to the Pre-Deliberation Governor Review for deliberation (Deliberation Protocol §2.4). Both prompt the Governor to provide structured input before agent work begins. When an OD Drafting session will also configure deliberation, the Governor Commission may inform the Pre-Deliberation Review checklist.

### 3.3 Structured Input Detection

If the Governor's commission contains analytical connectors ("given that," "assuming," "because"), multiple clauses, or embedded hypotheses, the OD Architect detects the implicit structure:

"I detected the following structure in your commission:
1. **Primary question:** [extracted]
2. **Embedded hypothesis:** [extracted]
3. **Analytical constraints:** [extracted]
Is this correct?"

If confirmed, skip the decomposition proposals (§4) and map directly to OD elements. An informed Governor who has pre-structured their thinking shouldn't be forced through agent decomposition.

---

## 4. Decomposition Phase

This is the core innovation of the protocol: domain agents propose how the problem should be decomposed, rather than the Governor or a single AI doing it alone.

### 4.1 Domain Selection

Based on the commission and any clarifications, the OD Architect:

1. **Proposes domain models.** Identify 3-7 domains relevant to the problem. For each, state: domain name, why it's relevant to this commission, whether a pre-built model exists or needs to be authored. For each pre-built model proposed for reuse, include a recommended adaptation intent (Adapt or Preserve as independent lens) with rationale, following the same criteria as startup.md Group 3. Governor confirms intent per model.

2. **Presents to Governor for approval.** "I propose analyzing this from these N perspectives: [list with one-line rationale each]. Add, remove, or modify?"

3. **Applies domain count bounds** (cowork protocol §3.1 rule 8): 3-5 recommended. If proposing more, state the trade-off.

### 4.2 Decomposition Proposals

Each domain agent produces a Decomposition Proposal — its view of how the OD should be structured from its domain perspective.

**Decomposition Proposal template:**

```markdown
## Decomposition Proposal — [Domain Name] ([Agent ID])

### Proposed Goal
[How this domain frames the overarching goal]

### Proposed Objectives
- **OBJ-[N]:** [Objective from this domain's perspective] | Metric: [what to measure] | Why: [why this objective matters from this domain]

### Proposed Strategies
- **STR-[N]:** [Strategy suggestion] → serves OBJ-[N] | Rationale: [domain-grounded reasoning] | WMBT: [key assumption]

### Proposed Guardrails
- **G-[N]:** [Constraint this domain considers essential] | Severity: [hard/soft] | Evaluation: [mechanical/interpretive] | Why: [domain-grounded justification]

When populating guardrails, classify each as `mechanical` (explicit numeric threshold) or `interpretive` (qualitative judgment required). All guardrails with clear numeric comparisons should be `mechanical`. Default: `interpretive`.

### Decomposition Tensions
[Where this domain's proposed structure conflicts with likely proposals from other domains. This is the highest-value section — it surfaces structural disagreements before they become downstream execution problems.]

### Scope Configuration Recommendations
- Scope type: [finite/ongoing] and why
- Tier recommendation: [0/1/2/3] and why
- Complexity level: [CORE/ROBUST/ADVANCED] and why
- Deliberation: [recommended/not needed] and why
```

**Process:**
1. Each domain agent reads its domain model (if available) and the framework ingestion context
2. Each agent produces a Decomposition Proposal independently (same isolation rules as Deliberation Protocol Round 1)
3. Proposals are collected — no cross-reading between agents at this stage

**Agent count for decomposition:** Use 3-5 agents even if the scope will eventually use more domains. Decomposition doesn't need the full roster — it needs the major structural perspectives. Additional domains can be added when the OD is refined.

### 4.3 Synthesis into Draft OD

The OD Architect (acting as coordinator for this phase) synthesizes the decomposition proposals into a single Draft OD:

1. **Goal synthesis:** If agents propose the same goal with different framings → merge. If they propose different goals → present to Governor as a scope decision ("Your commission could be structured as Goal A or Goal B — which better captures your intent?").

1a. **AFC consistency check (when AFC exists).** After synthesizing the goal, verify that the synthesized goal's framing matches the AFC derived from the Governor Commission (§3.2 step 7). If the synthesis drifted the frame (e.g., the commission said "expose dependency risk" but synthesis produced "evaluate vendor suitability"), correct before proceeding to objective synthesis. Log any correction.

2. **Objective synthesis:** Map proposed objectives across agents. Merge overlapping objectives. Flag complementary objectives (both belong in the OD). Flag competing objectives (Governor must choose or both become strategies under a broader objective).

3. **Strategy synthesis:** Group proposed strategies by which objective they serve. Identify where different domains propose different strategies for the same objective — these are the structural tensions that make the OD analytically rich.

4. **Guardrail synthesis:** Combine all proposed guardrails. Check for contradictions (one domain's essential constraint conflicts with another's proposed strategy). If contradictions are intentional (analytical scope exploring tensions), create an Engineered Contradiction Register entry.

5. **Configuration synthesis:** If agents disagree on scope type, tier, or complexity level, the OD Architect resolves by applying the framework's selection guidance (§0.3 Implementation Tiers) and presents the rationale.

6. **Populate the OD template.** Fill in `cowork/templates/operating-document.md` using the synthesized structure. Apply the field complexity determination from cowork protocol §4: include [CORE] always, include [ROBUST] if deliberation or A/B testing or ≥Independence Level 2, include [ADVANCED] if metric lag or metric prerequisites.

7. **Tournament assessment.** For each tactic that produces a generative deliverable (not data collection, not signal monitoring), the OD Architect evaluates whether tournament execution would add value. The test: "Would structurally different approaches to this deliverable reveal a design principle the Governor should see?" If yes, run the Dimension Elicitation Protocol (spec §4.6): analyze domain model tensions, guardrail pairs, reference pool clusters, and deliverable trade-offs to propose behavior space dimensions. Present proposed dimensions to Governor alongside the Draft OD. If the Governor approves, populate the tournament fields in the tactic specification. If the Governor declines or no meaningful dimensions emerge, use standard single-run execution.

8. **Flag gaps.** Any OD field that couldn't be filled from the commission + decomposition proposals is marked `[GOVERNOR INPUT NEEDED]` with a specific question.

### 4.4 Decomposition Tension Report

Alongside the Draft OD, the OD Architect produces a Decomposition Tension Report:

```markdown
## Decomposition Tension Report

### Structural Tensions
[Where domain agents proposed incompatible decompositions — different goal framings, competing objectives, contradictory guardrails. Each tension includes: which agents disagree, what each proposes, and why the OD Architect resolved it the way it did (or why it's flagged for Governor decision).]

### Configuration Tensions
[Where agents recommended different scope types, tiers, or complexity levels. How resolved.]

### Coverage Gaps
[Domains or perspectives that the commission implies but no agent addressed. Recommendations for additional domain models.]

### Assumptions Made
[Decisions the OD Architect made in the absence of Governor input. Each listed with: what was assumed, what the alternative would be, and how to change it if the Governor disagrees.]
```

---

## 5. Governor Review Gate

The Draft OD is presented to the Governor with the Decomposition Tension Report. This is a hard gate — the OD does not become operational until the Governor passes this gate.

### 5.1 Presentation Format

The OD Architect presents the Draft OD in this order:
1. **One-paragraph summary:** "Here's what I've structured based on your commission: [goal], decomposed into [N] objectives with [N] strategies. The scope is [finite/ongoing] at [Tier X] with [CORE/ROBUST/ADVANCED] complexity."
2. **Key decisions for Governor:** The `[GOVERNOR INPUT NEEDED]` items, presented as specific questions with the OD Architect's recommended answer.
3. **Decomposition Tension Report** (§4.4).
4. **Full Draft OD** — for the Governor to review in detail.

### 5.2 Comprehension Gate

**Why this exists:** The stress-test finding that motivated this protocol includes the risk that a Governor rubber-stamps an agent-drafted OD they don't fully understand. An OD the Governor can't explain is an OD the Governor can't govern.

**Requirement:** Before the OD becomes operational, the Governor must demonstrate comprehension. The OD Architect asks:

"Before we proceed, I need to confirm you understand the structure. For each objective, can you tell me in your own words: (a) why it's included, and (b) what would make you kill it?"

The Governor's answers don't need to match the OD verbatim. They need to show the Governor understands the decomposition logic and the kill conditions. If the Governor can't articulate why an objective exists, that objective should be simplified or removed.

**This is not a test.** It's a collaborative check. If the Governor struggles with an objective, the OD Architect explains the reasoning and asks if it should be restructured. The goal is a Governor who owns the OD's logic, not one who merely approves its text.

### 5.3 Iteration

The Governor may:
- **Approve** the Draft OD as-is → proceeds to quality gate
- **Revise** specific elements → OD Architect incorporates changes and re-presents affected sections
- **Request re-decomposition** of specific areas → returns to §4.2 for targeted decomposition proposals on the flagged areas only (not full re-run)
- **Reject** the structure entirely → returns to §3.2 for additional commission clarification

Maximum 3 full iteration cycles. If the OD isn't approved after 3 cycles, the OD Architect must simplify: reduce to single objective, 2 strategies, minimum viable structure. This prevents infinite refinement loops.

---

## 6. Quality Gate

After Governor approval, the Draft OD passes through the standard quality gates defined in the cowork protocol.

### 6.1 Structural Validation

Run the cowork protocol's OD structural integrity checks (§12.1):
- All required fields populated
- GOSTA hierarchy valid (every strategy traces to an objective, every tactic to a strategy)
- Kill conditions evaluable (C1 invariant)
- Allocation arithmetic correct (C2 invariant)
- Temporal ordering consistent (C3 invariant)
- Entity reference integrity verified (C4 invariant) — every domain model name, agent ID, and cross-reference in OBJ/STR/TAC resolves to a declared entity in the OD's roster, model list, or guardrail table
- Guardrails calibrated above/below baseline (§4.1)
- Guardrail evaluation mode declared: `mechanical` for numeric thresholds, `interpretive` for qualitative constraints (§5.1)

### 6.2 Domain Model Quality Gate

If domain models were created or selected during this process, run the 3-test quality gate (cowork protocol §5.2):
1. Specificity — concept descriptions explain how they apply to this scope. For models with Preserve adaptation intent (startup.md Group 3), evaluate Application Context header only — general-purpose concept descriptions are expected and should not be flagged as specificity failures.
2. Distinctiveness — concepts produce different results than generic analysis
3. Anti-Pattern specificity — anti-patterns go beyond basic critical thinking

Output in severity-graded format: PASS / PASS-WITH-FLAGS / FLAG-FOR-REVIEW with CRITICAL/MATERIAL/INFORMATIONAL classification.

### 6.3 OD-Specific Quality Checks

Additional checks specific to agent-drafted ODs:

1. **Governor intent fidelity:** Does the OD's goal still match the Governor's original Problem Statement? Agent decomposition can drift from the original intent through well-meaning structural improvement.

2. **Over-scoping check:** Count objectives, strategies, tactics. If the total exceeds what the commission's decision horizon and Governor capacity can support, flag: "This OD has [N] objectives and [M] strategies. Given your stated capacity of [X], this may exceed sustainable governance. Consider reducing to [recommended count]."

3. **Tier consistency:** Verify the OD doesn't use [ROBUST] or [ADVANCED] features at a Tier 0 scope without justification. If the OD Architect recommended Tier 0 but populated [ROBUST] fields (e.g., deliberation), confirm the Governor understands the implications.

4. **Decomposition boundary check:** For each strategy, verify it's a strategy (approach logic, reasoning) and not a tactic (specific implementation). For each tactic, verify it's a tactic (testable hypothesis) and not an action (specific task). Use §2.4 Layer Transformation Model as the test.

5. **AFC frame consistency (when AFC exists):** Does every objective's analytical question use the AFC's output verb? Does every strategy's rationale serve the AFC's failure mode? Does every tactic's hypothesis test something relevant to the AFC's stance? Does any deliverable description produce the AFC's prohibited frame? If any section fails, flag as `[FRAME-DRIFT]` and return to Governor for correction before handoff.

### 6.4 Decision-Spine Consistency Check (from GOSTA §8.7 V3)

The Operating Document and the scope-definition file must derive from a single decision spine. At OD authoring time and at every Phase 1 entry, run a cross-document key-set comparison:

- Every `STR-N` declared in the OD has a corresponding row in scope §6 (or equivalent objectives section).
- Every guardrail name referenced in scope appears in the OD's guardrail set.
- Every scope deliverable references an OD strategy ID by exact match.
- Every OD `TAC-N` references a scope strategy or signal.

This is a mechanical key-set comparison, not a strategic-alignment judgment. Run by reading both documents and computing the symmetric difference of named entities.

**Failure mode:** BLOCK at Phase 1 entry on non-empty symmetric difference. Reconcile by extending the OD to match scope OR revising scope to match the OD. Do NOT advance to Phase 1 with drift; the v3-class failure of mid-construction Option-B reconciliation is the empirical pattern V3 exists to prevent.

**Authoring-time check:** When drafting an OD, after each Strategy or Tactic addition, verify the corresponding scope entry exists. Add scope entries before OD entries — scope is upstream.

---

## 7. Handoff to Cowork Protocol

Once the OD passes both Governor review and quality gates:

1. **Write the OD** to `operating-document.md` in the session directory
2. **Write domain models** to `domain-models/` directory
3. **Write the 00-BOOTSTRAP.md** with initial state, context loading order, and the Ingestion Log reference
4. **Write the OD Drafting Log** to `od-drafting-log.md` containing: Governor Commission, Ingestion Log, Decomposition Proposals (all agents), Decomposition Tension Report, Governor Review decisions, Quality Gate results
5. **Transition to cowork protocol:** The session enters the normal cowork protocol flow at the point AFTER Bootstrap Session's "Create OD" step. The OD already exists; the bootstrap session proceeds with domain model ingestion and first execution planning.

The OD Drafting Log is an audit artifact. It makes the OD's provenance transparent — any reviewer can trace why each structural choice was made, what alternatives were considered, and what the Governor decided.

---

## 8. Multi-Tier Considerations

### 8.1 Tier 0 (File-based)

At Tier 0, the OD Architect is the same conversational AI that will execute the session. The ingestion and decomposition happen in conversation. Domain agents run sequentially in the same conversation (single_session_sequential mode from the deliberation protocol).

**Context pressure mitigation:** The full ingestion sequence plus decomposition proposals plus synthesis may consume significant context. To manage this:
- After ingestion, the agent writes the Ingestion Log to a file and summarizes key findings in 5-10 bullets (the file is the record; the summary is the working memory)
- Decomposition proposals are written to files, not held entirely in conversation context
- The OD Architect re-reads the OD template immediately before synthesis (Step 6 in §2.1) to ensure template compliance despite context distance

### 8.2 Tier 1+ (Coded)

At Tier 1+, the OD Architect can be a dedicated agent or pipeline:
- Framework ingestion can be automated (read files, extract key parameters, validate versions)
- Domain agents can run in parallel (true isolation, no contamination risk)
- The synthesis step can include automated structural validation before presenting to the Governor
- The comprehension gate (§5.2) still requires human Governor interaction — this cannot be automated

### 8.3 Multi-Scope Operations

When drafting ODs for scopes that exist within a multi-scope hierarchy (GOSTA §4.3):
- The OD Architect reads the parent scope's OD to understand inherited guardrails and constraints
- The child scope's goal must be traceable to a specific parent-scope strategy or objective
- Guardrails from the parent propagate downward — the OD Architect includes them automatically, marked `[INHERITED from parent-scope]`

---

## 9. Protocol Boundaries

### 9.1 What This Protocol Does NOT Replace

- **Governor authority.** The Governor remains final authority on goals, objectives, strategies, guardrails, and domain model changes. The OD Architect proposes; the Governor decides.
- **Quality gate.** The cowork protocol's structural and domain model quality gates still run. This protocol adds to them, not replaces them.
- **Deliberation protocol.** The decomposition phase uses deliberation-like mechanics (independent agent proposals, coordinator synthesis) but is not a deliberation. There are no rounds of cross-examination. Domain agents propose decomposition structure, not policy positions.

### 9.2 What This Protocol DOES Replace

- **The unstructured "Create OD" step** in the cowork protocol's Bootstrap Session (§5.2). When this protocol is used, that step is replaced entirely.
- **Governor solo authoring** of complex ODs. The Governor provides intent; the system provides structure.

---

## 10. Failure Modes and Mitigations

### 10.1 Agent Over-Scoping

**Risk:** Domain agents propose too many objectives and strategies because they don't feel resource constraints.

**Mitigation:** The commission includes explicit scope caps: "Maximum [N] objectives, maximum [M] strategies." The OD Architect enforces these caps during synthesis. If proposals exceed caps, the OD Architect ranks by relevance to the Governor's Problem Statement and presents the top-N with runners-up noted.

### 10.2 Governor Rubber-Stamping

**Risk:** Governor approves an agent-drafted OD they don't fully understand, making the Governor-quality problem worse.

**Mitigation:** The Comprehension Gate (§5.2) requires the Governor to articulate each objective's purpose and kill condition in their own words. This cannot be skipped. If the Governor says "it all looks fine" without engaging, the OD Architect must ask targeted questions: "Can you explain why OBJ-2 is separate from OBJ-1?" This is the most important safeguard in the protocol.

### 10.3 Decomposition Drift

**Risk:** The synthesized OD solves a different problem than the Governor intended, through well-meaning structural improvement by agents.

**Mitigation:** The Governor Intent Fidelity check (§6.3.1) explicitly compares the final OD's goal against the original Problem Statement. If they've diverged, the OD Architect explains why and asks the Governor to confirm the drift is acceptable.

### 10.4 Ingestion Staleness

**Risk:** The agent reads an old version of the framework or protocols.

**Mitigation:** The Ingestion Log records exact version numbers. The sync-manifest check (Step 7 in §2.1) catches recent changes. The re-ingestion triggers (§2.3) define when a full re-read is required.

---

## Changelog

| Version | Date | Changes | Source |
|---------|------|---------|--------|
| v0.1 | 2026-03-22 | Initial draft. Framework Ingestion phase, Governor Commission, Decomposition phase with domain agents, Governor Review Gate with Comprehension Gate, Quality Gate extensions, Multi-tier considerations, Failure mode mitigations. | ChatGPT assessment finding (OD-as-single-point-of-failure) + stress-test observations (Governor-quality dependency) |

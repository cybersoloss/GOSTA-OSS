# Domain Model Authoring Protocol

**Version:** 0.3
**Derives from:** Framework §13.2–13.6, §21.11; Cowork Protocol §3.1
**Purpose:** Step-by-step procedure for creating a domain model from one or more source resources. Produces a domain model conformant to `cowork/templates/domain-model.md`.

---

## 1. Scope

This protocol governs the extraction of domain knowledge from source resources (documents, regulations, book chapters, research papers, web pages) into a GOSTA domain model. It covers single-source and multi-source workflows.

It does NOT cover:
- Domain model creation from Governor corrections (no source document) — see Cowork Protocol §3.1.1 (first-cycle correction-derived procedure, operationalizes Framework §21.11)
- Domain model updates from execution feedback — see Cowork Protocol §3.1 rule 9 (deliberation feedback) and Deliberation Protocol §12.4
- Domain model replacement during execution — see Cowork Protocol §4 (Domain model replacement protocol), which routes to this protocol when the replacement requires source-based creation
- Domain model stacking or runtime quality detection — see Framework §13.7, §13.3

---

## 2. Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Primary source(s) | Yes | The document(s) from which domain knowledge will be extracted. Must be the original text — not summaries, interpretations, or AI-generated derivatives. |
| Application context | Yes | What session or scope this model serves. From the Governor. |
| Purpose statement | Yes | What evaluation criteria this model should provide. From the Governor. |
| Enhancement sources | No | Secondary documents consulted AFTER the primary extraction is complete. |
| Existing domain models | No | Other domain models in the same session, for cross-model relationship mapping. |

**Source integrity rule (Framework §13.6, §21.11):** The primary source must be established domain knowledge — books, industry standards, regulations, professional frameworks, verified research. Agent training data is not a source. If the Governor provides only keywords or topic names, the agent must not generate a domain model from memory. Instead: flag the gap, request source material, or use the Reference Pool to locate relevant resources (Protocol §3.1 rule 5).

**Component build priority (Protocol §3.1 rule 6):** If the source material is thin and only supports a 3-component model (Core Concepts + Quality Principles + Anti-Patterns), that is the minimum viable model. When extending to a 4th component, add the **Hypothesis Library** first — it is the single highest-value component above the floor.

---

## 3. Procedure

### Step 1 — Source Reading (full pass)

Read the primary source completely before extracting anything. Do not begin building components while still reading. The purpose is to understand the source's structure, scope, and internal logic before making extraction decisions.

During this pass, note:
- What the source treats as foundational (these become Core Concept candidates)
- What the source treats as good practice vs. bad practice (Quality Principles and Anti-Patterns)
- What the source treats as testable approaches (Hypothesis Library candidates)
- What the source treats as boundaries or constraints (Guardrail Vocabulary candidates)
- What relationships the source draws between its own concepts

If there are multiple primary sources, read all of them before proceeding. Note where sources agree, disagree, or cover non-overlapping territory.

### Step 2 — Model Type Classification and Knowledge vs. Strategy Separation

Before extracting anything, make two classification decisions.

**2a. Model Type Classification**

Identify the model's primary functional type. This determines what the model must deliver to be useful to an agent. A single model may contain sections of different types (e.g., Content Curation has craft sections and audience-facing sections), but the dominant type should be declared and shapes extraction priorities.

| Type | Agent need it serves | What it must encode | Example |
|------|---------------------|--------------------|---------
| **Constraint** | Boundary enforcement — agent checks output against permitted/prohibited boundaries | Clear permit/deny criteria, boundary tests, prohibited concepts, accumulation risks | Public Disclosure Policy |
| **Operational** | Sequencing, dependencies, execution checklists — agent follows procedures | Dependency graphs, prerequisite chains, checklists, escalation rules, metrics | Campaign Operations |
| **Craft** | How to do something well regardless of audience — agent shapes output quality | Format rules, style standards, platform mechanics, voice definitions, structural patterns | Content Curation §1.5–1.6 |
| **Audience-facing** | Help agent produce output that works on a specific audience — agent transforms drafts | Audience evaluation model (how they assess claims), skepticism triggers, evidence formats they trust, subject-to-audience mapping | Funding Alignment, BIIC |

**Why type matters:** A model that says "enables agents to produce investor-compelling content" (audience-facing purpose) but only encodes the subject's properties (craft structure) has a type-purpose mismatch. The model will help agents *check* output but not *transform* it for the intended audience. Declaring type early prevents this mismatch by shaping what gets extracted.

**Type-specific extraction guidance:**
- **Constraint models:** Focus extraction on boundaries, prohibited concepts, boundary tests, accumulation risks. Quality Principles define how to apply the boundary. Anti-Patterns show what boundary violations look like in practice.
- **Operational models:** Focus extraction on dependencies, sequencing rules, checklists, metrics. Quality Principles define operational excellence. Anti-Patterns show operational failures with recovery procedures.
- **Craft models:** Focus extraction on format rules, quality standards, style definitions, structural patterns. Quality Principles define what good output looks like mechanically. Anti-Patterns show craft failures.
- **Audience-facing models:** Focus extraction on the audience's evaluation dimensions — how they assess, what makes them skeptical, what evidence they trust. Core Concepts must encode the audience's mental model alongside the subject's properties. Quality Principles define what output looks like that successfully engages the audience. Anti-Patterns show failures to connect with the audience's evaluation model.

**Record the type classification** in the Purpose field of the model header, alongside the purpose statement. Example: "Purpose: [Audience-facing] Provides knowledge about what funding assessors value so that announcement content can naturally demonstrate alignment..."

**2b. Knowledge vs. Strategy Separation**

Classify the source content:

| Category | Belongs in domain model | Examples |
|----------|------------------------|----------|
| **Facts** — what is true about the domain | Yes (Core Concepts) | Regulatory requirements, market structures, technical constraints, established principles |
| **Quality standards** — what good looks like | Yes (Quality Principles) | Assessment criteria, best practices, professional standards |
| **Failure modes** — what bad looks like | Yes (Anti-Patterns) | Known mistakes, common traps, false signals |
| **Constraints** — what is forbidden or required | Yes (Guardrail Vocabulary) | Legal prohibitions, ethical boundaries, hard dependencies |
| **Testable approaches** — approaches that can succeed or fail | Yes (Hypothesis Library) | Strategies with conditions, approaches with trade-offs |
| **Audience evaluation knowledge** — how a target audience assesses, decides, or reacts | Yes (Core Concepts — audience-facing models only) | Investor evaluation criteria, assessor scoring dimensions, reader skepticism triggers, evidence formats an audience trusts |
| **Recommendations** — what the source says to do | **No** | Specific CTAs, tactical prescriptions, action sequences, channel selections |
| **Strategy** — how to win | **No** | Competitive moves, campaign plans, prioritization choices |

**Critical distinction for audience-facing models:** Knowledge about how an audience evaluates (their mental model, decision criteria, what evidence they need) is domain knowledge — it belongs in the model. Knowledge about how the agent should sequence, frame, or present information to exploit that mental model is strategy — it belongs with the agent during deliberation. The model encodes *what the audience looks for*. The agent decides *how to deliver it*.

**The test (from template):** Could an agent reasonably choose a *different* approach while still satisfying all Quality Principles and Guardrails? If not, you are encoding strategy as knowledge. Extract the underlying principle instead of the specific recommendation.

**Example:**
- Source says: "Post on LinkedIn at 9am Tuesday for maximum reach among enterprise buyers."
- Wrong extraction: QP: "Post on LinkedIn at 9am Tuesday" (this is a tactical prescription)
- Right extraction: Core Concept: "Platform algorithms reward timing alignment with audience activity patterns." Anti-Pattern: "Publishing without regard to audience availability windows."

**Audience-facing example:**
- Source says: "Investors want to see a clear path to revenue before committing."
- Wrong extraction: QP: "Include a revenue projection slide" (tactical prescription — steals agent's presentation design space)
- Right extraction: Core Concept: "Financial Logic — investors evaluate whether the path from current state to revenue is structurally sound and evidence-backed, not aspirational." This tells the agent what investors look for; the agent decides how to demonstrate it.

### Step 3 — Core Concepts Extraction

Extract foundational concepts from the source. Organize by theme, not alphabetically (Protocol §3.1 rule 2).

For each concept:
1. **Name it** using the source's own terminology where possible
2. **Write applied narrative** connecting the concept to the Application Context — not encyclopedic definitions (Protocol §3.1 rule 1)
3. **Define boundaries** — what the concept does NOT include (Template §1 distortion-prevention, Framework §14.3.2)
4. **Include 2–3 application examples** to prevent agent fixation on one manifestation
5. **Flag common misapplications** if the concept is frequently confused with adjacent ideas

**Specificity test (Framework §13.3):** Does the concept description explain how it applies specifically to THIS session's context, not just define it generically? If the description would be equally true for any project in this domain, it is too generic.

**Minimum:** 3 core concepts. Recommended: 6+ for full analytical depth.

### Step 4 — Concept Relationships

Map how extracted concepts relate to each other. Three relationship types:

1. **Prerequisites** — which concepts must be satisfied before others can operate?
2. **Tensions** — where do concepts pull in opposing directions?
3. **Amplifiers** — where does satisfying one concept strengthen another?

Also map relationships to concepts in other domain models in the same session, if they exist. Cross-model tensions are the highest-value analytical output of multi-domain assessment (Framework §13.7).

**Quality check:** Each relationship must identify the specific dependency, tension, or amplification. Listing concept pairs without explaining the relationship mechanism adds no value (Template §2).

### Step 5 — Quality Principles

Extract what "good" looks like from the source. These become evaluation criteria that agents apply during scoring and deliberation.

For each principle:
1. State the principle concretely
2. Define how to evaluate it — what to look for, what counts as meeting it

**Distinctiveness test (Framework §13.3):** Would applying this principle to a different domain produce a different assessment? If no, it adds no analytical value beyond other domains.

**Knowledge-vs-strategy check:** Quality Principles say what good output looks like. They do NOT say which specific output to produce. "Content must demonstrate domain expertise" is a quality principle. "Content must include three case studies" is a tactical prescription.

**Minimum:** 3 quality principles.

### Step 6 — Anti-Patterns

Extract what "bad" looks like. Common mistakes, failure modes, false signals specific to this domain.

For each anti-pattern:
1. Describe the failure pattern
2. Explain why it is harmful
3. Describe how to detect it
4. Include **exception conditions** — the boundary between the anti-pattern and valid practice (Framework §13.6 step 6). Without exception conditions, coarse anti-patterns flag valid approaches.

**Anti-Pattern specificity test (Framework §13.3):** Is this anti-pattern already covered by basic critical thinking? If yes, it does not prevent domain-specific errors.

**Minimum:** 2 anti-patterns.

### Step 7 — Hypothesis Library

Extract testable approaches from the source. These become starting points for tactic design.

Format: "If [action], then [outcome], because [reasoning from core concepts]."

The hypothesis library captures approaches that *could* work under stated conditions — not approaches that the source says *must* be used. Multiple competing hypotheses for the same objective are expected and valuable.

**Minimum:** 2 hypotheses.

### Step 8 — Guardrail Vocabulary

Extract domain-specific constraints. These are concepts that naturally become guardrails in Operating Documents.

For each guardrail:
1. State the constraint
2. Classify severity: **hard** (violation = immediate stop) or **soft** (violation = flag for Governor review)
3. Explain why the constraint matters in this domain

Sources of guardrails: legal requirements, ethical boundaries, technical limitations, organizational policies, professional standards, risk thresholds.

**Minimum:** 2 guardrail vocabulary entries.

### Step 8b — Safe Defaults Per Action Type (Framework §13.6 step 7)

For each action type the system will execute in this domain, define a **safe default** — the conservative, deterministic action that keeps the system operational if the orchestrator fails mid-execution.

- For action types where repetition would be harmful (e.g., duplicate outreach to the same contacts, re-sending the same referral request), the safe default is **skip** — do not execute.
- Record safe defaults in the Anti-Patterns section so the system knows which action types must not be blindly repeated.

If the source material does not describe action types (e.g., a regulatory text or research paper), this step may produce nothing. That is acceptable — safe defaults are populated as the session's action types become concrete.

### Step 9 — Enhancement Source Integration (if applicable)

Only after Steps 3–8 are complete from the primary source, consult enhancement sources. Enhancement sources may:
- Add session-specific or project-specific elements
- Provide additional examples or application context
- Surface anti-patterns or hypotheses not covered in the primary source

Enhancement sources must NOT:
- Replace primary-source concepts with alternative interpretations
- Override the primary source's definitions or boundaries
- Change the domain model's scope or purpose

Tag any content added from enhancement sources so the provenance is traceable.

### Step 10 — Template Assembly

Assemble the extracted content into the template structure (`cowork/templates/domain-model.md`):

1. Fill the header: Source, Enhancement Sources, Application Context, Created, Purpose
2. Include both authoring protocol blockquotes (authoring order, knowledge-vs-strategy)
3. Populate all 6 components in order
4. Use component-specific ID prefixes (e.g., QP-XX-1, AP-XX-2, GV-XX-3 where XX is a short domain code)

### Step 11 — Validation

Run these checks before presenting to the Governor:

**Structural completeness (Framework §13.3, minimum thresholds):**
- [ ] ≥3 core concepts
- [ ] Concept Relationships section present (may be initially sparse)
- [ ] ≥3 quality principles
- [ ] ≥2 anti-patterns (each with exception conditions)
- [ ] ≥2 hypothesis library entries
- [ ] ≥2 guardrail vocabulary entries (each with severity classification)
- [ ] Safe defaults considered for known action types (may be empty if action types are not yet concrete)

**Content quality (Framework §13.3 quality criteria):**
- [ ] **Specificity test passed** — concept descriptions are specific to the application context
- [ ] **Distinctiveness test passed** — quality principles differ from what other domains would produce
- [ ] **Anti-pattern specificity test passed** — anti-patterns go beyond basic critical thinking
- [ ] **Knowledge-vs-strategy test passed** — no tactical prescriptions in Core Concepts or Quality Principles; an agent could choose a different approach while satisfying all QPs and Guardrails

**Authoring rules (Protocol §3.1):**
- [ ] Application Context stated
- [ ] Concepts organized by theme, not alphabetically
- [ ] Each concept includes domain-specific implications
- [ ] Model ≤~120 lines of applied content (excluding headers and template boilerplate)
- [ ] Source material cited in header

**Functional verification (agent-seat test):**

After structural and content quality checks pass, run the agent-seat test. This test verifies that the model delivers the right type of support for its declared purpose.

**The test:** Put yourself in the agent's seat. You have a draft (or a task to execute). You load this domain model. Walk through the model section by section and answer:

1. **Can I act on this?** For each Core Concept, can you point to a specific thing you would *do differently* in your draft because of this knowledge? Or does the concept only confirm something you already know without changing your output?
2. **Does the model match its declared type?** Apply the type-specific check:

| Declared Type | Agent-Seat Question | Failure Signal |
|--------------|--------------------|----- |
| **Constraint** | "Can I take my draft, scan it against this model, and identify every statement that must be removed or revised?" | Model describes what's bad in general terms but doesn't give you the boundary test or specific prohibited concepts to scan for. |
| **Operational** | "Can I take this model and execute a sequence of operations? Do I know what comes before what, what to check, and when to escalate?" | Model describes operational concepts but doesn't give you the dependency graph, checklists, or decision rules to execute. |
| **Craft** | "Can I take my draft and improve its structural quality — format, voice, platform fit — using this model?" | Model states quality aspirations but doesn't give you the specific format rules, voice definitions, or platform constraints to apply. |
| **Audience-facing** | "Can I take my draft and transform it so the target audience's evaluation criteria are addressed? Do I know what they look for, what makes them skeptical, and what evidence they trust?" | Model encodes the subject's properties but not the audience's mental model. You can check your draft doesn't violate guardrails, but you can't restructure it to create engagement because you have no model of the reader's mind. |

3. **Transformation vs. evaluation gap** (audience-facing models only): Read your Core Concepts and ask: "Do these concepts tell me what the *audience* evaluates, or only what the *subject* is?" A model that only describes the subject helps agents evaluate output ("does this accurately represent X?") but not transform it ("does this address what the audience needs to see about X?"). Both layers are needed.

**If the agent-seat test reveals gaps:** This is not a failure of the authoring steps — the six components may all be structurally valid. It is a failure of model design. Common fixes:
- **Missing audience mental model:** Add audience evaluation dimensions to Core Concepts. For each dimension: what the audience assesses, what demonstrates it, what evidence format they trust.
- **Concepts too generic:** Rewrite with applied narrative that connects to the specific task an agent would perform.
- **Guardrails without transformation knowledge:** The model can prevent bad output but can't guide good output. Add the positive knowledge layer (what *to* do, not just what not to do).

**If any check fails:** Fix before presenting. Do not present a domain model that fails validation and rely on the Governor to catch it — that inverts the quality assurance direction.

---

## 4. Multi-Source Workflow

When multiple primary sources cover different aspects of the same domain:

1. Read ALL sources completely (Step 1) before extracting from any
2. Identify overlapping territory — where sources agree, these are high-confidence concepts
3. Identify contradictions — where sources disagree, present both positions as distinct concepts or note the tension in Concept Relationships
4. Identify gaps — territory covered by one source but not another. These are valid single-source extractions.
5. Proceed through Steps 2–11 drawing from all sources. The header should list all primary sources.

When multiple primary sources cover different domains (i.e., the Governor wants one model combining two fields): reconsider whether this should be two separate domain models. Domain model stacking (Framework §13.7) is usually better than cramming two domains into one model, because stacking preserves cross-domain tension detection. If the Governor still wants a combined model, proceed but flag the trade-off.

---

## 5. Common Extraction Errors

| Error | Description | Fix |
|-------|-------------|-----|
| **Strategy-as-knowledge** | Source recommends a specific approach; author encodes it as a Core Concept or Quality Principle instead of extracting the underlying principle | Apply the knowledge-vs-strategy test (Step 2). Extract the principle, not the recommendation. |
| **Encyclopedic extraction** | Author copies source definitions verbatim without connecting to Application Context | Rewrite as applied narrative (Protocol §3.1 rule 1). Every concept must explain its implications for THIS context. |
| **Missing boundaries** | Concept is defined by what it IS but not what it ISN'T | Add boundary definitions and common misapplications (Template §1 distortion-prevention). |
| **Coarse anti-patterns** | Anti-patterns are too broad, flagging valid practice as failures | Add exception conditions (Framework §13.6 step 6). |
| **Guardrail-as-preference** | Author classifies a stylistic preference as a hard guardrail | Hard guardrails = violation requires immediate stop. If reasonable people could disagree, it is soft at most. |
| **Source amnesia** | Author starts generating domain knowledge from training data instead of extracting from the source | Every concept should be traceable to a specific section, principle, or finding in the source document. |

---

## 6. Governor Interaction

The Governor is involved at two points:

1. **Before Step 1:** Governor provides or approves the primary source(s), Application Context, and Purpose.
2. **After Step 11:** Governor reviews the completed domain model. The Governor may: approve, request additions, request removals, or request restructuring. Domain models enter the session only after Governor approval.

The agent does NOT auto-expand keywords into domain models without Governor review (Protocol §3.1 rule 5). If the source material is insufficient to meet minimum thresholds, the agent reports the gap and requests additional sources — it does not fill gaps from training data.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1 | 2026-03-26 | Initial version. Codifies extraction workflow from Framework §13.2–13.6, §21.11 and Protocol §3.1. |
| 0.2 | 2026-03-26 | Scope section updated: cross-references to §3.1.1 (correction-derived creation), §4 (replacement protocol), and Deliberation Protocol §12.4 (feedback updates). Clarifies how execution-time triggers route to this protocol. |
| 0.3 | 2026-03-26 | Model type classification added to Step 2 (constraint, operational, craft, audience-facing). Functional verification (agent-seat test) added to Step 11. Knowledge-vs-strategy table extended with audience evaluation knowledge row. Type classification shapes extraction priorities and is verified post-assembly. |

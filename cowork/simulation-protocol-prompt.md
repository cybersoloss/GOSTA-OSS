# GOSTA Simulation Protocol

**Purpose:** Run a structured simulation that stress-tests the GOSTA framework, Cowork protocol, and user experience simultaneously on any topic. Produces four deliverables (five if an app design is provided): framework findings, protocol findings, UX findings, risk register, and optionally app design findings.

**Version:** 3.1

---

## How to Use This Prompt

The Governor says: **"Create a sim on [TOPIC] using GOSTA with this file."**

The AI then:
1. Reads this file (simulation protocol).
2. Locates and reads the GOSTA framework spec (highest version `.md` file in the repo root matching `GOSTA*architecture*`).
3. Locates and reads `cowork/gosta-cowork-protocol.md`, `cowork/CLAUDE.md`, and all files in `cowork/templates/`.
4. **If an app design document is referenced** (product definition, wireframes, user flow, architecture doc), reads it. This activates the 4th simulation axis (see "App Design Stress Testing" below).
5. Determines the simulation directory (Governor may specify a path, otherwise create `sessions/[topic-slug]/`).
6. Executes Phases 0–6 below.

If the Governor provides additional parameters (persona, domain count, etc.), use them. Otherwise, apply defaults.

---

## The Simulation

You are running a GOSTA simulation. This simulation has three simultaneous objectives (four if an app design is provided):

1. **Stress-test the GOSTA framework** — find where the spec is ambiguous, silent, or structurally insufficient.
2. **Stress-test the Cowork protocol** — find where the protocol fails to translate the framework into executable steps.
3. **Stress-test the user experience** — simulate a real user running this analysis and find where the flow breaks, confuses, or fails to deliver value.
4. **Stress-test the app design** *(conditional — only when an app design document is provided)* — validate whether the app's user journey, output format, and scalability assumptions hold when real analysis runs through them. The simulation becomes a functional test of the app design.

The simulation runs on two layers. **Layer 1 (surface)** is the actual analysis — this is the output a user would see. **Layer 2 (meta)** is the real objective — capturing every point where the framework, protocol, UX, or app design failed during Layer 1. Layer 2 is why we're here. Layer 1 is the vehicle.

---

### Phase 0: Simulation Setup

**Inputs (Governor provides or defaults apply):**

| Input | Description | Default |
|---|---|---|
| **Topic** | What the simulated user wants to analyze | *(required — no default)* |
| **User persona** | Naive (keywords only), Informed (structured questions), or Both | Naive |
| **Domain count** | How many domain models to use | 3 |
| **Domain models** | Pre-built (use existing in repo), AI-created (build from topic), or Mixed | AI-created |
| **Intelligence source** | Real web search, mocked data, or hybrid | Real web search |
| **Isolation level** | Level 1 (same context, labeled), Level 2 (sequential, no back-revision), Level 3 (separate agents) | Level 2 |
| **Priority order** | If context exhaustion hits, which deliverables to produce first | B > A > D > C > E |
| **Sim directory** | Where to create files | `sessions/[topic-slug]/` |
| **App design** | Product definition, wireframes, or user flow document to stress-test | None (3-axis sim). If provided, activates 4th axis. |

**Setup actions:**
1. Read the GOSTA framework spec, protocol, CLAUDE.md, and all templates (see "How to Use" above).
2. Create the simulation directory structure (see File Structure below).
3. Determine the simulation number: check if prior sims exist in the directory. If yes, increment (sim2, sim3...). If no, this is sim1.
4. Save the design as `sim[N]/00-SIMULATION-DESIGN.md` with all parameters recorded.

---

### Phase 1: Bootstrap

Execute the GOSTA bootstrap process as if a real user initiated it. Follow the Cowork protocol exactly.

**Actions:**
1. Transform the topic into domain model candidates. The topic might be a single keyword ("climate change"), a question ("should we enter the AI market?"), or a complex statement. Decompose it into 3+ analytical dimensions that become domain candidates.
2. Build or select domain models:
   - **AI-created:** Produce full 6-component models (Core Concepts, Concept Relationships, Quality Principles, Anti-Patterns, Hypothesis Library, Guardrail Vocabulary) using the `cowork/templates/domain-model.md` template. Also produce a 3-component version (Core Concepts, Quality Principles, Anti-Patterns) to test the quality floor.
   - **Pre-built:** If existing domain models are available in the repo, select and reference them.
   - **Mixed:** Some pre-built, some AI-created.
3. Draft an Operating Document following the `cowork/templates/operating-document.md` template.
4. Draft a Scope Definition following the `cowork/templates/scope-definition.md` template.
5. If the Governor is present (interactive session), present for approval. If running autonomously, proceed with self-approval and note it.

**Capture during this phase (L2 annotations):**
- Every point where the protocol was ambiguous about what to do next.
- Every point where the framework didn't define something the protocol needed.
- Every point where a user would be confused, blocked, or would abandon.
- Time estimate: how long would this take a real user?
- If keywords map to multiple candidate domains, note the disambiguation gap.
- **If app design provided:** Does the bootstrap flow match the app's onboarding/domain selection UX? Note every mismatch between what the protocol does and what the app design says the user sees.

---

### Phase 2: Intelligence Gathering & Signal Processing

Execute the analysis cycle: gather intelligence, process into signals, apply domain models.

**Actions:**
1. Execute web searches (or mock, per setup) — one per domain minimum.
2. Apply **signal triage** before recording: relevance to active tactic, source credibility minimum, temporal currency. Record what was triaged out and why.
3. Record formal signals using the `cowork/templates/signal-entry.md` template. For compound sources (single source, multiple claims), record as one signal with individually tagged claims.
4. Attribute each signal with:
   - **Source tier (1-6):** Tier 1 = sensor/primary data, Tier 2 = institutional research, Tier 3 = quality journalism, Tier 4 = partisan/editorial, Tier 5 = government/official statements, Tier 6 = social media/unverified.
   - **Credibility modifier:** neutral, partisan-[direction], affiliated-[entity], or self-interested. Use modifiers that fit the topic — these are not fixed categories.
   - **Temporal validity window:** How long this signal remains reliable (hours, days, weeks, or "structural" for permanent facts).

**Capture during this phase (L2 annotations):**
- Signal volume: raw sources found vs. signals formally recorded (triage ratio).
- Source credibility distribution: how many per tier?
- Compound signal count: how many sources contained multiple distinct claims?
- Missing domain detection: did the search reveal analytical dimensions the user didn't include?
- Cost tracking: count of web searches, AI calls, estimated compute cost.
- **If app design provided:** Does the app's progress UI accommodate the actual triage ratio? Does the source count match what the app promises to display? Does the cost at this phase match the app's credit model?

---

### Phase 3: Cross-Domain Analysis & Tension Surfacing

Execute the core analytical step: run each domain independently, then synthesize.

**Actions:**
1. Run domain-by-domain assessment at the specified isolation level.
   - **Level 1:** Same context, clearly labeled domain sections.
   - **Level 2:** Sequential assessment. Once a domain's assessment is written, no back-revision when assessing subsequent domains.
   - **Level 3:** Separate agent calls per domain (if tools support it). When Level 3 is selected and 3+ domain models are active, the Deliberation Protocol (cowork/deliberation-protocol.md) governs the multi-agent round structure, disagreement classification, and synthesis. Each domain model is assigned a Domain Agent; a Coordinator manages the rounds. See Framework §14.7 for the three-level escalation model.
2. Run synthesis: identify cross-domain tensions.
3. Classify each tension:
   - **BLOCKING** — domains fundamentally disagree; the user must make a framing decision before analysis can conclude.
   - **MATERIAL** — domains disagree substantively but analysis can proceed with both views presented.
   - **INFORMATIONAL** — domains surface different facets of the same truth; no real disagreement.
4. Produce the analysis output in the **4-layer format:**
   - **Layer 1:** Summary + Key Tension (primary view — what the user sees first)
   - **Layer 2:** Per-domain assessments (expandable detail)
   - **Layer 3:** All tensions with classification (expandable)
   - **Layer 4:** Source breakdown + cost + temporal validity (footer)

**Capture during this phase (L2 annotations):**
- Tension count by classification (blocking / material / informational).
- Did any BLOCKING tension reframe the user's original question? (This is the core value signal.)
- Domain contamination: at Level 2, did later domains show awareness of earlier domains' assessments despite the no-back-revision rule?
- Kill condition testability: could you define a meaningful kill condition for this analysis? If the topic is qualitative, note whether the framework supports qualitative kill conditions.
- Guardrail evaluation: which guardrails could be checked at phase gate vs. only at deliverable completion?
- **If app design provided:** Does the 4-layer output format match the app's display design? Does the key tension surface in the position the app design specifies? Are there output elements the protocol produces that the app design doesn't accommodate, or vice versa?

---

### Phase 4: Health Computation & Review

Execute the GOSTA health computation and review cycle.

**Actions:**
1. Compute tactic health for each active tactic.
2. Compute strategy health.
3. Compute goal health.
4. Check all guardrails (both phase-level and deliverable-level, noting which is which).
5. Produce a health report following the `cowork/templates/health-report.md` template.
   - Verify that all recommendations in the health report carry epistemic classification (confirmed/information_gap/conditional per §14.3.8). Check that kill recommendations classified as `information_gap` are not presented as autonomous decisions.
6. Make a phase-gate decision: advance / iterate / kill.

**Capture during this phase (L2 annotations):**
- Composite score: what normalization did you use? Was it defined in the protocol or did you invent one?
- Guardrail evaluation timing: which guardrails couldn't be checked until the deliverable existed?
- Kill condition fit: did the kill conditions defined in the OD actually test for the right failure modes?
- Temporal validity: is the analysis already degrading? What's the validity window?
- Template mismatch: which health report template fields were irrelevant for this scope type?
- Epistemic classification: did each recommendation receive a classification? Were any `information_gap` kills incorrectly presented as autonomous?

---

### Phase 5: Deliverables

Produce four structured deliverables (five if app design is provided). If context is running low, produce in priority order (per setup, default: B > A > D > C > E).

---

#### Deliverable A: Protocol Enhancement Findings

For every point during the simulation where the Cowork protocol was insufficient, ambiguous, or silent.

**Format per finding:**

| Field | Content |
|---|---|
| **ID** | PA-[N] / PB-[N] / PC-[N] (severity prefix) |
| **Protocol Section** | §X.Y |
| **Finding** | What happened |
| **Impact** | What goes wrong if unfixed |
| **Recommended Fix** | Specific text change with estimated line count |

**Severity:**
- **(A) Would cause experiment failure** — the protocol doesn't define something required, and the experiment can't proceed.
- **(B) Would cause silent degradation** — the experiment proceeds but produces worse output without anyone noticing.
- **(C) Inconvenience** — friction or ambiguity that slows work but doesn't affect outcomes.

**Known gap checklist** — verify each during the simulation:
- Signal triage: does the protocol handle high-volume signal sources? Is there a triage output template?
- Compound signals: does the signal format support multi-claim sources with per-claim metadata?
- Analytical guardrails: does the guardrail model handle quality criteria (not just metric boundaries)?
- Source credibility modifiers: are credibility modifiers supported in signal format?
- Temporal validity: is signal/analysis expiry defined?
- Composite score normalization: is the health computation reproducible across sessions?
- Phase-gate partial exit: what happens when exit criteria are "partially met"?
- Deliverable organization: is there a naming convention and structure for outputs?
- Domain model reuse: if using pre-built models, is the reuse/versioning protocol defined?
- Keyword disambiguation: if user keywords map to multiple domains, is the disambiguation step defined?
- Confidence expression: does the scoring model fit analytical scopes (qualitative confidence vs. numeric)?

---

#### Deliverable B: Framework Enhancement Findings

For every point where the GOSTA framework itself (not just the protocol) was insufficient.

**Format per finding:**

| Field | Content |
|---|---|
| **ID** | FB-[N] |
| **Framework Section** | §X.Y |
| **Classification** | Ambiguity / Missing Tier Differentiation / Structural Gap |
| **Finding** | What the framework says (or doesn't say) |
| **Impact** | What the protocol had to do as a workaround |
| **Recommended Spec Change** | Specific addition or modification |

**Classification types:**
- **Ambiguity** — the spec can be interpreted multiple ways; the protocol had to pick one without clear guidance.
- **Missing Tier Differentiation** — the spec requires something at a single level of rigor that should vary by tier.
- **Structural Gap** — the spec is silent on something the protocol needs to implement.

**Known gap checklist** — verify each during the simulation:
- Analytical vs. operational scope: does the framework differentiate them sufficiently?
- Signal triage at architecture level: is pre-recording filtering defined in the spec?
- Signal granularity: what constitutes one signal?
- Qualitative kill conditions: can kill conditions be structural tests, not just metric+date?
- Guardrail types: is there a guardrail type for quality criteria in analytical scopes?
- Temporal validity: does the signal spec include expiry? Does it handle permanent/structural signals?
- Domain completeness detection: can the framework flag missing analytical dimensions? At what timing?
- Tension semantics: does "blocking" mean the same thing in operational vs. analytical scopes?
- Domain model depth: is minimum viable depth (e.g., 3-component floor) defined per tier?
- Objective measurability: can analytical scopes have structural (non-numeric) measurability?
- Health report fields: do they adapt to scope type (finite vs. ongoing)?
- Composite score normalization: does it handle non-standard metric directionality?

---

#### Deliverable C: UX & Product Findings

For every point where a real user would be confused, blocked, or underwhelmed.

**Format:** User journey map with friction annotations.

```
Step N: [WHAT HAPPENS]
   FRICTION: [what goes wrong for the user]
   IMPACT: [abandonment / confusion / reduced value]
   SOLUTION: [product design recommendation]
   COST: [estimated compute cost for this step]
```

**Known gap checklist** — verify each during the simulation:
- Keyword disambiguation: does the system handle ambiguous user input?
- Missing domain suggestion: does the system detect and suggest domains the user didn't include?
- Question decomposition: can broad questions be broken into structured objectives?
- Progress visibility: what does the user see while the system works?
- Tension prominence: is the KEY TENSION visually prominent and not buried?
- Dual-mode output: does the output serve both naive users and informed users?
- Source credibility legibility: are source tiers presented in a way non-experts understand?
- Temporal validity display: does the user know when the analysis expires?
- Cost transparency: does the user know what they paid before and after?
- Time-to-insight: how many seconds from question submission to first useful output?
- Domain gap warning timing: is it shown before the analysis (pre-purchase) or only after?

---

#### Deliverable D: Risk Register

Risks discovered during the simulation, categorized by source.

| Field | Content |
|---|---|
| **Risk** | Description |
| **Source** | Framework / Protocol / Domain / Business Model |
| **Severity** | would-break / would-degrade / would-annoy |
| **Likelihood** | HIGH / MEDIUM / LOW |
| **Mitigation** | Specific action |

---

#### Deliverable E: App Design Findings *(Conditional — only when app design document is provided)*

For every point during the simulation where the app design was invalidated, insufficient, or revealed a gap.

**Format per finding:**

| Field | Content |
|---|---|
| **ID** | AD-[N] |
| **App Design Section** | Which part of the app design (user journey step, UI component, architecture element) |
| **Category** | User Journey / Usability / Scalability / Output Format / Business Model |
| **Finding** | What the simulation revealed |
| **Evidence** | Which simulation phase/step exposed this |
| **Recommended Fix** | Specific design change |

**Mandatory checks — validate each during the simulation:**

**User Journey:**
- Does the app's onboarding flow handle keyword disambiguation? (Sim 3 found silent mapping.)
- Does the app show question decomposition to the user? (Sim 3 found invisible decomposition.)
- Does the app provide progress indicators during intelligence gathering? (Sim 3 found no visibility.)
- Does the app stream domain assessments progressively? (Sim 3 found batch delivery.)
- Does the domain gap warning appear both pre-analysis AND post-analysis? (Sim 3 found post-only.)

**Usability:**
- Does the output format match what the protocol actually produces? (Count fields, compare.)
- Is the key tension visually prominent — interactive card, not buried text?
- Does the accordion/expandable UI work for both naive and informed users?
- Are source credibility tiers presented in narrative form ("institutional, journalism, government") not raw numbers?
- Is temporal validity displayed as a banner/badge, not hidden in footer?

**Scalability:**
- What happens when signal volume exceeds triage capacity? (Sim 3 baseline: 30 raw → 10 retained.)
- Does the app's credit model hold at 4-5 domains? (Cost doubles but credit cost only doubles — margin preserved?)
- Does the re-weighting upsell mechanism work at scale? (What % of users will click? What's the server load?)
- Can the system handle concurrent analyses from multiple users on the same topic? (Caching implications.)
- Does the refresh mechanism create stale-data race conditions? (User A refreshes while User B reads old version.)

**Output Format:**
- Layer 1 (Summary + Key Tension): Does the app render this as the primary view?
- Layer 2 (Per-domain): Does the app support expandable/collapsible sections?
- Layer 3 (All tensions): Does the app support tension classification badges (BLOCKING/MATERIAL/INFORMATIONAL)?
- Layer 4 (Sources/cost/validity): Does the app show this as footer with expandable detail?
- Export: Does the app support PDF and shareable link?

If no app design is provided, skip this deliverable entirely. Do not fabricate app design findings from the UX findings in Deliverable C — those are protocol/framework UX issues, not app design validation.

---

### Layer 2 Annotation Protocol

Throughout all phases, capture issues inline using these tags:

```
[L2-PROTOCOL: §X.Y — description of what the protocol doesn't cover]
[L2-FRAMEWORK: §X.Y — description of what the spec doesn't define]
[L2-UX: description of user experience issue]
[L2-APP: app-design-section — description of app design mismatch or gap]
[L2-RISK: description of what would go wrong in production]
[L2-COST: operation=X, count=N, est_cost=$X.XX]
```

At the end of the simulation, extract all L2 annotations into the appropriate deliverable. Report the total count by category.

---

### Phase 6: Simulation Retrospective

After all deliverables are produced, write a retrospective answering:

1. **What worked?** Patterns validated by this simulation.
2. **What broke?** Anti-patterns discovered.
3. **What was missing?** Things this simulation needed but the framework/protocol didn't provide.
4. **Calibrated norms:** Baseline numbers established (cost per analysis, signal triage ratio, tension count, time-to-insight).
5. **Delta from previous sims:** If prior simulations exist in the same session directory, compare: new findings vs. confirmed findings vs. findings now resolved. If this is the first sim, skip this section.
6. **App design validation summary** *(if app design provided)*: Which app design assumptions were confirmed? Which were invalidated? What's the highest-priority design change?
7. **Recommendations for next simulation:** What should the next sim specifically target?

Save as `sim[N]/learnings.md`.

---

## Simulation Quality Criteria

A simulation is successful if it produces:

- [ ] ≥3 findings per deliverable (A, B, C, D). If a deliverable has 0 findings, explain why.
- [ ] ≥1 BLOCKING tension in the analysis. If 0, the topic may not be adversarial enough — note this.
- [ ] L2 annotation count ≥10 across all phases. Below 10 suggests the simulation was too shallow.
- [ ] Cost tracking for every phase.
- [ ] Temporal validity declared on the analysis output.
- [ ] Retrospective written.
- [ ] **If app design provided:** ≥3 findings in Deliverable E, covering at least 2 of the 4 categories (User Journey, Usability, Scalability, Output Format). If the app design perfectly matches the simulation output, explain why — this likely means the simulation wasn't adversarial enough.

---

## Simulation Anti-Patterns

Avoid these:

| Anti-Pattern | What Happens | Prevention |
|---|---|---|
| **Running dry on context before deliverables** | Simulation produces great analysis but no findings | Set priority order upfront. If context is 60% consumed and Phase 3 isn't done, skip to deliverables. |
| **Treating the analysis as the goal** | The analysis is compelling and the sim gets absorbed in it | The analysis is Layer 1 (surface). The findings are Layer 2 (meta). Layer 2 is why we're here. |
| **Inventing protocol workarounds without noting them** | The AI silently compensates for a protocol gap, making the gap invisible | Every time you do something the protocol doesn't specify, add an L2 annotation. |
| **Skipping health computation because analysis "looks good"** | Health computation reveals framework gaps that informal review doesn't | Always run Phase 4, even if the analysis seems complete. |
| **Under-specifying domain models to save context** | Shallow models produce generic output and the sim tests nothing | Minimum 3-component models. Full 6-component for at least one domain. |
| **Not tracking costs** | Business model findings have no grounding | Count every web search and AI call. Estimate costs even if imprecise. |
| **Guidance-template mismatch** | Adding protocol guidance without updating templates to match | After noting a protocol gap, check whether the corresponding template supports the fix. |

---

## File Structure

```
[sim-directory]/
├── domain-models/                     ← shared across sims in this session
│   ├── [domain-1].md
│   ├── [domain-2].md
│   └── [domain-3].md
├── sim[N]/
│   ├── 00-SIMULATION-DESIGN.md        ← Parameters + Governor decisions
│   ├── 01-scope-definition.md
│   ├── operating-document.md
│   ├── learnings.md                   ← Phase 6 retrospective
│   ├── signals/
│   │   └── [date]-signals.md
│   ├── health-reports/
│   │   └── [date]-phase-gate.md
│   └── deliverables/
│       ├── A-protocol-findings.md
│       ├── B-framework-findings.md
│       ├── C-ux-findings.md
│       ├── D-risk-register.md
│       ├── E-app-design-findings.md   ← Only if app design provided
│       └── analysis-report.md         ← Layer 1 output
```

If this is the first sim in a new session, create `sim1/`. If sims already exist, increment the number.

Domain models live at the session root if shared across sims, or inside `sim[N]/domain-models/` if sim-specific.

---

## Quick Start

To run a simulation:

1. Governor says: "Create a sim on [TOPIC] using GOSTA."
2. AI reads this protocol, plus the framework spec, cowork protocol, CLAUDE.md, and all templates.
3. AI applies defaults for any unspecified parameters.
4. AI creates the directory structure and `00-SIMULATION-DESIGN.md`.
5. AI executes Phases 1–6 sequentially, annotating L2 tags throughout.
6. AI extracts L2 annotations into deliverables A–D.
7. AI writes retrospective.
8. Governor reviews findings and decides which feed into protocol/framework updates.

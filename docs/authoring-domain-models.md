# Authoring Domain Models — A Walkthrough

A teaching artifact for writing your own GOSTA domain model from scratch. Companion to `cowork/domain-model-authoring-protocol.md` (which is procedure-only) and `cowork/templates/domain-model.md` (which is a stub template).

This walkthrough takes a single worked example — a hiring rubric domain model — through all six components, showing the difference between shallow models that produce weak sessions and rigorous models that produce strong sessions.

> **Time investment:** ~1.5–2 hours per domain model for first-time authors. Drops to ~30–60 min once you've internalized the patterns. Rigorous domain models are the load-bearing input that determines session output quality — under-investing here propagates downstream.

---

## Why Domain Models Matter

Without a domain model, the AI reasons from training data. It produces outputs that look domain-aware but aren't traceable to specific concepts or principles. Two prompts on the same problem produce different outputs and you can't tell why.

With a domain model, every claim cites a specific concept by name, states the concept's definition, and applies the concept to the case at hand. This is the cite-then-apply discipline (G-10). Two prompts on the same problem now produce comparable outputs — same concepts cited, differences traceable.

The domain model is also the **anti-sycophancy mechanism**. Without explicit concepts, the AI tends toward whatever framing the Governor seemed to prefer. With explicit concepts, the AI must trace claims back to the model — even when the trace produces unwelcome conclusions.

## The Six Components

Every GOSTA domain model has six components. Each has a distinct role; together they make the model usable for grounded reasoning.

| Component | Role | Failure mode if absent |
|---|---|---|
| **Core Concepts** | The domain's named ideas with definitions, boundaries, misapplication notes | AI uses general training terminology without traceable definitions |
| **Concept Relationships** | How concepts connect (prerequisites, tensions, amplifiers) | Cross-domain tensions don't surface; AI smooths over real conflicts |
| **Quality Principles** | Testable standards for "good" in this domain | Claims aren't evaluable; "good" is whatever the AI says is good |
| **Anti-Patterns** | Named failure modes the AI should detect and flag | AI doesn't recognize bad outputs in this domain |
| **Hypothesis Library** | Testable starting points (incl. Governor hypotheses) | Sessions don't test what the Governor cares about |
| **Guardrail Vocabulary** | Reusable constraints applicable across tactics | Each session re-invents constraints inconsistently |

---

## Worked Example: Hiring Rubric Domain Model

The rest of this walkthrough authors a "hiring-rubric" domain model for evaluating engineering-role candidates. We'll build it component-by-component, with annotations showing what good looks like vs what shallow looks like.

### Step 1: Pick a Primary Source

Domain models cite a primary source for traceability. The source is the canonical reference your model encodes; if your model conflicts with the source, the source wins (or you fork the source explicitly).

Good primary sources for a hiring rubric: a structured interviewing book (e.g., *Topgrading*, *Who*, *The Effective Manager*), a published methodology (e.g., Triplebyte/Otta evaluation frameworks), or your organization's documented hiring playbook.

> ❌ **Shallow:** "Source: my own experience hiring engineers."
> Provides no traceability; can't be checked or challenged.
>
> ✅ **Rigorous:** "Source: Geoff Smart and Randy Street, *Who: The A Method for Hiring* (2008) — Topgrading interviewing methodology, scorecard-based candidate evaluation. Adapted for engineering-role context with technical skill assessment from Triplebyte's published evaluation framework (2019)."
> Cites specific sources; states what was retained vs adapted; downstream readers can check against the originals.

### Step 2: Draft Core Concepts

Core Concepts are the domain's vocabulary. Each concept gets:
- A name (consistent throughout the model)
- A definition (one or two sentences from the primary source, paraphrased if necessary)
- A boundary (what the concept does NOT cover)
- A misapplication note (a common way people get this wrong)

Aim for 6–10 concepts. Fewer than 6, the model is probably too thin; more than 12, you may be conflating multiple domains into one model.

> ❌ **Shallow:**
> ```
> ### Skill Fit
> Whether the candidate has the skills needed for the role.
> ```
> No boundary, no misapplication note. "Skills needed for the role" is circular — what counts as "needed"? "Skill fit" could mean a hundred different things.
>
> ✅ **Rigorous:**
> ```
> ### Skill Match (Topgrading Scorecard concept)
> Whether the candidate's demonstrated capabilities (per their work history, technical
> assessment, and reference checks) align with the role's required outcomes (per the
> scorecard's Mission and Outcomes sections, NOT the JD's wishlist).
>
> **Boundary:** Does NOT cover potential, growth trajectory, or culture fit — those
> live in their own concepts. A candidate can have high Skill Match and low Trajectory.
>
> **Misapplication:** Equating Skill Match with years-of-experience. A candidate with
> 3 years of focused experience producing measurable outcomes scores higher on Skill
> Match than a candidate with 10 years of generic experience without traceable outcomes.
> ```
> Specific concept (Topgrading scorecard); explicit boundary (doesn't cover potential or culture); explicit misapplication (years-of-experience trap).

**Suggested Core Concepts for a hiring rubric:**

1. **Skill Match** — capabilities aligned with role outcomes
2. **Trajectory** — growth rate and potential
3. **Outcome Track Record** — measurable results in prior roles
4. **Culture Add** — what the candidate adds to the team's culture (not "fit", which selects for sameness)
5. **Compensation Realism** — fit between candidate's expectations and role's compensation band
6. **Onboarding Risk** — predictable startup friction (e.g., distance, family situation, prior role similarity)
7. **Interview Signal Quality** — how reliably the interview process surfaced the above

### Step 3: Fill Concept Relationships

Concepts don't exist in isolation. Relationships make their interaction explicit.

Three relationship types:
- **Prerequisite:** X must hold before Y matters. (e.g., "Skill Match is a prerequisite for considering Trajectory — a candidate without baseline skills doesn't have meaningful trajectory toward the role.")
- **Tension:** X and Y pull in opposite directions. (e.g., "High Compensation Realism may tension with high Skill Match for senior candidates — the most-skilled candidates often have compensation expectations above the role's band.")
- **Amplifier:** X strengthens Y. (e.g., "Strong Outcome Track Record amplifies confidence in Trajectory — a candidate who has shown growth before is more likely to grow again.")

Tensions are the most important — they're what cross-domain deliberation surfaces. Without explicit tensions, the AI smooths over real conflicts.

> ❌ **Shallow:**
> "All concepts work together to evaluate the candidate."
> No specific relationships; the AI can't surface real conflicts.
>
> ✅ **Rigorous:**
> ```
> ### Concept Relationships
>
> **Prerequisites:**
> - Skill Match is a prerequisite for considering Trajectory
> - Outcome Track Record is a prerequisite for inferring Trajectory (without past outcomes,
>   "growth potential" is wishful thinking)
>
> **Tensions:**
> - Skill Match ↔ Compensation Realism: senior candidates with high Skill Match
>   typically expect compensation above mid-level role bands
> - Culture Add ↔ Onboarding Risk: candidates who would add the most cultural variety
>   often have higher onboarding risk (different prior context, more adjustment)
> - Trajectory ↔ Outcome Track Record: high-trajectory junior candidates have weaker
>   track records by definition; the rubric must not over-penalize this
>
> **Amplifiers:**
> - Strong Outcome Track Record amplifies confidence in Trajectory
> - Strong Interview Signal Quality amplifies confidence in ALL other scores
> ```

### Step 4: Write Quality Principles

Quality Principles are testable standards. Each principle:
- References specific concepts by name
- Provides an observable criterion
- Is testable — someone reading the principle can tell whether it's been violated

> ❌ **Shallow:**
> "QP-1: Be thorough in candidate evaluation."
> Not testable; "thorough" is undefined.
>
> ✅ **Rigorous:**
> "QP-1: Skill Match scoring must cite specific outcomes the candidate produced (per the Outcome Track Record concept), not generic claims like 'has experience with X.' A score above 7/10 on Skill Match without at least one measurable outcome citation is a violation."
> Testable — read the score, check for outcome citations.

**Suggested Quality Principles:**

- **QP-1:** Skill Match scoring cites specific outcomes per Outcome Track Record (testable: outcomes present)
- **QP-2:** Trajectory scoring above 7/10 requires explicit prior-growth evidence (testable: growth evidence present)
- **QP-3:** Culture Add explicitly identifies what the candidate ADDS, not how they fit the existing culture (testable: addition stated, not just "good fit")
- **QP-4:** Compensation Realism scoring states the role band and the candidate's expectation; mismatch >20% gets explicit acknowledgment (testable: numbers present)
- **QP-5:** Onboarding Risk above 5/10 lists specific risk factors with mitigation paths (testable: factors enumerated)
- **QP-6:** Interview Signal Quality scoring acknowledges any interview-process gaps (panel diversity, behavioral question coverage, take-home presence) (testable: gaps acknowledged or "no gaps observed")

### Step 5: Write Anti-Patterns

Anti-Patterns are named failure modes — bad output the AI should recognize and flag.

> ❌ **Shallow:**
> "AP-1: Don't be biased."
> Too generic; what counts as "biased"?
>
> ✅ **Rigorous:**
> "AP-1: Affinity-Bias Smoothing — scoring a candidate higher on Culture Add because their background resembles the interviewer's (or the existing team's), framed as 'they'd fit in well here.' Detect: Culture Add scoring uses similarity language ('like us', 'understands our culture', 'shares our background') rather than additive language ('brings perspective on X that the team lacks'). Mitigation: re-score with explicit 'what does this person ADD?' framing."
> Specific behavior pattern; detection cue; mitigation path.

**Suggested Anti-Patterns:**

- **AP-1: Affinity-Bias Smoothing** — Culture Add inflated by background similarity (detection: similarity language)
- **AP-2: Years-of-Experience Trap** — Skill Match conflated with tenure (detection: scoring cites years rather than outcomes)
- **AP-3: Optimistic-Trajectory Inference** — Trajectory above 7/10 without prior growth evidence (detection: no growth examples cited)
- **AP-4: Compensation Self-Censorship** — avoiding the realism question because numbers are uncomfortable (detection: Compensation Realism scored without stating numbers)
- **AP-5: Interview-Quality Excuse** — using "we don't know" as a reason to score lower vs flagging Interview Signal Quality directly (detection: claims like "couldn't tell" or "hard to say" without flagging the upstream interview-process gap)

### Step 6: Build the Hypothesis Library

Hypothesis Library entries are testable starting points stated in the domain's vocabulary. They serve two roles: encoding the model author's working theories, and absorbing Governor-submitted hypotheses for explicit testing during sessions.

Each hypothesis follows: claim + result format + structured outcome states.

> ❌ **Shallow:**
> "HL-1: We should hire people who are smart."
> Not testable; "smart" is undefined; no result format.
>
> ✅ **Rigorous:**
> ```
> HL-1: Candidates with strong Outcome Track Record (≥3 measurable outcomes per
>   prior role) outperform candidates with strong Trajectory (high growth signal,
>   weaker track record) at the 12-month review point in our context.
>
> Result format: confirmed / not confirmed / insufficient data
> Test method: post-12-month review of recent hires; compare 12-month performance
>   ratings against hire-time scores on Outcome Track Record vs Trajectory.
> ```
> Testable claim; structured result format; concrete test method.

**Suggested Hypothesis Library entries:**

- **HL-1:** Outcome Track Record predicts 12-month performance better than Trajectory
- **HL-2:** Culture Add scoring above 6/10 correlates with team-velocity improvements within 6 months
- **HL-3:** Onboarding Risk above 7/10 correlates with first-90-day attrition
- **HL-4:** Compensation Realism mismatch >30% predicts offer rejection regardless of other scores
- **HL-5 (Governor-submitted):** [reserved for Governor's session-specific hypothesis — added at bootstrap]

### Step 7: Write the Guardrail Vocabulary

Guardrail Vocabulary lists reusable constraints that can be applied across tactics. These feed into the Operating Document's guardrail definitions.

> ✅ **Rigorous:**
> ```
> ### Guardrail Vocabulary
>
> **GV-1: Outcome-cite-required** (hard, mechanical)
>   Every Skill Match score above 7/10 must cite at least one measurable outcome
>   from the candidate's track record. Mechanical check: grep for outcome citation
>   format in scoring output.
>
> **GV-2: Affinity-flag** (soft, interpretive)
>   Culture Add scoring using similarity language triggers a review prompt asking
>   the scorer to re-frame in additive terms.
>
> **GV-3: Compensation-numbers-required** (hard, mechanical)
>   Compensation Realism scoring must state both the role band and the candidate's
>   expectation as numbers. Mechanical check: numeric pattern present in scoring
>   output.
>
> **GV-4: Interview-gap-disclosure** (soft, interpretive)
>   Interview Signal Quality below 6/10 must list specific interview-process gaps
>   that produced the low score.
> ```

These are reusable — any session that uses this domain model can pull guardrails directly from this vocabulary into the OD without re-authoring.

---

## Quality Gate Checklist

When you finish authoring, run this checklist before declaring the model ready:

- [ ] **All 6 components present** (Core Concepts, Concept Relationships, Quality Principles, Anti-Patterns, Hypothesis Library, Guardrail Vocabulary)
- [ ] **Primary source cited** with what's retained vs adapted
- [ ] **6–10 Core Concepts**, each with definition + boundary + misapplication
- [ ] **Concept Relationships** include at least one tension (probably more)
- [ ] **Quality Principles testable** — someone can verify violation by reading scoring output
- [ ] **Anti-Patterns specific** — each names a behavior pattern with detection cue
- [ ] **Hypothesis Library entries testable** with structured result format
- [ ] **Guardrail Vocabulary reusable** across multiple tactics
- [ ] **No session-private content** (Pattern 8: no specific candidate names, no real organization names if model is contributed back to framework)
- [ ] **Cross-model boundaries acknowledged** if model overlaps with other domain models in the same session

If multiple checks fail, the model needs another iteration before use.

---

## Common Authoring Mistakes

Patterns that produce weak domain models — recognize them in your draft:

### Mistake 1: Concepts Without Boundaries

A concept like "Skill Fit" without an explicit boundary is unreachable in deliberation — the AI can claim almost anything is or isn't "skill fit". Boundaries make the concept's scope visible and disputable.

### Mistake 2: Quality Principles That Aren't Testable

"Be rigorous" / "Be thorough" / "Use good judgment" — none are testable. A QP that requires interpretation to evaluate is not a QP; it's a tautology. Test: can someone reading the scoring output check whether the QP was honored?

### Mistake 3: Anti-Patterns That Are Inverse-of-QPs

If your QP-1 says "cite outcomes" and your AP-1 says "fail to cite outcomes" — that's redundant. AP-1 should be a distinct failure mode (e.g., "Affinity-Bias Smoothing") that the QPs don't directly catch.

### Mistake 4: Concept Relationships Missing Tensions

Tensions are the engine of cross-domain deliberation. A model with prerequisites and amplifiers but no tensions produces sessions that don't surface real conflicts. Test: does your model contain at least one "X and Y pull in opposite directions" relationship?

### Mistake 5: Hypothesis Library Too Generic

"We should hire smart people" / "Quality matters" — not testable. Hypotheses must state a claim in the model's vocabulary with a structured result format.

### Mistake 6: Guardrail Vocabulary Inheriting Session-Specific Labels

If your domain model is contributed back to the framework, guardrails like "G-7: Must satisfy our Q3 budget" leak session-specific content. Per Pattern 8, framework-contributed models use abstract guardrail names (`outcome-cite-required`) that any future session can adopt.

### Mistake 7: Missing Cross-Model Boundary Clarification

When two models overlap (e.g., "user-value" and "market-fit" both score willingness-to-pay), they double-count without explicit boundaries. Add a "Cross-model boundary" section declaring what THIS model owns and what an OVERLAPPING model owns.

---

## Iteration Patterns

### Pattern 1: Author Against One Session, Then Refine for Reuse

Domain models authored against a specific session are usually too session-specific. After running one session, look at where the model fell short and abstract — replace specific candidate names with generic placeholders, replace session-specific guardrail values with parameter slots.

### Pattern 2: Fork vs Extend

If you find a published domain model that's 70% right for your domain, fork it explicitly (cite the original; document what you changed) rather than authoring from scratch. The community gets cleaner derivation lineage; you save authoring time.

### Pattern 3: Versioning Your Models

Tag your model with a version (e.g., `hiring-rubric.md v0.3`) and a date. When you update, increment the version and document what changed in the model's "Authoring protocol" footer. Sessions inheriting your model can pin to a version.

### Pattern 4: Quality-Gate Before Use, Not After

Run the Quality Gate Checklist BEFORE using the model in a session. Models that fail the checklist mid-session produce friction — better to catch the gaps at authoring time.

---

## Authoring Time Budget

Realistic time budgets for first-time authors:

| Component | Time |
|---|---|
| Pick primary source + read enough to draft | 30 min |
| Core Concepts (6–10) | 30 min |
| Concept Relationships | 15 min |
| Quality Principles (4–6) | 20 min |
| Anti-Patterns (4–6) | 20 min |
| Hypothesis Library | 15 min |
| Guardrail Vocabulary | 10 min |
| Quality Gate Checklist + iteration | 20 min |
| **Total first-time** | **~2.5 hr** |

Drops to ~30–60 min once you've internalized the patterns. Models authored at this rigor pay back the investment immediately — sessions produce traceable, defensible decisions instead of generic-sounding output.

---

## Related

- [`cowork/domain-model-authoring-protocol.md`](../cowork/domain-model-authoring-protocol.md) — procedure document (this walkthrough is the teaching companion)
- [`cowork/templates/domain-model.md`](../cowork/templates/domain-model.md) — stub template
- [`domain-models/examples/`](../domain-models/examples/) — community-contributed example models
- [Examples — domain models in action](examples/) — see authored models in completed sessions
- [Glossary](glossary.md) — terminology lookup
- [Walkthrough](walkthrough.md) — first session in 10 minutes
- [Verification Patterns](../cowork/verification-patterns.md) — Pattern 8 (strip session-private content) applies when authoring models for framework contribution

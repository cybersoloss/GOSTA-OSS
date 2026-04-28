# Domain Model: [Domain Name]

**Source:** [Primary source — cite the original document, regulation, or book chapter. Use the actual source text, not summaries, interpretations, or experiment-derived files. Examples: "Regulation (EU) 2022/2554 — original text from EUR-Lex", "Michael Porter, Competitive Strategy — Chapter 2: Generic Competitive Strategies (28 pages)"]
**Enhancement Sources:** [Optional. Secondary sources consulted AFTER building from primary source. Examples: "sessions/example-project-v2/domain-models/value-creation.md — scoring criteria VC-1 through VC-12 reviewed for project-specific elements to incorporate"]
**Application Context:** [What session/domain this is written for. For reused models with Preserve adaptation intent: explain how this general-purpose lens serves the current session — this header is the only session-specific element.]
**Created:** [date]
**Purpose:** [[Model type: constraint | operational | craft | audience-facing] What evaluation criteria this model provides. Example: "[Audience-facing] Provides knowledge about what funding assessors value so that announcement content can naturally demonstrate alignment..."]

> **Authoring protocol:** Build the model entirely from the primary source first. Only consult enhancement sources after the 6-component structure is complete. Enhancement sources may add project-specific or session-specific elements but must not replace primary-source concepts. If no primary source document exists (e.g., domain expertise only), state "domain expertise" as source and note the limitation.
>
> **Knowledge vs. strategy (critical distinction):** Domain models encode what is *true* (knowledge), what *good* looks like (quality principles), and what is *forbidden* (guardrails). They do NOT encode what agents should *choose* — that is strategy, and strategy belongs to agents during deliberation. If you find yourself writing specific CTAs, content hooks, posting sequences, audience-to-channel mappings, structural templates, or tactical prescriptions in Core Concepts or Quality Principles, you are encoding strategy as knowledge and stealing the agent's deliberation space. Test: could an agent reasonably choose a *different* approach while still satisfying all Quality Principles and Guardrails? If not, the model is too prescriptive. Everything the model does not constrain is implicitly available for agents to decide.

**Vertical-Fit Validation (from GOSTA §8.7 V7):** When this domain model is inherited by a new session, run a concept-coverage check at Phase 1 entry: extract the new session's declared concept set (scope objectives + OD strategies + deliberation roster) and verify ≥70% of concepts have at least one matching reference in this domain model's §1 Core Concepts. Coverage below threshold: extend, accept-with-acknowledgment, or substitute. Generic-pass models that load without error but do not cover the session's concept set are NOT a substitute for vertical-fit-validated models.

---

## 1. Core Concepts
[3+ required minimum / 6+ recommended for full analytical depth. Organized by theme, not alphabetically. Each concept must include domain-specific implications for scoring/decision-making. Written as applied narrative, not encyclopedic definitions. Models with 3-5 concepts are viable but may produce fewer tensions during multi-domain assessment.]

**Distortion-prevention guidance (§14.3.2 retrieval faithfulness):** Agents cite these concepts during execution and deliberation. Concepts with vague boundaries get narrowed, broadened, or semantically drifted during application. To resist distortion:
- **Define the boundary.** State what the concept does NOT include, especially near-misses. Example: "Risk Reversal means removing barriers to the first transaction by reversing who bears the risk — free trials, money-back guarantees, proof-of-concept projects, performance guarantees. It does NOT include general discounting or promotional pricing, which reduce cost but don't shift risk."
- **Include application examples.** Show 2-3 concrete applications so agents don't fixate on one manifestation.
- **Flag common misapplications.** If a concept is frequently confused with something adjacent, say so. This is distinct from Anti-Patterns (§4) which cover domain-level mistakes; misapplication notes here cover concept-level misuse.

### [Concept Theme A]
[How this concept applies to the session's specific domain. What it means for feature scoring, tactic evaluation, or strategic decisions.]

### [Concept Theme B]
[Applied narrative...]

---

## 2. Concept Relationships
[How concepts interact. Focus on three relationship types:

1. **Prerequisites** — which concepts must be satisfied before others can operate? (e.g., "EU hosting must exist before any GDPR feature opportunity can be realized")
2. **Tensions** — where do concepts pull in opposing directions, especially across domain models? (e.g., "Value Creation's subscription form creates tension with Sales' self-serve transaction path when features produce one-time outputs")
3. **Amplifiers** — where does satisfying one concept strengthen another? (e.g., "Mature enforcement makes GDPR the lowest-friction entry point, amplifying the Iron Law's preference for existing markets")

Weak relationship sections list concepts without identifying the specific dependency, tension, or amplification between them.]

---

## 3. Quality Principles
[3+ required. What "good" looks like in this domain. Concrete, testable criteria — not abstract aspirations.]

- **QP-1:** [Principle] — [How to evaluate: what to look for, what counts as meeting this principle]
- **QP-2:** [Principle] — [Evaluation criteria]
- **QP-3:** [Principle] — [Evaluation criteria]

---

## 4. Anti-Patterns
[2+ required. What "bad" looks like. Common mistakes, false signals, or traps specific to this domain.]

- **AP-1:** [Anti-pattern] — [Why it's harmful, how to detect it, what to do instead]
- **AP-2:** [Anti-pattern] — [Detection and mitigation]

---

## 5. Hypothesis Library
[2+ required. Testable hypotheses that tactics in this domain commonly test. Pre-built starting points for tactic design.]

- **HL-1:** "If [action], then [outcome], because [reasoning from core concepts]"
- **HL-2:** "If [action], then [outcome], because [reasoning]"

---

## 6. Guardrail Vocabulary
[2+ required. Domain-specific constraints that should appear as guardrails in ODs operating in this domain.]

- **GV-1:** [Guardrail] — Severity: [hard | soft] — [Why this constraint matters in this domain]
- **GV-2:** [Guardrail] — Severity: [hard | soft] — [Reasoning]

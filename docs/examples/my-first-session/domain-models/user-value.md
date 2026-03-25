# Domain Model: User Value

**Source:** domain expertise — user behavior research, product analytics patterns
**Application Context:** my-first-session — feature prioritization for next quarter
**Created:** 2026-03-25
**Purpose:** Provides criteria for evaluating how users perceive, adopt, and derive value from features

---

## 1. Core Concepts

### Activation Distance
The friction required for a new user to realize value from a feature. Features with low activation distance are perceived as immediately useful; high-distance features require education campaigns, configuration, or context the user may not have.

**Domain-specific implications:** A feature with high Activation Distance is unlikely to drive organic adoption even if the underlying functionality is valuable. In quarter-based prioritization, features that require extensive onboarding (e.g., audit logging systems) compete against features users can activate within minutes (e.g., dark mode toggle).

**Boundary note:** Activation Distance does NOT include the feature's inherent quality or correctness — it's purely about the user's perception of "can I use this right now?" It excludes long-term learning curves; it's about the first 5 minutes.

**Common misapplication:** Confusing Activation Distance with feature complexity. A technically complex feature (API rate limiting) may have low Activation Distance if it solves an immediate pain point. A simple feature (dark mode) may have variable distance depending on discoverability.

### Retention Signal
Observable user behavior that indicates ongoing value extraction from a feature. Retention Signal is not adoption (did they use it once) — it's habituation (do they keep using it).

**Domain-specific implications:** Features with strong Retention Signals (e.g., dark mode once enabled) generate sustained engagement. Features with weak signals (audit logging, which is compliance-driven) may be adopted but never habitually used, making retention metrics noisy.

**Boundary note:** Retention Signal is behavioral, not declarative. It does not include survey responses like "I plan to use this." It includes repeat usage patterns, feature session counts, and time intervals between use.

**Common misapplication:** Treating adoption rate as Retention Signal. A feature may be adopted by 80% of users (high adoption) but used regularly by only 5% (weak Retention Signal).

### Perceived Complexity
How difficult users believe a feature is to use, independent of actual implementation complexity. User perception drives adoption more than objective difficulty.

**Domain-specific implications:** A feature perceived as complex creates psychological friction before the user even tries it. Even if UI is simple, features with domain-specific terminology (e.g., "API rate limiting") inherit the complexity perception of their domain.

**Boundary note:** Perceived Complexity is subjective. It's measured via user feedback, NPS comments, support ticket volume, or conversion funnels (% who click "try now" vs. % who actually install/enable). It does NOT equal code complexity.

**Common misapplication:** Assuming a feature that's technically simple (like a checkbox) is perceived as simple. If the feature solves a conceptually hard problem (quota allocation), users may perceive it as complex regardless of UI simplicity.

### WTP Indicator (Willingness to Pay)
Signal that a user would pay for a feature or perceives it as premium/valuable. WTP Indicator is an upstream proxy for user value — not whether they currently pay, but whether they would.

**Domain-specific implications:** Features with strong WTP Indicators (e.g., advanced audit logging for compliance-sensitive customers) can justify premium SKUs or upsells. Features with weak indicators (e.g., dark mode) are table stakes in modern SaaS and don't support pricing power.

**Boundary note:** WTP does NOT include current pricing strategy. It's the user's latent perception of value, measured via feature requests, upgrade conversion rates for feature-driven reasons, or stated preference in surveys.

**Common misapplication:** Confusing WTP with frequency of use. A feature may be used infrequently (audit logging, checked monthly) but have high WTP (because it's mandatory for compliance). Conversely, high-use features may have low WTP (expected as default, not premium).

### Segment Reach
The breadth of the user base that would benefit from this feature. Features with broad reach address problems common across customer segments; narrow-reach features solve point problems for a subset.

**Domain-specific implications:** In a finite quarter with limited development budget, broad-reach features compound value (benefit to 70% of users > benefit to 15% of users). Narrow-reach features may be high-impact for their segment but dilute quarter-level impact.

**Boundary note:** Reach is defined by addressable customer count, not by customer size. A feature reaching 100 SMB customers may have higher reach within the product (small user count) but address a large revenue cohort.

**Common misapplication:** Confusing Segment Reach with market size. Enterprise-focused features may have narrow reach within the product (small user count) but address a large revenue cohort.

### Habit Formation Potential
Likelihood that a feature becomes a regular behavior pattern once adopted. Features with high Habit Formation Potential enter user workflows and become sticky; features with low potential remain one-off utilities.

**Domain-specific implications:** Features designed into daily workflows (onboarding wizard, API rate limiting for developers) have higher Habit Formation Potential than features used on-demand (dark mode, bulk import). Features with strong Habit Formation Potential generate compounding retention and lower churn.

**Boundary note:** Habit Formation Potential is independent of perceived usefulness. A feature may solve an important problem (audit logging) but generate no habit (checked twice yearly). Another feature may be frivolous (dark mode) but generate daily habit (every session).

**Common misapplication:** Assuming high-frequency features have high Habit Formation Potential. A feature used 10 times could be 10 separate incidents (low habit) or a genuine daily behavior (high habit).

---

## 2. Concept Relationships

**Prerequisites:**
- Segment Reach must be established before assessing Retention Signal — if a feature reaches no one, retention is moot
- Perceived Complexity affects Activation Distance: high complexity → high Activation Distance (cannot activate what you don't understand)

**Tensions:**
- Activation Distance vs. Habit Formation Potential: features designed for quick activation (dark mode) may lack friction to cement habit; features requiring effort upfront (audit logging) may never activate enough to form habit
- Segment Reach vs. WTP Indicator: broad-reach features (dark mode, needed by everyone) often have weak WTP (expected as default); narrow-reach features (advanced audit logging) may have strong WTP from their segment

**Amplifiers:**
- Low Activation Distance amplifies Habit Formation Potential: if users can activate immediately, they're more likely to test the feature repeatedly, cementing habit
- Habit Formation Potential amplifies Retention Signal: habitual use produces observable recurring patterns
- Strong Retention Signal amplifies WTP Indicator: users who habitually use a feature are willing to pay more for it

---

## 3. Quality Principles

- **QP-1: User-Centric Framing** — Scoring must reference user mental models, not technical implementation details. A feature scored only on "API response time" without reference to what users perceive is QP-1 violation. Evaluation: does the score justify each concept choice by reference to how users experience or adopt the feature?

- **QP-2: Segment Specificity** — Scoring for Segment Reach must name the segments reached, not just "broad" or "narrow." Evaluation: is Segment Reach score accompanied by a list of affected customer types or personas?

- **QP-3: Signal Grounding** — Scores for Retention Signal must cite observable data (NPS comments, support tickets, usage patterns) or acknowledged empirical gaps. "High retention" without grounding is a violation. Evaluation: does the Retention Signal score cite specific types of behavioral evidence?

- **QP-4: Distinction from Implementation** — No score in this model should be determined by code complexity, technical elegance, or engineering effort. Those belong in the engineering-cost model. Evaluation: does any justification invoke technical implementation details rather than user behavior?

---

## 4. Anti-Patterns

- **AP-1: Adoption-Retention Conflation** — Assuming a feature with high adoption (% of users who tried it) automatically has high Retention Signal. Many features are adopted once and abandoned. Detection: score Adoption at 8/10 and Retention at 3/10 for the same feature. Mitigation: assess these independently. Look for evidence of repeat usage, not just initial try.

- **AP-2: Feature-Set Inference** — Assuming a feature solves a user problem because it's technically capable. "Audit logging exists; therefore, security-conscious users will adopt it." Detection: when scoring, justify Activation Distance and Segment Reach by reference to user behavior research or explicit customer feedback, not feature description. Mitigation: cite user interviews, support tickets, or stated feature requests.

- **AP-3: Premature Maturity Assumption** — Assuming a feature reaches maturity in its first quarter post-release. Early Activation Distance may be high; Habit Formation may take 2-3 quarters to surface. Detection: retroactively, when a feature's Retention Signal stalls in Q2 despite strong Q1 adoption. Mitigation: in prioritization, score based on potential, not maturity. Flag features as "first-quarter uncertain" if data is unavailable.

---

## 5. Hypothesis Library

- **HL-1:** "If we build an onboarding wizard, then new users' Activation Distance will drop below 2 minutes, because the wizard guides them through first-value-add step without requiring documentation reading." Testable by: session replay data, time-to-first-action metric, support ticket volume pre/post.

- **HL-2:** "If we implement bulk CSV import, then Segment Reach expands to non-technical users (operations, finance teams), because they can now load data without engineering intervention." Testable by: which user personas request this feature, support ticket patterns before/after.

- **HL-3:** "If we add dark mode, then Habit Formation Potential is high because every user session presents the toggle, creating repeated exposure and habit." Testable by: toggle frequency in session logs, retention cohort comparison (toggled vs. never-toggled users).

- **HL-4 [Governor-submitted]:** "Dark mode is a distraction — it will score below average on user-value concepts because it addresses aesthetic preference rather than functional gaps." Testable by: scoring dark mode against all six concepts, comparing to onboarding wizard and bulk CSV import, confirming hypothesis if user-value total for dark mode < average of other features.

---

## 6. Guardrail Vocabulary

- **GV-1: Evidence Anchoring** — Severity: hard — Do not score a feature's user-value without explicit reference to at least one form of evidence: user interviews, support tickets, feature request frequency, or cohort analytics. Guessing is not permitted. Why: user-value scoring is most susceptible to HiPPO bias and general-knowledge hallucination.

- **GV-2: Segment Transparency** — Severity: hard — When scoring Segment Reach, name the segments reached. If the feature reaches "all users," justify with business data (true for all SKUs? all geographies? all company sizes?). Why: preventing vague claims that expand reach artificially.

- **GV-3: Distinction Burden** — Severity: soft — If two concepts score identically for the same feature, re-examine whether the scoring is actually independent or whether one is redundant. Why: catching conflation patterns early.

# Domain Model: Engineering Cost

**Source:** domain expertise — software engineering estimation, technical debt research
**Application Context:** my-first-session — feature prioritization engineering assessment
**Created:** 2026-03-25
**Purpose:** Provides criteria for evaluating technical effort, risk, and maintenance burden of implementing features

---

## 1. Core Concepts

### Effort Estimate Confidence
The reliability of the engineering effort estimate for a feature. High confidence means the team has shipped similar features before and can predict implementation time accurately. Low confidence signals unknowns, novel architecture, or dependency complexity.

**Domain-specific implications:** In quarter-based planning with a single developer, a feature with low Effort Estimate Confidence carries disproportionate risk. A 3-week estimate with 80% confidence may be preferable to a 2-week estimate with 30% confidence. Low-confidence estimates tend to slip by 40-80%.

**Boundary note:** Confidence is not difficulty—a feature can be technically hard (high skill required) but high-confidence (predictable because similar work has been done). Conversely, a simple feature in an unfamiliar codebase may have low confidence.

**Common misapplication:** Confusing confidence with optimism. "I think we can do it in 2 weeks" is low-confidence estimation. "We've done 3 similar features; they averaged 2.5 weeks; this is 10% simpler" is higher confidence.

### Dependency Chain Length
The number of sequential dependencies that must be resolved before implementation can complete. Features with short chains (≤1 external dependency) can proceed in parallel with other work. Long chains (3+ dependencies) create bottlenecks and risk delays.

**Domain-specific implications:** With one developer, each external dependency (API changes, third-party library updates, customer data access) creates blocking wait. A feature dependent on 4 other features or external systems may sit idle for 2+ weeks waiting for prerequisites.

**Boundary note:** Dependency Chain Length is the *sequential* count, not the total count. A feature with 5 parallel dependencies (all available at once) has chain length 1. A feature with 2 sequential dependencies has chain length 2.

**Common misapplication:** Counting all dependencies as equal. A dependency on a library that's been stable for 2 years is lower risk than a dependency on a recently refactored internal API.

### Reversibility
The cost and complexity of undoing or rolling back a feature if it causes production issues or violates constraints. Easily reversible features can ship with lower review gates; irreversible features need more testing.

**Domain-specific implications:** A feature that modifies user data storage schema (audit logging, bulk import) is partially irreversible — rolling back deletes history. A feature that's purely additive (dark mode, new button) is fully reversible. The constraint "no breaking changes to public API" makes some features unreversible if they touch the API contract.

**Boundary note:** Reversibility is about operational risk, not code quality. Clean code doesn't make a feature more reversible if it modifies persistent data.

**Common misapplication:** Assuming stateless features are fully reversible. A feature that changes query patterns or caching behavior may cause performance regressions that persist even after code is reverted if the issue is cached downstream.

### Maintenance Burden
The ongoing operational cost to keep a feature working post-launch: monitoring, bug fixes, customer support, compliance updates, dependency maintenance.

**Domain-specific implications:** A feature like audit logging generates indefinite support overhead (customers calling about audit queries, compliance questions). A feature like dark mode has minimal ongoing burden (toggle works or doesn't). In a small team, ongoing burden compounds — 5 features each adding 2 hours/quarter of maintenance burden consume 2.5 weeks of annual engineering time.

**Boundary note:** Maintenance Burden is not feature development time. It's post-launch operational cost.

**Common misapplication:** Assuming mature, battle-tested features have zero maintenance burden. A widely-used feature may attract edge-case bug reports that require investigation even if the core feature is solid.

### Technical Debt Multiplier
The degree to which implementing this feature creates technical debt that impairs future velocity. Features that require workarounds, create complexity in other systems, or delay architectural improvements generate higher multipliers.

**Domain-specific implications:** Building audit logging with a quick schema patch multiplies debt (1.8x) — it blocks future database refactoring. Building it with a proper event streaming architecture adds only 30% overhead now but prevents 6 months of future slowdown. The short-term cost difference (2 weeks vs 3 weeks) is offset by future impact.

**Boundary note:** Technical Debt Multiplier is not implementation quality. A well-written quick implementation can still generate debt if it takes a shortcut that future features must work around.

**Common misapplication:** Assuming architectural perfection prevents debt. Sometimes a good-enough implementation is right (dark mode doesn't need event streaming). The multiplier captures whether this specific feature choice blocks or enables future work.

### Integration Surface Area
The number of existing systems or APIs that this feature touches or must integrate with. Features with large surface areas are more likely to break existing functionality or create unexpected interactions.

**Domain-specific implications:** A dark mode feature touches UI layer only (surface area: 1). Bulk CSV import touches data validation, import queue, user notification, and activity log (surface area: 4). Larger surface areas require broader testing and create more opportunities for regressions.

**Boundary note:** Surface Area is structural, not about code quality. A well-isolated feature that touches 5 systems still has surface area 5 and carries integration risk.

**Common misapplication:** Assuming well-tested systems are safe integration targets. A battle-tested API can still have undocumented edge cases that a new integration trigger.

---

## 2. Concept Relationships

**Prerequisites:**
- Dependency Chain Length must be resolved before Effort Estimate Confidence can be finalized — if dependencies are still unknown, estimates are provisional
- Integration Surface Area affects Reversibility: larger surface areas make rollback riskier and more complex

**Tensions:**
- Effort Estimate Confidence vs. Dependency Chain Length: a simple feature (high confidence) may have a long chain (high cost); a complex feature (low confidence) may be independent (low chain length)
- Reversibility vs. Maintenance Burden: fully reversible features are easy to roll back but may generate support overhead once live; hard-to-reverse features require careful testing but may have lower ongoing burden once proven stable
- Technical Debt Multiplier vs. Effort Estimate: choosing the high-debt-multiplier approach saves 1-2 weeks now but costs 4+ weeks in future velocity lost

**Amplifiers:**
- Long Dependency Chain Length amplifies Effort Estimate Confidence degradation: the longer the chain, the more unknowns, the lower the confidence
- Large Integration Surface Area amplifies Maintenance Burden: more systems touched = more potential edge cases = more support tickets
- High Technical Debt Multiplier amplifies future Effort Estimate cost: a multiplier of 2.0x means future features estimate 2x higher effort

---

## 3. Quality Principles

- **QP-1: Dependency Transparency** — Before scoring Dependency Chain Length, list every external dependency explicitly. "API changes required" is vague; "API v2 rollout scheduled for May 15; we depend on it" is transparent. Evaluation: does the score include a dependency list that's been reviewed against the technical roadmap?

- **QP-2: Evidence-Based Estimation** — Effort estimates must be calibrated against historical data. "We think 3 weeks" without reference to similar work is QP-2 violation. Evaluation: is the effort estimate tied to a historical baseline (e.g., "dark mode took 5 days on product X; this codebase is 30% more complex")?

- **QP-3: Debt Explicitness** — If a feature's Technical Debt Multiplier is >1.2, the scoring must name the specific debt (e.g., "blocks Q3 database migration," "creates tight coupling to queue system"). Generic "architectural debt" is insufficient. Evaluation: does each high-multiplier feature explain the debt it generates?

- **QP-4: Single-Developer Constraint Awareness** — All scores must account for the constraint: one developer, no parallelization. A feature that would be 5 weeks for a 2-person team is not 5 weeks in this context. Evaluation: does the estimate account for serial execution and context switching costs?

---

## 4. Anti-Patterns

- **AP-1: Optimism Bias in Estimates** — Systematic underestimation of effort, especially for features that sound simple ("dark mode — just a CSS toggle"). Research shows estimates cluster 20-40% too low. Detection: compare estimate against team's historical estimate velocity and ask whether this feature is truly simpler than historical benchmarks. Mitigation: add 30% buffer to low-confidence estimates automatically.

- **AP-2: Ignoring Dependency Wake-Up Risk** — Assuming dependencies will be ready on schedule. Third-party libraries, API changes, and infrastructure projects slip. Detection: if a feature's Effort Chain Length depends on something controlled outside the team and no slip plan exists, flag as high-risk. Mitigation: add 2-week contingency for each external dependency.

- **AP-3: Reversibility Overconfidence** — Assuming a feature can be "turned off" or "reverted" without understanding the downstream impact. A feature that modifies how data is stored or queried may require migration even after code removal. Detection: ask "if this feature ships and creates a production incident in week 6, can we restore the system to pre-incident state in under 4 hours?" If the answer is no or uncertain, reversibility is low. Mitigation: design with explicit rollback procedures (feature flags, data migration reversals) before implementation.

---

## 5. Hypothesis Library

- **HL-1:** "If we implement API rate limiting, then Integration Surface Area will be medium (3-4 systems) and Effort Estimate Confidence will be high (we've done quota systems before), resulting in 3-3.5 weeks of work." Testable by: comparing actual development time to estimate, validating surface area assumptions during implementation.

- **HL-2:** "If we implement bulk CSV import, then Dependency Chain Length will be 1 (only data validation upstream) because import can happen asynchronously, resulting in reduced blocking risk." Testable by: dependency analysis during design phase, comparing to features with longer chains.

- **HL-3:** "If we implement dark mode, then Reversibility will be high (feature flag gating the entire dark mode path), Technical Debt Multiplier will be low (CSS, no architecture changes), and Maintenance Burden will be minimal." Testable by: post-launch monitoring of support tickets and maintenance time.

- **HL-4:** "If we implement audit logging without a proper event streaming architecture, then Technical Debt Multiplier will be 1.6x because future logging features will have to work around the schema, costing 2-3 weeks of velocity drag per quarter." Testable by: comparing audit logging maintenance hours quarter-over-quarter with other features, measuring velocity impact on other features that touch the audit schema.

---

## 6. Guardrail Vocabulary

- **GV-1: Single-Developer Serialization** — Severity: hard — All effort estimates must assume serial execution (one developer can only do one thing at a time). No parallelization. Effort estimates that assume concurrent work are non-compliant. Why: violates hard constraint.

- **GV-2: Dependency Declaration** — Severity: hard — Features with Dependency Chain Length > 0 must name each dependency and declare its expected completion date. Dependencies without dates are flagged as unknown and estimates are marked "provisional." Why: prevents silent risk accumulation.

- **GV-3: Reversibility Test** — Severity: soft — For features with Reversibility < 7/10 (partially reversible or irreversible), a rollback procedure must be designed and reviewed by Governor before implementation proceeds. Why: preventing production incidents without recovery paths.

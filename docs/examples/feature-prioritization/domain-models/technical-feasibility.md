# Domain Model: Technical Feasibility

**Source:** Domain expertise — synthesized from software architecture assessment practices, technical debt literature (Cunningham's original metaphor, Martin Fowler's quadrant), and infrastructure scaling patterns
**Application Context:** Evaluating implementation cost, risk, and architectural impact of features for roadmap sequencing
**Created:** 2026-03-25
**Purpose:** Grounds AI agent reasoning in engineering reality when scoring features — prevents market-driven prioritization from ignoring implementation constraints that determine actual delivery

---

## 1. Core Concepts

### Dependency Depth

The number of prerequisite systems, components, or capabilities that must exist before a feature can be built. Features with deep dependency chains carry compounding risk — each prerequisite can delay or block the entire chain. Dependency depth is not the same as effort: a high-effort feature with zero dependencies is more predictable than a low-effort feature with three prerequisites, two of which don't exist yet.

**Boundary:** Dependency depth covers technical prerequisites within the system. It does NOT cover organizational dependencies (team availability, hiring, vendor contracts), which are resource constraints, not technical ones.

**Common misapplication:** Counting only direct dependencies. Feature A depends on Service B, which depends on Database Migration C, which depends on Infrastructure Upgrade D. The depth is 3, not 1. Teams routinely undercount by stopping at the first level.

### Architectural Congruence

The degree to which a feature aligns with the existing system architecture versus requiring architectural changes. High-congruence features fit within current patterns — they use existing APIs, follow established data flows, and don't introduce new infrastructure components. Low-congruence features require new patterns, new infrastructure, or changes to existing contracts between services.

**Boundary:** Architectural congruence covers system design alignment. It does NOT cover code quality or developer experience. A feature can be architecturally congruent and still be implemented poorly.

**Common misapplication:** Equating "uses existing technology" with architectural congruence. A feature can use existing technology while fundamentally violating the system's data flow assumptions. Congruence is about patterns, not tools.

### Technical Debt Load

The accumulated cost of past implementation shortcuts that affect a feature's development area. Features built in high-debt areas take longer, break more things, and produce less predictable outcomes. Technical debt load should inflate effort estimates and risk assessments for features that touch affected components.

**Boundary:** Technical debt load covers code and architectural shortcuts that increase future development cost. It does NOT cover feature gaps, missing documentation, or inadequate testing — those are quality deficits, not debt. The distinction matters: debt was a deliberate or inadvertent shortcut; quality deficits are things that were never built.

### Reversibility

How easily a feature can be rolled back, modified, or removed after deployment. Highly reversible features (feature flags, A/B testable, isolated components) carry less risk than irreversible ones (database schema changes, public API contracts, data format migrations). Reversibility should be a scoring factor because it determines the cost of being wrong.

**Boundary:** Reversibility covers technical rollback capability. It does NOT cover business reversibility (customer expectations, contractual commitments, market positioning). A feature can be technically reversible but practically irreversible if customers depend on it.

### Scalability Trajectory

Whether a feature's resource consumption grows linearly, polynomially, or exponentially with usage. Features with non-linear scaling trajectories create infrastructure time bombs — they work fine at current load but fail at 3x or 10x. Scalability trajectory should be assessed during prioritization, not after launch.

**Boundary:** Scalability trajectory covers computational resource consumption (CPU, memory, storage, network). It does NOT cover operational complexity (monitoring, debugging, incident response), which is a separate concern.

### Integration Surface Area

The number of external systems, APIs, or third-party services a feature touches. Larger integration surface area means more failure modes, more version compatibility issues, and more maintenance burden from external changes outside your control.

**Boundary:** Integration surface area covers external technical interfaces. It does NOT cover internal module boundaries, which are under your control and can be refactored.

---

## 2. Concept Relationships

**Prerequisites:** Technical Debt Load must be assessed before Dependency Depth is meaningful — a dependency chain through high-debt components has different risk than the same chain through clean components. Architectural Congruence assessment requires current architecture documentation; without it, congruence claims are speculation.

**Tensions:** Reversibility creates tension with Architectural Congruence — the most congruent approach (extend existing patterns) is often the least reversible (deeply embedded in existing flows). Scalability Trajectory optimization creates tension with delivery speed — building for 10x scale takes longer than building for current scale. Integration Surface Area reduction (fewer external dependencies) creates tension with market demands for integrations.

**Amplifiers:** High Reversibility amplifies willingness to attempt uncertain features — if rollback is cheap, the cost of failure drops. Low Technical Debt Load amplifies estimation accuracy — predictions in clean codebases are more reliable.

---

## 3. Quality Principles

- **QP-1:** Effort estimates for features in high-debt areas must include a debt-load multiplier (1.5x–3x depending on assessed debt severity). Estimates without this adjustment are systematically optimistic.
- **QP-2:** Dependency chains must be enumerated to full depth, not just direct dependencies. Any chain >2 deep requires explicit risk assessment.
- **QP-3:** Architectural congruence claims must reference specific system components and patterns. "This fits our architecture" without naming the patterns and interfaces is not an assessment.
- **QP-4:** Scalability trajectory must be stated for every feature that processes user data or handles concurrent requests. "It'll scale" without specifying the trajectory (linear, O(n log n), quadratic) is not an assessment.

---

## 4. Anti-Patterns

- **AP-1:** Dependency blindness — Approving features without mapping their full dependency chain, then discovering mid-implementation that a prerequisite doesn't exist. Detect by checking whether the first week of implementation reveals "unexpected" blockers. If this happens regularly, dependency analysis is being skipped or performed superficially.
- **AP-2:** Debt denial — Estimating features as if the codebase were clean when it isn't. Produces systematic underestimation. Detect by comparing estimated vs. actual delivery time for features in known high-debt areas. If actuals consistently exceed estimates by >50%, debt denial is operating.
- **AP-3:** Scale-later thinking — Shipping features with known non-linear scalability trajectories under the assumption that "we'll optimize later." Later rarely comes before the scaling failure does. Detect by checking whether any shipped feature in the last 6 months has caused a scaling incident.

---

## 5. Hypothesis Library

- **HL-1:** "If we reduce the dependency depth of Feature X by extracting Service B into an independent module first, then Feature X delivery time will decrease by 40% and risk by 60%, because Dependency Depth predicts that shallower chains have fewer failure modes."
- **HL-2:** "If we add feature flags to all features touching the billing system (high-debt area), then incident rate from billing deployments will decrease by 50%, because Reversibility predicts that cheap rollback reduces the blast radius of errors in high-debt code."

---

## 6. Guardrail Vocabulary

- **GV-1:** Dependency depth limit — Severity: soft — Features with dependency chains >3 deep require explicit risk mitigation plan. Chains >5 deep require Governor approval with architectural review. Recovery: decompose into smaller deliverables that reduce chain length.
- **GV-2:** Irreversibility gate — Severity: hard — Features involving database schema changes, public API contract changes, or data format migrations must pass an irreversibility review before development begins. The review documents rollback cost, data migration reversibility, and customer impact of reversal.
- **GV-3:** Debt area multiplier — Severity: soft — Effort estimates for features in identified high-debt components must apply a minimum 1.5x multiplier. Estimates submitted without the multiplier are flagged for recalibration.

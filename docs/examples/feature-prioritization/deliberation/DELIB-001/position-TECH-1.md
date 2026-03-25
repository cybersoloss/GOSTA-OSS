# Position Paper: TECH-1 (Technical Feasibility)
**Deliberation:** DELIB-001 | **Round:** 1 | **Date:** 2026-03-19
**Domain Model:** technical-feasibility | **Evaluation Target:** 12 candidate features (F-01 through F-12)

---

## Domain Concepts Applied

| Concept | Definition (from model) | How It Applies |
|---------|------------------------|----------------|
| Dependency Depth | Number of prerequisite systems that must exist before a feature can be built | F-05 depends on F-08 (depth 1). F-07 depends on event pipeline AND data warehouse (depth 2, parallel). F-12 depends on WebSocket infrastructure AND CRDT engine (depth 2, neither exists). |
| Architectural Congruence | Degree of alignment with existing system architecture | F-03 (Templates), F-04 (Slack) are high-congruence — they extend existing patterns. F-12 (Real-Time Collab) is fundamentally low-congruence — introduces CRDT, WebSockets, presence protocol. F-01 (EU Residency) requires infrastructure-level changes outside application architecture. |
| Technical Debt Load | Accumulated cost of shortcuts in the feature's development area | Identity service (affects F-06, F-10) is a known high-debt area — last 3 features touching it exceeded estimates by 80%. Data catalog (affects F-02, F-11) has moderate debt. Billing system (not directly involved) is highest debt but not in scope. |
| Reversibility | How easily a feature can be rolled back after deployment | F-01 (EU Residency) is LOW reversibility — infrastructure migration is effectively permanent. F-12 (CRDT) is LOW — data format changes are irreversible. F-03 (Templates) is HIGH — feature-flaggable, isolated. F-04 (Slack) is MEDIUM — webhook contracts are removable but customers depend on them quickly. |
| Scalability Trajectory | How resource consumption grows with usage | F-07 (Analytics Dashboard) has polynomial scaling risk — real-time aggregation over growing event volume. F-12 (Real-Time Collab) has potential exponential scaling with concurrent users per document. F-09 (Workflow Automation) is linear if well-designed but execution engine could become O(n²) with complex rule chains. |
| Integration Surface Area | Number of external systems, APIs, or third-party services touched | F-04 (Slack) adds 1 external dependency (Slack API — version changes, rate limits). F-10 (SSO/SAML) adds N external dependencies (each customer's IdP). F-01 (EU Residency) interacts with cloud provider infrastructure APIs. |

## Feature Scores (1-10 scale, feasibility perspective — higher = more feasible/lower risk)

| Feature | Score | Effort (FTE-weeks) | Rationale |
|---------|-------|-------------------|-----------|
| F-01: EU Data Residency | **3** | 12-16 | Infrastructure migration. Low reversibility. Not an application feature — it's an infrastructure project. Dependency depth 0 but effort is dominated by migration complexity, not code. Cloud provider coordination required (integration surface area). |
| F-02: Automated DSAR Pipeline | **5** | 6-8 | Depends on data catalog (exists but has moderate debt — apply 1.5x multiplier → 9-12 effective weeks). Requires identity resolution across services. Architecturally congruent with existing data flow patterns. Medium reversibility. |
| F-03: In-App Templates | **9** | 2-3 | High architectural congruence — extends existing project creation flow. Zero dependency depth. High reversibility (feature flag). No scaling concerns. Low-debt area. This is the most technically straightforward feature in the list. |
| F-04: Slack Integration | **8** | 3-4 | High congruence — webhook infrastructure exists. Dependency depth 0. One external dependency (Slack API) — manageable but adds maintenance burden. High reversibility. Linear scaling. |
| F-05: AI Code Review | **5** | 8-10 | Dependency depth 1 (requires F-08 for EU compliance). LLM integration adds integration surface area (model provider API). Scalability trajectory depends on model hosting — could be expensive at scale. Architecturally new pattern (no existing LLM integration). Medium reversibility (can feature-flag, but model contracts are sticky). |
| F-06: RBAC | **4** | 8-12 | Touches identity service — HIGH debt area (1.5x multiplier → 12-18 effective weeks). Dependency depth 1 (identity service refactor). Low reversibility — permission models are deeply embedded once shipped. Architecturally invasive — touches every API endpoint's authorization logic. |
| F-07: Usage Analytics | **5** | 6-8 | Dependency depth 2 (event pipeline + data warehouse, parallel). Polynomial scalability risk on real-time aggregation. Medium congruence — new infrastructure pattern (analytics pipeline). Medium reversibility. |
| F-08: AI Act Transparency | **7** | 3-4 | Dependency depth 0. Architecturally contained — model card generation is a new but isolated module. High reversibility. No scaling concerns (runs on model deployment, not per-request). Clean code area. |
| F-09: Custom Workflows | **4** | 10-14 | New architectural pattern (workflow engine). Scalability risk on rule execution (potential O(n²) with complex chains). Dependency depth 0 but massive scope — workflow engines are notoriously underestimated. Medium reversibility. Would benefit from A/B testing with limited rule complexity first. |
| F-10: SSO/SAML | **4** | 6-10 | Touches identity service — HIGH debt area (1.5x multiplier → 9-15 effective weeks). Integration surface area: N external IdPs, each with configuration variance. Low reversibility once enterprise customers configure SSO. Dependency shares F-06's identity refactor prerequisite. |
| F-11: Bulk Data Export | **7** | 3-4 | Depends on data catalog (moderate debt). Architecturally congruent — batch job pattern exists. High reversibility. Linear scaling. Low complexity. |
| F-12: Real-Time Collaboration | **2** | 16-24 | Lowest feasibility score. Dependency depth 2 (WebSocket infrastructure + CRDT engine, neither exists). Fundamentally new architectural pattern. Low reversibility (data format migration). Potential exponential scaling. No team experience with CRDTs. This is a 1-2 quarter project by itself. |

## Key Technical Tensions

1. **F-06 and F-10 share the identity service refactor prerequisite.** Building one without the other wastes the refactor investment. But building both in the same quarter risks 24-33 effective FTE-weeks on a single high-debt subsystem. Technical recommendation: sequence them together but in dedicated sprints with the refactor as Phase 0.

2. **F-12 is technically the riskiest feature by a wide margin.** CRDT implementation, WebSocket infrastructure, and presence protocol are all new patterns. Estimated 16-24 FTE-weeks is already aggressive — AP-2 (debt denial) risk is high because the team has no baseline for CRDT work. If market demand is strong, recommend a proof-of-concept sprint (2-3 weeks) before committing to full build.

3. **F-01 is infrastructure, not application.** It doesn't follow normal development patterns — it's a cloud migration project. Effort estimates have wider variance (12-16 weeks but could be 20+ with unexpected provider issues). Integration surface area is high and partially outside our control.

4. **F-05 → F-08 dependency creates a regulatory-technical coupling.** F-08 is technically simple (score 7) but F-05 cannot ship to EU without it. If market prioritizes F-05 in Q2, F-08 must precede it — this is a hard sequencing constraint regardless of F-08's market score.

## Recommended Priority (Technical Domain Only)

**Tier 1 (low-risk, high-feasibility — build first):** F-03, F-04, F-08, F-11
**Tier 2 (moderate risk — build with planning):** F-02, F-05, F-07
**Tier 3 (high risk — build with dedicated investment):** F-06 + F-10 (paired), F-09
**Tier 4 (very high risk — requires proof-of-concept first):** F-01, F-12

**Effort summary for Tier 1+2:** ~31-41 FTE-weeks (roughly 2 FTE-quarters). Tiers 1-3 total: 57-86 FTE-weeks (3.5-5.4 FTE-quarters — exceeds G-3 ceiling). Cannot build everything. Tier 4 alone could consume 28-40 FTE-weeks.

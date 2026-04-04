# Scope Definition: Feature Prioritization — EU Developer Tools SaaS

**Created:** 2026-03-18 | **Governor:** VP Product
**Scope Type:** finite
**Complexity:** complex
**GOSTA Version:** v6.1
**Cowork Protocol:** v3.12
**Deliberation Protocol:** v0.8
**Mode:** cowork
**Deliberation Mode:** enabled

## What This Session Is

This session conducts a multi-domain feature prioritization for a B2B developer tools SaaS expanding into the EU market. Twelve candidate features are evaluated across three domains — market-fit, technical-feasibility, and regulatory-compliance — using structured multi-agent deliberation with 5 agents. The session produces a scored feature matrix and a phased 2-quarter (Q2–Q3 2026) roadmap that accounts for dependency chains, compliance prerequisites, and effort constraints.

The scope is deliberately complex: 12 features, 3 domain models, 16 core concepts, 5 deliberation agents, and 6 guardrails. This exercises GOSTA's cross-domain deliberation, prerequisite chain enforcement, and segment concentration analysis capabilities.

## Why GOSTA

Without structured governance, this prioritization would collapse into either (a) market-driven sequencing that ignores regulatory prerequisites (shipping F-05 before F-08, violating the AI Act transparency requirement), or (b) compliance-driven sequencing that over-invests in regulatory features at the expense of market traction. The three-domain deliberation surfaces these tensions explicitly rather than letting one domain silently dominate.

Specific failure modes GOSTA prevents:

- **Prerequisite chain violations** — G-1 enforces that no feature ships before its compliance dependencies are met
- **Effort overcommit** — G-3 caps total engineering effort to prevent aspirational roadmaps
- **Segment concentration** — G-4 flags when Enterprise features consume >50% of investment
- **Activation regression** — G-2 ensures no shipped feature makes the product harder to start using
- **Sycophancy in deliberation** — Position independence verification detects when domain agents converge without genuine agreement

## Domain Models Required

| Domain Model | Source | Purpose |
|---|---|---|
| market-fit | Domain expertise — SaaS market dynamics, competitive analysis, B2B customer research | Evaluates market demand, competitive pressure, segment concentration, and willingness-to-pay signals. 6 concepts: Activation Distance, Switching Cost Asymmetry, WTP Signal, Market Timing Sensitivity, Segment Concentration Risk, Competitive Parity Gap. |
| technical-feasibility | Domain expertise — software architecture, estimation research, technical debt literature | Evaluates engineering effort, risk, architectural fit, and maintenance burden. 6 concepts: Dependency Depth, Architectural Congruence, Technical Debt Load, Reversibility, Scalability Trajectory, Integration Surface Area. |
| regulatory-compliance | Domain expertise — GDPR, EU AI Act, DPA enforcement patterns, data sovereignty requirements | Evaluates compliance obligations, enforcement probability, and regulatory change velocity. 4 concepts: Enforcement Probability Gradient, Data Flow Sovereignty, Compliance Prerequisite Chain, Regulatory Change Velocity. |

## Success Criteria

- All 12 features assessed with ≥3 independent domain scores each (G-6)
- Cross-domain tensions explicitly documented with disagreement classification
- Dependency chains mapped — no feature sequenced before its prerequisites
- Final roadmap fits within 2.4 FTE-quarter effort ceiling (G-3)
- Segment concentration analysis completed (G-4)
- Governor resolves all structured decisions with documented rationale
- Phased roadmap for Q2 and Q3 delivered with effort ranges and risk flags

## Constraints

- **Timeline:** 2 quarters (Q2–Q3 2026) for implementation roadmap
- **Budget:** 2.4 FTE-quarters total engineering effort (G-3)
- **Staffing:** Engineering team available; infrastructure team availability TBD (determines F-01 feasibility)
- **Regulatory:** EU AI Act and GDPR compliance non-negotiable for EU market features
- **Governance:** VP Product (Governor) available for 3 review touchpoints per week

## Risk Factors

- **Infrastructure team availability** — F-01 (EU Data Residency) requires infrastructure team; if unavailable, Q2 plan needs restructuring → maps to: DECISION-1 in deliberation synthesis
- **Effort estimation uncertainty** — Features touching high-debt components (identity service, data pipeline) carry inherent estimation risk → maps to: G-5 (≥1.5x debt multiplier)
- **Regulatory timeline pressure** — AI Act enforcement timeline may accelerate, increasing urgency for F-08 → maps to: G-1 (compliance prerequisite enforcement)
- **Segment concentration** — EU regulatory features structurally bias toward Enterprise segment → maps to: G-4 (50% concentration cap, soft)
- **CRDT expertise gap** — F-12 (Real-Time Collaboration) requires expertise the team doesn't have → maps to: DECISION-4 (POC vs. defer)

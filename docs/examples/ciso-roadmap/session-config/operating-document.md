# Operating Document: CISO Priorities 2026 — Multi-Domain Assessment
**Version:** 1 | **Date:** 2026-04-08 | **Governor:** Murat
**Scope Type:** finite | **Graduation Stage:** 1

## Goal
Produce a multi-domain CISO priority assessment for EU-based mid-market organizations (50-500 employees) that surfaces cross-domain tensions, competing priorities, and sequencing constraints that single-domain or single-prompt analyses miss. The assessment will serve as the Level 4 (GOSTA) output in a 4-level comparison article demonstrating the value of structured deliberation over generic prompting.

### Guardrails
- **G-1:** All regulatory claims must cite specific articles/sections from applicable legislation, not general regulatory references | Severity: hard | Evaluation: interpretive | Threshold: zero uncited regulatory claims
- **G-2:** No priority recommendation shall require more cumulative FTE than realistic mid-market security staffing (0.5–3 FTE) | Severity: hard | Evaluation: interpretive | Threshold: total FTE demand across top-5 priorities ≤ 3 FTE
- **G-3:** Threat claims must be grounded in EU-specific data (ENISA, Europol, national CERTs), not US-centric or vendor-sponsored sources alone | Severity: soft | Evaluation: interpretive | Threshold: ≥80% of threat citations from EU-specific sources
  - Recovery: Flag vendor-sourced claims and add EU-specific corroboration or annotation
- **G-4:** Every recommended priority must trace to at least one specific business process or revenue stream it protects | Severity: soft | Evaluation: interpretive | Threshold: zero priorities without business-impact traceability
  - Recovery: Add business-impact statement to any priority lacking one

## Objectives

### OBJ-1: Multi-Domain CISO Priority Assessment
- **Analytical Question:** What should an EU-based mid-market CISO (50-500 employees) prioritize in 2026, and why does the answer change when regulatory compliance, threat landscape, operational capacity, business continuity, technology architecture, and supply chain risk are assessed simultaneously rather than independently?
- **Acceptance Criteria:** All 6 domain models applied; cross-domain tensions explicitly identified and resolved; priority sequencing accounts for execution bandwidth constraints; at least 3 non-obvious insights that single-domain analysis would miss
- **Deliverable:** Priority assessment document with: (a) prioritized list with multi-domain reasoning, (b) tension map showing where domains pull in different directions, (c) sequencing recommendation accounting for execution bandwidth, (d) explicit comparison to what a single-domain or generic analysis would produce
- **Quality Standard:** Every priority cites specific domain model concepts from ≥2 domain models; every tension identifies the pulling domains and resolution rationale; sequencing respects operational capacity constraints
- **Priority:** critical

## Strategies

### STR-1: Multi-Agent Deliberation with Domain Model Stacking → serves OBJ-1
- **Rationale:** The analytical question requires simultaneous consideration of 6 domains that create non-obvious tensions. Single-perspective analysis produces plausible-sounding priorities that collapse when cross-domain constraints are applied. Multi-agent deliberation with independence level 2 forces each domain perspective to surface before premature convergence.
- **What Must Be True (WMBT):** Domain models are sufficiently rich to produce genuine tensions (not just complementary perspectives). Deliberation agents operate with enough independence to surface disagreements rather than converge prematurely.
- **Not Doing:** Product-specific recommendations (no vendor names). Implementation-level technical guidance (no step-by-step howtos). Specific organizational assessment (this is a generalized mid-market analysis, not a pentest report).
- **Kill Signal:** If deliberation produces the same priority order as generic prompting (Levels 1-2), the strategy has failed to add value.
- **Relationship to sibling strategies:** sole strategy
- **Authorized By:** GOV-session-1

## Tactics

### TAC-1: Domain-Stacked Deliberation → serves STR-1
- **Parent Strategy:** STR-1
- **Parent Objective:** OBJ-1
- **Hypothesis:** If we run multi-agent deliberation where each agent perspective is grounded in 2-3 domain models with forced cross-domain tension identification, then we will produce priority recommendations with explicit trade-off reasoning that generic single-prompt analysis cannot produce.
- **Kill Condition:** Deliverable not accepted after 3 revision cycles
- **Success Metrics:** (a) Number of cross-domain tensions identified (target: ≥5), (b) Number of non-obvious priority reorderings compared to generic analysis (target: ≥3), (c) Governor assessment of analytical depth vs. Level 1-3 outputs
- **Guardrails (inherited):** G-1, G-2, G-3, G-4
- **Guardrails (own):** None
- **Timeline:** 2026-04-08 (single session)
- **Bootstrap Cycles:** 0 (finite analytical — no cycles)
- **Seed Actions:** Execute phases sequentially
- **Owner:** AI
- **Approach:** Three-agent deliberation (Analyst, Challenger, Synthesizer) with domain model stacking. Each agent grounds arguments in specific domain model concepts. Deliberation follows independence level 2 (agents see each other's output but must maintain independent positions through round 2 before convergence in round 3).
- **Dependencies:** execution
- **Domain Model Dependencies:** regulatory-compliance (concepts: Article 21 Minimum Measures, Transposition Fragmentation, Cross-Compliance Efficiency, Reporting Timeline Cascade), threat-landscape (concepts: Ransomware, Credential Abuse, Supply Chain Multiplier, Threat Actor Convergence), operational-capacity (concepts: Security Staffing Cliff, Budget Reality, Execution Bandwidth, Maturity Asymmetry), business-value-continuity (concepts: Crown Jewel Identification, Recovery Time Reality, Revenue Insurance, Supply Chain Qualification), technology-architecture (concepts: Microsoft Monoculture, Identity as Control Plane, SaaS Dependency, Asset Inventory), supply-chain-risk (concepts: Bidirectional Position, Dependency Concentration, Vendor Assessment Paradox, Cascade Multiplier)
- **Human Creative Input Estimate:** 1 (Governor review of final assessment)

## Actions (Current Cycle)

### ACT-1: Execute multi-agent deliberation → serves TAC-1
- **Assignee:** AI
- **Deliverable:** Deliberation transcript with per-agent positions, tension identification, and resolution
- **Deadline:** 2026-04-08
- **Dependency Type:** execution

### ACT-2: Synthesize priority assessment from deliberation → serves TAC-1
- **Assignee:** AI
- **Deliverable:** Priority assessment document with prioritized list, tension map, sequencing recommendation
- **Deadline:** 2026-04-08
- **Dependency Type:** execution

### ACT-3: Governor review and acceptance → serves TAC-1
- **Assignee:** Governor
- **Deliverable:** Acceptance or revision request
- **Deadline:** 2026-04-08
- **Dependency Type:** human_creative

## Review Cadences
- **Finite scope:** Review at each phase gate

## Decision History
- **2026-04-08 — OD-v1 created:** Initial operating document for CISO Priorities 2026 session. 6 domain models built from scratch using existing session models as enhancement sources. Single strategy (multi-agent deliberation) with single tactic (domain-stacked deliberation).

---

## Phases (finite scopes only)

### Phase 1: Domain Model Review & Deliberation Setup
- **Objective:** Verify domain models are sufficient for deliberation; configure deliberation parameters
- **Entry Criteria:** All 6 domain models written
- **Exit Criteria:** Governor confirms domain model adequacy; deliberation configuration locked

### Phase 2: Multi-Agent Deliberation
- **Objective:** Execute 3-round deliberation with domain model stacking to produce priority assessment
- **Entry Criteria:** Phase 1 exit criteria met
- **Exit Criteria:** Deliberation complete; tension map produced; priority sequencing draft ready

### Phase 3: Synthesis & Governor Review
- **Objective:** Produce final priority assessment document; Governor acceptance
- **Entry Criteria:** Phase 2 exit criteria met
- **Exit Criteria:** Governor accepts deliverable or requests revision (max 3 cycles)

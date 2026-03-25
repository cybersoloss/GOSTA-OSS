# Operating Document: Feature Prioritization — EU Developer Tools SaaS
**Version:** 2 | **Date:** 2026-03-20 | **Governor:** VP Product
**Scope Type:** finite | **Graduation Stage:** 1

## Goal
Produce an evidence-grounded, cross-domain feature prioritization for the next two quarters (Q2–Q3 2026) that sequences 12 candidate features by balancing market demand, technical feasibility, and regulatory compliance — enabling the Governor to commit roadmap resources with explicit risk awareness.

### Guardrails
- **G-1:** No feature may be sequenced before its compliance prerequisite chain is complete | Severity: hard | Evaluation: mechanical | Threshold: 0 unmet prerequisites in any shipped feature
- **G-2:** Activation distance must not increase for any shipped feature | Severity: hard | Evaluation: mechanical | Threshold: current baseline (7 steps to first value)
- **G-3:** Total estimated engineering effort for the approved roadmap must not exceed 2.4 FTE-quarters | Severity: hard | Evaluation: mechanical | Threshold: 2.4 FTE-quarters
- **G-4:** No single customer segment may account for >50% of roadmap investment | Severity: soft | Evaluation: mechanical | Threshold: 50% investment concentration
  - Recovery: Rebalance lowest-priority features from the over-concentrated segment to the next-highest-priority cross-segment feature
- **G-5:** Features touching high-debt components must carry a ≥1.5x effort multiplier in estimates | Severity: soft | Evaluation: mechanical | Threshold: 1.5x minimum multiplier
  - Recovery: Recalculate affected feature estimates with correct multiplier; re-sequence if rank changes
- **G-6:** Multi-domain deliberation must include ≥3 independent domain assessments per evaluated feature | Severity: hard | Evaluation: mechanical | Threshold: 3 independent assessments

## Objectives

### OBJ-1: Produce Cross-Domain Feature Priority Matrix
- **Analytical Question:** Which of the 12 candidate features should be built in which quarter, given market demand strength, engineering cost and risk, and regulatory obligations?
- **Acceptance Criteria:** All 12 features assessed with ≥3 domain scores each; cross-domain tensions explicitly documented; final sequencing accounts for dependency chains and compliance prerequisites
- **Deliverable:** Feature-evidence matrix with per-feature verdicts and a phased 2-quarter roadmap
- **Quality Standard:** Every verdict cites specific domain model concepts by ID; every cross-domain tension identifies the conflicting concepts and how the conflict was resolved
- **Priority:** critical

## Strategies

### STR-1: Multi-Domain Deliberation Assessment → serves OBJ-1
- **Rationale:** Single-domain scoring misses cross-domain tensions that determine real-world sequencing. A feature with strong market demand but deep dependency chains and missing compliance prerequisites will fail if sequenced by market score alone. Multi-agent deliberation surfaces these tensions structurally.
- **What Must Be True (WMBT):** Domain models for market-fit, technical-feasibility, and regulatory-compliance are loaded and quality-gated. Feature specifications are detailed enough for each domain to score meaningfully. At least 3 domain agents produce independent assessments.
- **Not Doing:** Customer interviews, competitive analysis refresh, or new market research. This assessment uses existing evidence and domain expertise.
- **Kill Signal:** Fewer than 3 domain models produce scorable assessments (domain model quality failure), OR deliberation produces no actionable disagreements (domains are not in tension, meaning the problem is simpler than assumed and deliberation is overhead).
- **Relationship to sibling strategies:** none (single strategy)
- **Authorized By:** GOV-session-1

## Tactics

### TAC-1: Feature Scoring via 5-Agent Deliberation → serves STR-1
- **Parent Strategy:** STR-1
- **Parent Objective:** OBJ-1
- **Hypothesis:** If we score each feature independently across market-fit, technical-feasibility, and regulatory-compliance domains using isolated domain agents, then cross-domain tensions will surface as disagreements that the Coordinator can map — producing a priority matrix that no single-domain analysis could generate.
- **Kill Condition:** Deliverable not accepted after 3 revision cycles. Alternatively: if deliberation Round 1 produces <2 disagreements across all 12 features, kill (the problem doesn't warrant deliberation overhead).
- **Success Metrics:** Number of cross-domain tensions surfaced per feature; Governor acceptance of final matrix; all 12 features scored in all 3 domains
- **Guardrails (inherited):** G-1 (compliance prerequisites), G-2 (activation distance), G-3 (effort ceiling), G-6 (≥3 assessments)
- **Guardrails (own):** None additional
- **Timeline:** 2026-03-18 — 2026-03-25
- **Bootstrap Cycles:** 0 (finite analytical scope, no bootstrap needed)
- **Seed Actions:** Load domain models, prepare feature list with specifications
- **Owner:** AI (Governor reviews synthesis and makes final sequencing decisions)
- **Approach:** Single-session sequential deliberation. Each domain agent scores all 12 features from its domain perspective, producing a position paper. Coordinator synthesizes across domains, identifies tensions, and produces a draft priority matrix. Governor resolves tensions and approves final sequencing.
- **Dependencies:** execution (AI-driven)
- **Domain Model Dependencies:** market-fit (concepts: Activation Distance, Switching Cost Asymmetry, WTP Signal, Market Timing Sensitivity, Segment Concentration Risk, Competitive Parity Gap), technical-feasibility (concepts: Dependency Depth, Architectural Congruence, Technical Debt Load, Reversibility, Scalability Trajectory, Integration Surface Area), regulatory-compliance (concepts: Enforcement Probability Gradient, Data Flow Sovereignty, Compliance Prerequisite Chain, Regulatory Change Velocity)

### TAC-2: Dependency-Aware Roadmap Sequencing → serves STR-1
- **Parent Strategy:** STR-1
- **Parent Objective:** OBJ-1
- **Hypothesis:** If we sequence the priority matrix output from TAC-1 through dependency chain analysis and compliance prerequisite mapping, then the resulting roadmap will be executable without mid-quarter blocking discoveries.
- **Kill Condition:** Deliverable not accepted after 3 revision cycles. Alternatively: if dependency analysis reveals >60% of features are blocked by unbuilt prerequisites (indicating the candidate set is premature — prerequisites should be the roadmap).
- **Success Metrics:** Zero dependency violations in final roadmap; all compliance prerequisites sequenced before dependent features; total effort within G-3 ceiling
- **Guardrails (inherited):** G-1, G-3, G-5
- **Guardrails (own):** None additional
- **Timeline:** 2026-03-22 — 2026-03-25
- **Bootstrap Cycles:** 0
- **Seed Actions:** Take TAC-1 priority matrix output; map dependency chains per technical-feasibility domain model; map compliance prerequisite chains per regulatory-compliance domain model
- **Tactic Dependencies:** depends_on: TAC-1 (exit_criteria: Governor-accepted priority matrix)

## Actions (Current Cycle)

### ACT-1: Load and validate domain models → serves TAC-1
- **Assignee:** AI
- **Deliverable:** 3 domain models loaded, quality-gated (all 6 components present, QPs and APs populated)
- **Deadline:** 2026-03-18
- **Dependency Type:** execution

### ACT-2: Prepare feature specification list → serves TAC-1
- **Assignee:** AI (with Governor input on feature descriptions)
- **Deliverable:** 12-feature list with name, description, target segment, known dependencies, regulatory implications
- **Deadline:** 2026-03-18
- **Dependency Type:** human_creative

### ACT-3: Execute DELIB-001 deliberation cycle → serves TAC-1
- **Assignee:** AI
- **Deliverable:** 5 position papers, interim assessments, synthesis report with cross-domain tension map
- **Deadline:** 2026-03-20
- **Dependency Type:** execution

### ACT-4: Produce scored feature matrix → serves TAC-1
- **Assignee:** AI
- **Deliverable:** 12×3 domain score matrix with per-feature verdicts and tension annotations
- **Deadline:** 2026-03-21
- **Dependency Type:** execution

### ACT-5: Map dependency chains and compliance prerequisites → serves TAC-2
- **Assignee:** AI
- **Deliverable:** Dependency graph showing prerequisite chains for all 12 features
- **Deadline:** 2026-03-22
- **Dependency Type:** execution

### ACT-6: Produce phased 2-quarter roadmap → serves TAC-2
- **Assignee:** AI
- **Deliverable:** Q2 and Q3 feature assignments with effort estimates, dependency sequencing, and risk flags
- **Deadline:** 2026-03-23
- **Dependency Type:** execution

### ACT-7: Governor review and final approval → serves TAC-2
- **Assignee:** Governor
- **Deliverable:** Approved roadmap with resolved tensions and committed resource allocation
- **Deadline:** 2026-03-25
- **Dependency Type:** human_creative

## Review Cadences
- **Finite scope:** Review at each phase gate (Phase 1→2 gate after deliberation; Phase 2→closeout after roadmap acceptance)

## Decision History
- **2026-03-18 (GOV-session-1):** OD v1 created. Governor approved scope: 12 features, 3 domain models, deliberation enabled.
- **2026-03-19 (GOV-session-2):** OD v2. Governor added G-5 (debt multiplier) after reviewing technical-feasibility domain model. Added UX-Agent to deliberation roster (expanded from 4 to 5 agents) to cover activation distance assessment.

---

## Phases

### Phase 1: Multi-Domain Deliberation
- **Objective:** Score all 12 features across 3 domains via 5-agent deliberation
- **Entry Criteria:** Domain models loaded and quality-gated; feature list approved by Governor
- **Exit Criteria:** Synthesis report accepted by Governor; all disagreements resolved or explicitly deferred
- **Actions:** ACT-1, ACT-2, ACT-3, ACT-4

### Phase 2: Roadmap Construction
- **Objective:** Sequence scored features into an executable 2-quarter roadmap
- **Entry Criteria:** Phase 1 complete; scored matrix available
- **Exit Criteria:** Governor accepts final roadmap; dependency chains validated; effort within G-3 ceiling
- **Actions:** ACT-5, ACT-6, ACT-7

---

## Autonomy Safeguards

### Magnitude Thresholds
- **Resource cost:** Not applicable (analytical scope — no spend commitments)
- **Timeline impact:** Delays scope deadline by >3 days
- **Stakeholder visibility:** Roadmap shared with engineering leads or board
- **External commitment:** Not applicable

### Governor Attention Capacity
- **Reviews per Week:** 3 (Phase 1 gate, Phase 2 gate, final approval)
- **Role:** part_time
- **Sustainability Flag:** Within threshold

---

## Domain Models Referenced
- market-fit — Activation Distance, Switching Cost Asymmetry, WTP Signal, Market Timing Sensitivity, Segment Concentration Risk, Competitive Parity Gap
- technical-feasibility — Dependency Depth, Architectural Congruence, Technical Debt Load, Reversibility, Scalability Trajectory, Integration Surface Area
- regulatory-compliance — Enforcement Probability Gradient, Data Flow Sovereignty, Compliance Prerequisite Chain, Regulatory Change Velocity

## Multi-Domain Assessment
- **Independence Level:** 3 (Multi-agent deliberation)
- **Deliberation Mode:** enabled

## Deliberation

### Agent Roster

| Agent ID | Domain Model | Role | Model/Provider | Notes |
|----------|-------------|------|----------------|-------|
| MKT-1 | market-fit | domain_agent | default | Scores market demand, timing, segment risk |
| TECH-1 | technical-feasibility | domain_agent | default | Scores effort, risk, architectural fit |
| REG-1 | regulatory-compliance | domain_agent | default | Scores compliance requirements, enforcement risk |
| UX-1 | market-fit | domain_agent | default | Activation distance specialist — scores only activation impact |
| COORD-1 | — | coordinator | default | No domain model — synthesizes across domains |

**Note on UX-1:** Uses the market-fit domain model but is scoped exclusively to Activation Distance and its interactions. This prevents activation distance from being under-weighted within the broader market-fit assessment. UX-1's position paper covers only activation impact; MKT-1 covers all other market-fit concepts.

**G-6 Traceability Calibration:**
- **N (domain agents):** 4
- **Tolerated Fallback Proxies:** 1
- **G-6 Threshold:** 3

### Deliberation Cadence
- **Trigger:** on_schedule (Phase 1, single cycle)
- **Max Rounds:** 3
- **New Argument Gate (Round 4+):** enabled
- **Governor Interaction:** at_synthesis
- **Isolation:** single_session_sequential

### Termination Thresholds
- **Convergence Definition:** All domain agents within 2 points (on 10-point scale) for ≥80% of features, with aligned directional recommendations (build/defer/prerequisite)
- **New Argument Definition:** Introduces a domain concept not previously cited, or applies an existing concept to a feature not previously analyzed from that angle
- **Stall Definition:** 1 round of zero new arguments across all agents

### Deliberation File Structure
```
deliberation/
├── DELIB-001/
│   ├── position-MKT-1.md
│   ├── position-TECH-1.md
│   ├── position-REG-1.md
│   ├── position-UX-1.md
│   ├── interim-assessment-R1.md
│   ├── synthesis-report.md
│   └── verification.md
```

## Feature Candidate List

The following 12 features are the evaluation targets for this scope:

| ID | Feature | Description | Target Segment | Known Dependencies |
|----|---------|-------------|----------------|-------------------|
| F-01 | EU Data Residency | Process and store EU customer data exclusively on EU infrastructure | Enterprise | Infrastructure migration |
| F-02 | Automated DSAR Pipeline | Fulfill data subject access requests within 30-day GDPR deadline | Enterprise, Mid-market | Data catalog, identity resolution |
| F-03 | In-App Templates | Pre-built project templates reducing activation from 7 steps to 3 | All segments | Template engine |
| F-04 | Slack Integration | Bi-directional notifications and commands via Slack | Mid-market | Webhook infrastructure |
| F-05 | AI-Powered Code Review | Automated code review suggestions using LLM analysis | Mid-market, Enterprise | AI Act transparency layer (F-08) |
| F-06 | Role-Based Access Control | Granular permissions for team workspaces | Enterprise | Identity service refactor |
| F-07 | Usage Analytics Dashboard | Real-time usage metrics and team activity insights | Mid-market | Event pipeline, data warehouse |
| F-08 | AI Act Transparency Layer | Model card generation, explanation outputs for AI features | Enterprise (EU) | None (prerequisite for F-05) |
| F-09 | Custom Workflow Automation | User-defined automation rules (triggers, conditions, actions) | Mid-market, Enterprise | Workflow engine |
| F-10 | SSO/SAML Integration | Enterprise single sign-on support | Enterprise | Identity service refactor |
| F-11 | Bulk Data Export | Export all workspace data in portable formats | All segments | Data catalog |
| F-12 | Real-Time Collaboration | Simultaneous multi-user editing with presence indicators | Mid-market | WebSocket infrastructure, CRDT engine |

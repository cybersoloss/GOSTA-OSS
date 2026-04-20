# Deliberation Configuration: Vendor-Product Continuity Assessment

## Independence Level
**Level 2** — Agents see each other's output after each round but must maintain independent positions through round 2. Convergence permitted only in round 3.

## Deliberation Structure
- **Rounds:** 3 + synthesis
- **Round 1:** Initial positions — each agent presents assessment grounded in their assigned domain model pair, scoring vendor and product levels independently. Each agent must explicitly address which Talk-2 signals their domains inform.
- **Round 2:** Challenge and tension identification — agents challenge each other's signal assessments using their domain perspectives; cross-domain tensions must be explicitly named and traced to domain model concepts. Particular attention to where leading indicators (Agent D) contradict signal-based findings (Agents A-C).
- **Round 3:** Convergence — agents converge on unified signal scores, viability verdicts, and risk determination inputs. Residual disagreements that cannot be resolved without additional evidence are preserved as unresolved tensions.
- **Synthesis:** Coordinator produces synthesis report structured per the six-signal framework: (1) Business Model Signals, (2) Contractual Position, (3) Dependency Exposure, (4) Leading Indicators, (5) Cross-Domain Tensions, (6) Risk Determination.

## Agent Roles and Domain Assignments

### Agent A: Business Model Analyst
**Domain Models:** ECON-1 (Economic Health), DISP-1 (Competitive Displacement)
**Signal Coverage:** Signal 1 (Revenue model exposure — with SAAS-1 input from Agent B), Signal 2 (Domain depth vs. feature breadth — data moat), Signal 3 (Financial sustainability and consolidation)
**Perspective:** Is [Target Vendor] financially sustainable and is [Target Product] competitively defensible? This agent owns the business model signals — assessing revenue trajectory, competitive displacement pressure, data moat defensibility, and consolidation positioning. The central tension: a vendor may be profitable today but facing displacement pressure that erodes future viability, or financially stressed but holding a defensible market position through customer-specific data moats.

### Agent B: Structural Viability Analyst
**Domain Models:** ADAPT-1 (Adaptation Capacity), SAAS-1 (SaaS Structural Viability)
**Signal Coverage:** Signal 1 (Revenue model exposure — pricing model vulnerability via SAAS-1), supports Signals 1-3 via adaptation capacity assessment
**Perspective:** Can [Target Vendor] adapt to the pressures identified by Agent A, and does [Target Product] have structural SaaS characteristics that support or undermine long-term viability? This agent provides depth on Signal 1 (pricing model vulnerability) through SAAS-1 and contextualizes all business model findings through ADAPT-1's assessment of whether the vendor can respond. The central tension: a product may have strong SaaS economics today but low adaptation capacity, meaning it works now but cannot evolve as AI reshapes its category.

### Agent C: Dependency Exposure Analyst
**Domain Models:** STICK-1 (Structural Stickiness), REG-1 (Regulatory Entrenchment)
**Signal Coverage:** Signal 4 (Exit strategy provisions), Signal 5 (Regulatory embedding depth), Signal 6 (Vendor stickiness vs. viability)
**Perspective:** How deep is the dependency and does the regulatory environment create a viability floor or ceiling? This agent owns the contractual position and dependency exposure signals — the "what happens to us if they fail" assessment. The central tension: high stickiness combined with regulatory embedding creates maximum exposure — if the vendor fails, the organization faces both operational disruption and regulatory compliance disruption. Regulatory demand may protect the vendor's viability (floor) while simultaneously amplifying the dependent organization's exit costs (ceiling on escape).

### Agent D: Leading Indicator Analyst
**Domain Models:** GOV-1 (Governance & Strategic Coherence), TAL-1 (Talent & Workforce)
**Signal Coverage:** Leading indicators that predict viability deterioration before Signals 1-6 manifest
**Perspective:** Is [Target Vendor] organizationally healthy, and does its workforce trajectory sustain or undermine the viability picture from Agents A-C? This agent provides the forward-looking assessment — both GOV-1 and TAL-1 are vendor-level, prediction-oriented domains that serve as early warning systems. The central tension: a vendor may project strategic clarity through governance communications while quietly losing key personnel and shifting to maintenance hiring, or may undergo leadership restructuring while retaining strong engineering talent. Governance and talent together form the organizational health picture that either confirms or contradicts Agents A-C's signal-based findings. When Agent D's leading indicators diverge from the business model and dependency assessments, the divergence itself is a critical finding.

## Coordinator: COORD-1
Auto-generated. The Coordinator does not hold domain positions. It manages round transitions, enforces independence constraints, detects convergence vs. genuine agreement, and produces the synthesis report structured per the six-signal framework. The Coordinator specifically tracks:
- Whether all 6 signals received substantive assessment (G-2)
- Whether leading indicators confirm or contradict signal-based findings
- Whether the stickiness-viability combination matrix was applied (H-4)
- Whether the deliverable follows the prescribed structure

## Cross-Agent Signal Coverage Map

| Signal | Primary Agent | Supporting Agent | Required Tension |
|---|---|---|---|
| (1) Revenue model exposure | Agent A (ECON-1) + Agent B (SAAS-1) | — | A and B may disagree on whether pricing vulnerability translates to viability threat |
| (2) Domain depth vs. feature breadth | Agent A (DISP-1) | Agent B (ADAPT-1) | Data moat assessment vs. adaptation capacity — can vendor deepen the moat? |
| (3) Financial sustainability / consolidation | Agent A (ECON-1) | Agent D (GOV-1) | Financial trajectory vs. governance signals — do they align? |
| (4) Exit strategy provisions | Agent C (REG-1) | — | — |
| (5) Regulatory embedding depth | Agent C (REG-1) | Agent A (ECON-1) | Regulatory protection vs. financial pressure — does the moat hold? |
| (6) Vendor stickiness vs. viability | Agent C (STICK-1) | Agent A (ECON-1 + DISP-1) | Stickiness assessment needs viability input to determine combination matrix position |
| Leading: Talent trajectory | Agent D (TAL-1) | Agent A (ECON-1) | Talent signals vs. financial signals — confirming or contradicting? |
| Leading: Governance quality | Agent D (GOV-1) | Agent B (ADAPT-1) | Governance clarity vs. adaptation capacity — do they align? |

## Tension Detection Requirements
Each agent must identify at least 2 tensions per round where their domain perspective conflicts with another agent's assessment. Tensions must specify:
1. The two domain concepts in conflict (with domain model IDs)
2. Which Talk-2 signal the tension affects
3. Why they produce divergent viability signals for [Target Vendor] or [Target Product]
4. What resolution would require: additional evidence, accepted ambiguity, or conditional verdict (e.g., "VIABLE if X remains true, AT RISK if X changes")

## Sycophancy Detection
Active. Agents must not adopt another agent's signal assessment without providing independent domain-model-grounded reasoning from their assigned pair. Agreement on a verdict must be earned through converging evidence, not assumed through convergence pressure. The Coordinator flags any round where all four agents shift toward the same verdict without new evidence being introduced.

## Shortfall Logging
Enabled. When an agent cannot adequately score a signal or domain due to evidence gaps, the shortfall is logged with: domain model ID, affected signal number, missing evidence category, impact on scoring confidence, and whether the gap affects vendor-level, product-level, or both assessments.

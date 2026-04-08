# Deliberation Configuration: CISO Priorities 2026

## Independence Level
**Level 2** — Agents see each other's output after each round but must maintain independent positions through round 2. Convergence permitted only in round 3+.

## Deliberation Structure
- **Rounds:** 4 (expanded from 3 to include dependency audit)
- **Round 1:** Initial positions — each agent presents priority assessment grounded in their assigned domain model cluster
- **Round 2:** Challenge and tension identification — agents challenge each other's priorities using their domain perspectives; tensions must be explicitly named and traced to domain model concepts
- **Round 3:** Synthesis — agents converge on a unified priority assessment that resolves or explicitly accepts identified tensions
- **Round 4:** Dependency audit — each key dependency is validated from all three domain perspectives; counter-factual testing argues the reverse sequencing for each dependency

## Agent Roles and Domain Assignments

### Agent A: Regulatory-Operational Analyst
**Domain Models:** Regulatory Compliance, Operational Capacity
**Perspective:** What must be done (legal obligation) constrained by what can be done (staffing and budget reality). This agent surfaces the tension between regulatory aspiration and execution feasibility.

### Agent B: Threat-Technology Challenger
**Domain Models:** Threat Landscape, Technology & Architecture
**Perspective:** What actually compromises organizations (threat data) and what technical architecture creates or reduces exposure. This agent challenges priorities that address compliance without addressing actual attack chains.

### Agent C: Business-Supply Chain Synthesizer
**Domain Models:** Business Value & Continuity, Supply Chain & Third-Party Risk
**Perspective:** What matters to the business (revenue protection, customer retention, operational survival) and what external dependencies create existential risk. This agent grounds abstract security priorities in business reality.

## Tension Detection Requirements
Each agent must identify at least 2 tensions per round where their domain perspective conflicts with another agent's priorities. Tensions must specify:
1. The two domain concepts in conflict
2. Why they pull in different directions
3. What a resolution would require (trade-off, sequencing, or accepted risk)

## Shortfall Logging
Enabled. When an agent cannot adequately address a topic due to domain model gaps, the shortfall is logged with: domain model name, missing concept, and impact on analysis quality.

## Sycophancy Detection
Active. Agents must not adopt another agent's position without providing independent domain-model-grounded reasoning. Agreement must be earned through evidence, not assumed through convergence pressure.

# Phased Roadmap: Q2–Q3 2026
**Scope:** Feature Prioritization — EU Developer Tools SaaS
**Approved:** DEC-001 (2026-03-21) | **Governor:** VP Product

---

## Q2 2026: Foundation + Quick Wins

```
Week 1-2  ┃ F-03: In-App Templates (2-3 wk)
          ┃   → Ship first. Immediate activation distance improvement.
          ┃   → Success metric: trial-to-paid conversion baseline established
          ┃
Week 2-5  ┃ F-04: Slack Integration (3-4 wk)
          ┃   → Competitive parity. 4 documented deal losses addressed.
          ┃   → Parallel with F-03 tail and F-08 start
          ┃
Week 3-6  ┃ F-08: AI Act Transparency Layer (3-4 wk)
          ┃   → Compliance prerequisite for F-05 and all future AI features
          ┃   → Must complete before F-05 development begins
          ┃
Week 1-14 ┃ F-01: EU Data Residency (12-16 wk) [INFRASTRUCTURE TEAM]
          ┃   → Separate staffing. Cloud provider coordination.
          ┃   → Milestone check at Week 8: migration plan validated
          ┃   → Success metric: EU prospects unblocked (target: 8 prospects, €400K ARR)
```

**Q2 Product Engineering:** 8-11 FTE-weeks (of 12 FTE-week budget)
**Q2 Infrastructure:** 12-16 FTE-weeks (separate budget)

**Q2 Gates:**
- Week 6: F-03 shipped + conversion baseline measured
- Week 8: F-01 migration plan validated (escalation point if behind)
- Week 10: F-04 + F-08 shipped
- Week 12: Q2 retrospective, Q3 planning confirmation

**Parallel Q2 Activity:**
- Legal Ops: Manual DSAR capacity audit (DEC-001/DECISION-2 contingency)
- Product Design: F-06 (RBAC) G-2-compliant specification work (zero-config defaults, activation regression test design)

---

## Q3 2026: Enterprise Infrastructure + Exploration

```
Week 1-3  ┃ Identity Service Refactor Phase 0 (prerequisite for F-10)
          ┃   → Debt reduction in high-debt area
          ┃   → Estimate includes 1.5x debt multiplier
          ┃   → Milestone: refactored service passing existing test suite
          ┃
Week 3-12 ┃ F-10: SSO/SAML Integration (6-9 wk post-refactor)
          ┃   → Enterprise parity. 3 documented deal losses addressed.
          ┃   → Integration testing with 3 reference IdPs
          ┃   → Success metric: enterprise deal cycle reduction measured
          ┃
Week 8-10 ┃ F-12: Real-Time Collaboration POC (2-3 wk)
          ┃   → Proof-of-concept: CRDT text editing, 2 concurrent users
          ┃   → Exit criteria: library validated, latency measured, full-build
          ┃     estimate with ±20% confidence
          ┃   → Decision point: POC outcome informs Q4 build/no-build
```

**Q3 Product Engineering:** 11-15 FTE-weeks (of 12 FTE-week budget — slight overcommit, monitor)
**Q3 Infrastructure:** F-01 completion if it extends past Q2

**Q3 Gates:**
- Week 3: Identity refactor complete, F-10 development begins
- Week 6: F-10 midpoint check (debt multiplier adequacy)
- Week 10: F-12 POC complete, results reviewed
- Week 12: Q3 retrospective, Q4 backlog prioritization

---

## Q4 2026 Backlog (Unsequenced — Requires Q3 Retrospective)

| Feature | Effort | Prerequisite | Notes |
|---------|--------|-------------|-------|
| F-05: AI Code Review | 8-10 wk | F-08 (complete) | First AI-powered feature with transparency layer |
| F-02: DSAR Pipeline | 9-12 wk | Data catalog (moderate debt) | Depends on Q2 manual audit outcome |
| F-06: RBAC | 12-18 wk | Identity refactor (Q3), G-2 design spec | Highest effort; activation constraints require careful design |
| F-07: Usage Analytics | 6-8 wk | Lawful basis mechanism (unbuilt) | Prerequisite adds 2-3 weeks to timeline |

**Q4 total if all built:** 35-48 FTE-weeks → exceeds single-quarter capacity. Governor will select subset at Q3 retrospective based on Q2-Q3 outcomes, market conditions, and updated regulatory landscape.

---

## Deferred Features

| Feature | Reason | Revisit Trigger |
|---------|--------|----------------|
| F-09: Custom Workflows | Scope risk (workflow engine underestimation), activation harm (UX-1), no time pressure | Revisit if: (1) switching cost data shows churn increasing, (2) competitor ships workflow automation |
| F-11: Bulk Data Export | Low demand, minimal enforcement of GDPR Art. 20 | Revisit if: (1) Art. 20 enforcement changes, (2) enterprise RFP requirement emerges |
| F-12 Full Build | Pending POC outcome | POC in Q3. Full build decision at Q3 retrospective. |

---

## Risk Register

| Risk | Probability | Impact | Mitigation |
|------|:-:|:-:|---|
| F-01 infra team unavailable | Medium | Critical — G-3 violated, roadmap restructure needed | Governor to confirm staffing by Q2 Week 1 |
| Identity refactor exceeds 1.5x multiplier | Medium | High — F-10 slips, Q3 overcommit | Monitor Sprint 1 velocity; escalate if >80% of revised estimate consumed by midpoint |
| F-01 cloud provider delays | Medium | High — EU revenue capture window closes | Week 8 milestone check; escalation path to provider defined |
| Manual DSAR process fails during Q2 | Low | Critical — regulatory enforcement action | Q2 capacity audit as early warning system |
| F-12 POC invalidates CRDT approach | Medium | Low — only 2-3 weeks lost, feature returns to backlog | POC designed to fail fast; alternative architecture approaches documented |

---

## Guardrail Compliance Summary

| Guardrail | Q2 Status | Q3 Status | Annual Status |
|-----------|:-:|:-:|:-:|
| G-1: Compliance prerequisites | ✅ F-08 before F-05 | ✅ N/A | ✅ |
| G-2: Activation distance | ✅ F-03 reduces it | ✅ No regressing features | ✅ |
| G-3: Effort ceiling (2.4 FTE-Q) | ✅ 0.7-0.9 FTE-Q | ⚠️ 0.9-1.25 FTE-Q | ✅ 1.6-2.2 FTE-Q total |
| G-4: Segment concentration | ⚠️ Enterprise-heavy | ⚠️ Enterprise-heavy | ⚠️ Acknowledged (regulatory driver) |
| G-5: Debt multiplier | ✅ N/A (no high-debt work) | ✅ 1.5x applied to identity service | ✅ |
| G-6: ≥3 domain assessments | ✅ 4 agents completed | ✅ N/A (deliberation complete) | ✅ |

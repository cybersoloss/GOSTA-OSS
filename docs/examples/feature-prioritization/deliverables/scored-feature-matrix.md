# Scored Feature Matrix
**Scope:** Feature Prioritization — EU Developer Tools SaaS
**Date:** 2026-03-21 | **Source:** DELIB-001 Synthesis + DEC-001 Governor Decisions

---

## Domain Scores (1-10 scale)

| ID | Feature | Market (MKT-1) | Technical (TECH-1) | Regulatory (REG-1) | Activation (UX-1) | Composite | Governor Verdict |
|----|---------|:-:|:-:|:-:|:-:|:-:|---|
| F-03 | In-App Templates | 8 | 9 | — | 10 | **HIGH** | ✅ Q2 Build |
| F-04 | Slack Integration | 7 | 8 | 2 | 3 | **HIGH** | ✅ Q2 Build |
| F-08 | AI Act Transparency | 3 | 7 | 9 | — | **HIGH (reg)** | ✅ Q2 Build (G-1 prerequisite) |
| F-01 | EU Data Residency | 9 | 3 | 10 | 1 | **CRITICAL** | ✅ Q2 Infra Team |
| F-10 | SSO/SAML | 7 | 4 | 5 | 5 | **MEDIUM-HIGH** | ✅ Q3 Build (+ identity refactor) |
| F-12 | Real-Time Collaboration | 8 | 2 | 3 | 7 | **HIGH/BLOCKED** | ✅ Q3 POC (2-3 wk) |
| F-05 | AI Code Review | 6 | 5 | 8 | 4 | **MEDIUM** | ⏳ Q4 (after F-08) |
| F-02 | DSAR Pipeline | 5 | 5 | 9 | 1 | **HIGH (reg)** | ⏳ Q4 (Q2 manual audit) |
| F-06 | RBAC | 7 | 4 | 4 | -2 | **MEDIUM-HIGH** | ⏳ Q4 (needs G-2 design spec) |
| F-07 | Usage Analytics | 4 | 5 | 6 | 2 | **MEDIUM** | ⏳ Q4 (needs lawful basis) |
| F-11 | Bulk Data Export | 3 | 7 | 4 | 1 | **LOW** | ❌ Deferred |
| F-09 | Custom Workflows | 6 | 4 | 3 | -1 | **LOW** | ❌ Deferred |

**Scoring notes:**
- "—" indicates the domain has no relevant assessment (not opposition, just irrelevance)
- Negative UX-1 scores indicate features that INCREASE activation distance (G-2 violation risk)
- Composite is not a weighted average — it reflects the synthesis of cross-domain tensions documented in DELIB-001
- Governor verdicts override composite scores where structural constraints apply (G-1 compliance prerequisites, G-3 effort ceiling, dependency chains)

## Cross-Domain Tensions (from DELIB-001)

| Feature | Tension | Resolution |
|---------|---------|-----------|
| F-01 | Market/Regulatory (9-10) vs. Technical (3): highest value + lowest feasibility | Governor: separate infrastructure team staffing |
| F-08 | Market (3) vs. Regulatory (9): zero demand + hard compliance prerequisite | GV-1 hard guardrail: must build regardless of market |
| F-02 | Market (5) vs. Regulatory (9): invisible compliance vs. visible features | Governor: Q3 build with Q2 manual process audit |
| F-06 | Market (7) vs. UX (-2) vs. Technical (4): demand vs. activation harm vs. debt | Governor: defer to Q4 pending G-2-compliant design |
| F-12 | Market/UX (8/7) vs. Technical (2): desired but technically risky | Governor: Q3 POC to derisk, not full commitment |
| F-05→F-08 | Prerequisite chain: F-05 unshippable to EU without F-08 | Sequencing constraint: F-08 in Q2, F-05 in Q4 |

## Effort Summary

| Quarter | Features | Product FTE-weeks | Infrastructure FTE-weeks |
|---------|----------|:-:|:-:|
| Q2 2026 | F-03, F-04, F-08 | 8-11 | — |
| Q2 2026 | F-01 | — | 12-16 |
| Q3 2026 | F-10 (+ identity refactor), F-12 POC | 11-15 | — |
| **Total approved** | | **19-26** | **12-16** |
| **G-3 ceiling** | | **24** | **separate** |
| **G-3 status** | | **✅ PASS** | **N/A** |

## Dependency Graph

```
F-08 (AI Act Transparency)
  └── F-05 (AI Code Review) [compliance prerequisite]

F-01 (EU Data Residency)
  └── All EU features [data flow sovereignty foundation]

Identity Service Refactor (prerequisite work)
  ├── F-10 (SSO/SAML)
  └── F-06 (RBAC) [deferred to Q4]

Data Catalog (existing, moderate debt)
  ├── F-02 (DSAR Pipeline)
  └── F-11 (Bulk Data Export)

Lawful Basis Mechanism (unbuilt prerequisite)
  └── F-07 (Usage Analytics)
```

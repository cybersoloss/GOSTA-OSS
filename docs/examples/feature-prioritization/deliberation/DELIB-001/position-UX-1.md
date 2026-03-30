# Position Paper: UX-1 (Activation Distance Specialist)
**Deliberation:** DELIB-001 | **Round:** 1 | **Date:** 2026-03-19
**Domain Model:** market-fit (scoped to Activation Distance concept) | **Evaluation Target:** 12 candidate features (F-01 through F-12)

---

## Scope Declaration

UX-1 is scoped exclusively to Activation Distance and its interactions with other market-fit concepts. This prevents activation distance from being under-weighted within MKT-1's broader assessment, which covers 6 concepts simultaneously.

**Activation Distance** (from market-fit domain model): The number of steps between a new user's first interaction and the moment they experience the product's core value. Shorter activation distance correlates with higher trial-to-paid conversion. Features that reduce activation distance should score higher than features that add capability to already-activated users — unless retention data shows activated users are churning, which inverts the priority.

**Current baseline:** 7 steps from signup to first value moment (project creation → configuration → team invite → integration setup → first workflow → first result → "aha" moment). Trial-to-paid conversion: 12%. Drop-off analysis shows 23% abandonment at steps 4-5 (integration setup, first workflow).

## Feature Scores (1-10 scale, activation distance impact — higher = greater positive impact on activation)

| Feature | Score | Impact on Activation | Rationale |
|---------|-------|---------------------|-----------|
| F-01: EU Data Residency | **1** | None | Infrastructure feature. Invisible to activation flow. Zero effect on steps-to-value. |
| F-02: Automated DSAR Pipeline | **1** | None | Backend compliance feature. Users never interact with it during activation. |
| F-03: In-App Templates | **10** | Reduces 7→3 steps | Directly eliminates steps 2-5 (configuration, team invite, integration setup, first workflow) by providing pre-configured starting points. This is the single highest-leverage activation improvement available. Projected impact: trial-to-paid conversion increase from 12% to 17-19% based on drop-off analysis at steps 4-5. |
| F-04: Slack Integration | **3** | Minor reduction via familiar interface | Slack notifications could surface the product's value in a tool users already live in — creating an alternative activation path. But the user still needs to complete initial setup. Net effect: slight reduction in perceived distance, not actual step count. |
| F-05: AI Code Review | **4** | Creates new value moment but adds setup | AI review could deliver an "aha" moment faster than manual workflows — but only for users who push code through the system first. It compresses the distance between "first workflow" and "first value" but doesn't eliminate the steps before it. Net: neutral to slightly positive for users who reach step 5. |
| F-06: RBAC | **-2** | INCREASES activation distance | Guardrail G-2 alert: RBAC adds permission configuration to the activation flow for team-based users. Admin must configure roles before team members can work. This adds 1-2 steps for team activation paths. If RBAC is built, it MUST ship with sensible defaults that don't require configuration during initial activation. Without defaults, G-2 is violated. |
| F-07: Usage Analytics | **2** | Marginal post-activation value | Dashboard provides a feedback loop that reinforces activation ("look what your team did") but doesn't reduce steps to first value. Post-activation retention tool, not an activation tool. |
| F-08: AI Act Transparency | **0** | None | Backend compliance module. Zero user interaction during activation. |
| F-09: Custom Workflows | **-1** | INCREASES activation distance | Guardrail G-2 alert: Workflow automation adds complexity to the product surface. If presented during onboarding, it increases perceived complexity. If hidden during activation and revealed later, it's neutral. Strong recommendation: if built, exclude from onboarding flow entirely. Gate behind activation milestone. |
| F-10: SSO/SAML | **5** | Reduces friction for enterprise teams | For enterprise users, SSO eliminates the signup/password-creation step and leverages existing identity. Reduces activation distance by 1 step for enterprise segment. But only affects enterprise users — no impact on mid-market or free-tier activation. |
| F-11: Bulk Data Export | **1** | None | Post-activation utility feature. Zero activation impact. |
| F-12: Real-Time Collaboration | **7** | Creates team activation path | Real-time collaboration creates a new activation vector: team members invited into a live session experience the product's value immediately (they see someone working, they can contribute). This is an alternative activation path that bypasses the solo-setup flow entirely. Projected: team activation distance could drop to 2 steps (accept invite → start collaborating). But this path only works if F-12 is built with a "join session" flow that's frictionless. |

## Key Activation Tensions

1. **F-03 vs. F-12: competing activation strategies.** F-03 reduces solo activation distance (7→3 steps). F-12 creates team activation path (potentially 2 steps). They're complementary in theory but compete for development resources. If forced to choose: F-03 has certain impact on ALL users; F-12 has larger impact but only on team users and carries high technical risk (per TECH-1).

2. **G-2 violations: F-06 and F-09 increase activation distance.** RBAC adds role configuration steps. Workflow automation adds complexity. Both features have market demand (MKT-1 scores them 7 and 6 respectively) but harm activation. Resolution: if built, both MUST ship with zero-config defaults and be excluded from the onboarding flow. This is a design constraint, not a build/no-build decision — but the design constraint adds effort (technical domain should account for it).

3. **Enterprise vs. all-segment activation:** F-10 (SSO) helps enterprise activation. F-03 helps everyone. F-12 helps teams. The activation strategy should target the funnel stage with the highest leverage. Current data: 23% drop-off at steps 4-5 affects ALL segments. F-03 addresses this directly. Enterprise-specific activation improvements (F-10) affect a smaller population.

## Recommended Priority (Activation Domain Only)

**Critical (build immediately):** F-03 (In-App Templates)
**High (strong activation benefit):** F-12 (Real-Time Collaboration) — with caveat on technical feasibility
**Moderate (segment-specific benefit):** F-10 (SSO/SAML)
**Neutral (no activation impact):** F-01, F-02, F-04, F-05, F-07, F-08, F-11
**Negative (require design constraints if built):** F-06, F-09

**G-2 enforcement note:** If F-06 or F-09 proceed, their specifications must include: (1) default role/workflow configurations requiring zero setup, (2) exclusion from onboarding flow, (3) activation distance regression test. Without these, they violate G-2 (hard guardrail).

## Cross-Boundary Claims `[ROBUST]`

One cross-domain claim: F-12 scoring references TECH-1's risk assessment ("high technical risk") as a caveat to the activation benefit. This claim is `[CROSS-DOMAIN: technical-feasibility, Deployment Complexity]` — UX-1 cannot independently verify the technical risk claim and flags it for synthesis verification. All other scores derived from market-fit domain model concepts (Activation Distance only).

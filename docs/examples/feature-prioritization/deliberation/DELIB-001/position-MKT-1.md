# Position Paper: MKT-1 (Market Fit)
**Deliberation:** DELIB-001 | **Round:** 1 | **Date:** 2026-03-19
**Domain Model:** market-fit | **Evaluation Target:** 12 candidate features (F-01 through F-12)

---

## Domain Concepts Applied

| Concept | Definition (from model) | How It Applies |
|---------|------------------------|----------------|
| Activation Distance | Steps between first interaction and first value moment | F-03 (In-App Templates) directly reduces this from 7→3. F-12 (Real-Time Collaboration) creates a new activation path for team onboarding. |
| Switching Cost Asymmetry | Difference between cost of switching TO vs. AWAY from product | F-09 (Custom Workflows), F-12 (Real-Time Collab), F-06 (RBAC) all increase outbound switching cost. F-03 reduces inbound switching cost. |
| WTP Signal | Observable behaviors indicating willingness to pay | F-04 (Slack Integration) cited in 4 deal losses. F-01 (EU Data Residency) blocking 8 enterprise prospects (€400K ARR). F-06 (RBAC) in top-3 feature requests from paying Enterprise customers. |
| Market Timing Sensitivity | Time-dependent value due to external conditions | F-01 (EU Data Residency) has a hard window — 8 blocked prospects will commit to competitors by July 2026. F-08 (AI Act Transparency) has a February 2027 deadline but lead time makes Q2 start necessary. |
| Segment Concentration Risk | Strategic risk when a feature serves only one segment | F-01, F-02, F-06, F-08, F-10 all serve primarily Enterprise. If all are prioritized, >50% of roadmap serves one segment — violating G-4. |
| Competitive Parity Gap | Features competitors have that cause measurable deal losses | F-04 (Slack Integration) is a parity gap — 4 deal losses citing this. F-10 (SSO/SAML) is a parity gap — 3 deal losses. F-12 is parity for 1 competitor only. |

## Feature Scores (1-10 scale, market perspective)

| Feature | Score | Rationale |
|---------|-------|-----------|
| F-01: EU Data Residency | **9** | Strongest WTP signal in pipeline: 8 prospects, €400K ARR blocked. Market Timing Sensitivity is HIGH — window closes July 2026. Revenue impact is concrete and immediate. |
| F-02: Automated DSAR Pipeline | **5** | No direct WTP signal from customers (they assume we handle it). Value is risk reduction, not revenue generation. Market perspective: low pull. |
| F-03: In-App Templates | **8** | Activation Distance reduction from 7→3 steps is the single highest-leverage conversion improvement available. Trial-to-paid conversion data shows 23% drop-off at steps 4-5. Serves all segments (low concentration risk). |
| F-04: Slack Integration | **7** | Competitive Parity Gap: 4 documented deal losses. WTP signal is defensive (prevents loss, doesn't create growth). But the parity gap is measurable and specific. |
| F-05: AI Code Review | **6** | WTP signal moderate — 12 feature requests from paying customers, but willingness-to-pay hasn't been validated via pricing tests. Differentiation potential is high if executed well. Segment: mid-market + enterprise (low concentration risk). |
| F-06: RBAC | **7** | Top-3 feature request from Enterprise paying customers. WTP validated: 2 expansion deals contingent on RBAC. But serves Enterprise only — concentration risk if combined with F-01, F-02, F-08, F-10. |
| F-07: Usage Analytics | **4** | Weak WTP signal — mostly requested by free-tier users. Not a parity gap (competitors vary widely). Low timing sensitivity. |
| F-08: AI Act Transparency | **3** | Zero direct market pull. No customer has requested this. Value is entirely regulatory (prerequisite for F-05 in EU). Market score reflects demand, not strategic necessity. |
| F-09: Custom Workflows | **6** | Strong Switching Cost Asymmetry potential — once customers build workflows, outbound switching cost increases substantially. But activation distance for workflows is high (complex to set up). Mixed signal. |
| F-10: SSO/SAML | **7** | Competitive Parity Gap: 3 deal losses. Enterprise table stakes — without it, enterprise deals require security exception processes that slow sales cycles by 4-6 weeks. |
| F-11: Bulk Data Export | **3** | Low WTP signal. GDPR data portability (Art. 20) has seen minimal enforcement. Reduces inbound switching cost (customers feel safer adopting) but effect is diffuse and hard to measure. |
| F-12: Real-Time Collaboration | **8** | Differentiation play — only 1 competitor has this. Creates new team activation path. High switching cost asymmetry (teams that collaborate in-tool don't leave). But effort is likely very high (not market's concern, but affects feasibility). |

## Key Market Tensions

1. **Enterprise concentration vs. revenue opportunity:** The highest-WTP features (F-01, F-06, F-10) are all Enterprise-only. Prioritizing by pure market signal would violate G-4. F-03 and F-12 are the strongest cross-segment counterweights.

2. **Parity vs. differentiation:** F-04 and F-10 are parity features (defensive). F-12 and F-05 are differentiation features (growth). Market data supports both — parity features have concrete loss data, differentiation features have higher upside but less certain returns. Current ratio if we take top 6: 2 parity, 4 growth — within the AP-2 (parity trap) guardrail.

3. **Timing urgency vs. segment balance:** F-01 has the strongest timing signal (July 2026 window) but is Enterprise-only. Deferring it to balance segments means losing €400K ARR. This is a Governor tension — market data alone cannot resolve it.

## Recommended Priority (Market Domain Only)

**Tier 1 (must-build Q2):** F-01, F-03
**Tier 2 (strong Q2/Q3):** F-12, F-06, F-04, F-10
**Tier 3 (can defer):** F-05, F-09, F-02
**Tier 4 (low market priority):** F-07, F-08, F-11

**Explicit caveat:** This ranking ignores technical feasibility and regulatory compliance. F-08 scores 3 from market perspective but may be a hard prerequisite from regulatory perspective. F-02 scores 5 from market perspective but may score much higher from regulatory enforcement risk. Cross-domain synthesis will likely reorder these significantly.

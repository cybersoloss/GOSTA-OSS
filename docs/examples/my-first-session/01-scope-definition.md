# Scope Definition: my-first-session

**Created:** 2026-03-25 (refreshed 2026-05-03 to current framework state) | **Governor:** Murat
**Scope Type:** finite
**Complexity:** simple
**Framework Version:** v6.1
**Cowork Protocol:** v3.34 (effective; per `cowork/sync-manifest.md` last entry C217)
**Deliberation Protocol:** v0.9.3
**Mode:** cowork
**Independence Level:** 2
**Deliberation Mode:** disabled
**Shortfall Logging:** disabled
**Assessment Target:** none
**Debug Logging:** disabled
**Evidence Collection Mode:** disabled
**Bootstrap Mode:** interactive (Group 1 has 10 questions; the four "disabled/none" capability flags above were declined at bootstrap)
**Analytical Frame Contract (AFC):** N/A — operational scope (feature prioritization, not analytical question)

## What This Session Is

This session conducts a structured feature prioritization exercise for the next quarter, evaluating five candidate features against two domain models: user value and engineering cost. The session will produce a ranked list of the top three features to build, along with explicit trade-off analysis and deferred features with documented rationale.

The five candidate features are: (1) User onboarding wizard, (2) API rate limiting, (3) Dark mode, (4) Audit logging, and (5) Bulk CSV import.

## Why GOSTA

Without structured governance, the AI would rank features by gut feel, using general product intuition without explicit criteria. The team needs to know: which ranking rule was used? Why did dark mode score below rate limiting? What trade-offs were made between user adoption and engineering effort? GOSTA provides:

- **Multi-domain assessment:** evaluating each feature across both user-value and engineering-cost domains, preventing bias toward either dimension
- **Transparent criteria:** domain models make ranking rules explicit and auditable
- **Cross-domain tension visibility:** showing where user-value and engineering-cost compete (e.g., dark mode is quick to build but low user value)
- **Governor hypothesis testing:** including the Governor's specific hypothesis about dark mode as an explicit test case

## Domain Models Required

| Domain Model | Source | Purpose |
|---|---|---|
| User Value | domain expertise — user behavior research, product analytics patterns | Evaluates how users perceive, adopt, and derive value from features; defines concepts like Activation Distance, Retention Signal, Perceived Complexity, WTP Indicator, Segment Reach, Habit Formation Potential |
| Engineering Cost | domain expertise — software engineering estimation, technical debt research | Evaluates technical effort, risk, and maintenance burden; defines concepts like Effort Estimate Confidence, Dependency Chain Length, Reversibility, Maintenance Burden, Technical Debt Multiplier, Integration Surface Area |

## Success Criteria

- Ranked list of 3 features prioritized for next quarter with numeric scores in both domains
- Cross-domain trade-off analysis: areas where features excel in user-value but challenge engineering-cost, and vice versa
- Deferred features (bottom 2) with explicit rationale grounded in domain model concepts
- Governor hypothesis testing: HL-4 (dark mode scoring) confirmed or refuted with evidence
- Guardrail compliance check: all five features assessed against single-developer constraint, 12-week budget constraint, no-breaking-changes constraint
- Governor sign-off on the final recommendation

## Constraints

- **Timeline:** Single developer, 12-week budget available for the quarter
- **Resources:** Solo developer, no parallelization — features execute sequentially
- **Technical:** No breaking changes to public API during implementation
- **Governance:** Governor (Murat) must approve the final recommendation before features commit to the roadmap

## Risk Factors

- **Estimation uncertainty:** Features with low Effort Estimate Confidence (e.g., bulk CSV import if internal data model is undocumented) may slip in actual implementation
- **Dependency risk:** If any feature depends on third-party infrastructure or API changes not yet confirmed, sequential execution with one developer creates bottleneck risk
- **User feedback gap:** User-value scoring relies on best estimates of Retention Signal and Activation Distance; actual user behavior may differ post-launch
- **Hypothesis bias:** The Governor's hypothesis about dark mode (HL-4) may reflect domain knowledge or market intuition that domain models don't capture; scoring should test but not presume this hypothesis

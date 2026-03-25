# Signal: Engineering Cost Scoring

**Date:** 2026-03-25 | **Scope:** my-first-session | **TAC:** TAC-2
**Domain Model:** engineering-cost.md

---

## Feature 1: User Onboarding Wizard

### Effort Estimate Confidence

**Concept Definition:** The reliability of the engineering effort estimate for a feature. High confidence means the team has shipped similar features before and can predict implementation time accurately.

**Application to this feature:** Onboarding wizards are a standard pattern in SaaS. If the team has built multi-step workflows before, this estimate is high-confidence. The wizard involves: form validation, step navigation, data storage, completion tracking. These are well-understood patterns.

**Score:** 8/10 | **Effort Estimate:** 3 weeks

**Justification:** High confidence because onboarding wizards are a known pattern. Estimate: 3 weeks assumes: 1 week UI/UX design and prototyping, 1 week backend data model and APIs, 1 week integration testing and refinement. Confidence is 8, not 10, because every product's data model is unique and customization needs vary.

---

### Dependency Chain Length

**Concept Definition:** The number of sequential dependencies that must be resolved before implementation can complete.

**Application to this feature:** Onboarding wizard depends on: (1) data model finalization (what data does the wizard capture?), (2) user authentication system already operational. Both are likely pre-existing, making chain length 1 (single upstream dependency: data model). If data model is already defined, chain length is 0.

**Score:** 8/10 (chain length: 1 dependency, low risk)

**Justification:** The wizard depends on data model finalization, but this is an internal dependency, not external or third-party. Chain length is short. Score is 8 because the data model dependency could create a 1-week wait if it's not already finalized, but the dependency is low-risk overall.

---

### Reversibility

**Concept Definition:** The cost and complexity of undoing or rolling back a feature if it causes production issues.

**Application to this feature:** An onboarding wizard is fully reversible: if it causes issues, the team can disable it (feature flag) or remove it without affecting production data or user accounts. The wizard doesn't modify core data structures or alter the public API.

**Score:** 9/10

**Justification:** Onboarding wizards are fully reversible. Operational rollback is easy (disable in code, toggle in config). Users who completed the wizard retain their data. No data migration needed for rollback. Score is 9, not 10, because disabling the wizard mid-production may confuse returning users, but this is operational concern, not technical risk.

---

### Maintenance Burden

**Concept Definition:** The ongoing operational cost to keep a feature working post-launch.

**Application to this feature:** Onboarding wizard maintenance burden is low: monitor completion rates, fix bugs in wizard flow, update wizard copy for new features, support customers who skip the wizard. Estimated ongoing burden: 2-3 hours per quarter.

**Score:** 8/10 (low maintenance burden)

**Justification:** The wizard is relatively isolated from other systems, so maintenance burden is low. It will require occasional updates (new steps, copy changes), but won't be a source of ongoing support overhead. Score is 8, not 10, because wizard bugs can degrade new user experience and may generate support tickets.

---

### Technical Debt Multiplier

**Concept Definition:** The degree to which implementing this feature creates technical debt that impairs future velocity.

**Application to this feature:** An onboarding wizard creates no significant technical debt if implemented cleanly. It's isolated from core systems. Future features won't need to route around the wizard or work around its architecture. Multiplier is low.

**Score:** 8/10 (multiplier: 1.1x — minimal debt)

**Justification:** The feature is architecturally clean if designed properly. No core systems are compromised. Future velocity is unaffected. The multiplier is 1.1x (slightly above zero) only because every feature adds complexity to the codebase. Score is 8 because minimal debt is expected.

---

### Integration Surface Area

**Concept Definition:** The number of existing systems or APIs that this feature touches or must integrate with.

**Application to this feature:** Onboarding wizard touches: (1) user authentication system, (2) data model/storage, (3) UI framework. Surface area: 3 systems. Integration is moderate.

**Score:** 7/10 (surface area: 3 systems)

**Justification:** The wizard integrates with multiple systems (auth, data, UI), creating moderate integration surface area. Integration testing is required, but none of the touched systems are high-risk. Score is 7, not 5, because the integrations are straightforward (no unusual API usage).

---

### Per-Feature Engineering-Cost Total: 48/60 = 8.0 average

**Estimated Effort:** 3 weeks | **Confidence:** High
**Summary:** Onboarding wizard is a low-cost, low-risk feature with a well-understood pattern, short dependencies, full reversibility, and minimal ongoing burden. High confidence in 3-week estimate.

---

## Feature 2: API Rate Limiting

### Effort Estimate Confidence

**Concept Definition:** The reliability of the engineering effort estimate for a feature.

**Application to this feature:** API rate limiting is a standard pattern but implementation details vary significantly based on the system's current architecture. If the system already has quota infrastructure, implementation is quick. If quota is not in place, this is moderate-complexity. Confidence depends on existing architecture knowledge.

**Score:** 7/10 | **Effort Estimate:** 3.5 weeks

**Justification:** Moderate-high confidence because rate limiting is a known pattern, but implementation depends on existing infrastructure. Estimate: 3.5 weeks assumes: 1 week quota system design and schema, 1 week API middleware integration, 1 week testing and documentation, 0.5 weeks for handling edge cases. Confidence is 7, not 9, because architectural dependencies are unknown without deeper review.

---

### Dependency Chain Length

**Concept Definition:** The number of sequential dependencies that must be resolved before implementation can complete.

**Application to this feature:** API rate limiting depends on: (1) quota system architecture decision (how to store/track quota), (2) API infrastructure stable. The quota decision could block other work if not resolved. Chain length: 1-2 dependencies.

**Score:** 6/10 (chain length: 2 dependencies, moderate risk)

**Justification:** The feature has two upstream dependencies: quota architecture and API stability. If either is uncertain, the estimate becomes provisional. Chain length is longer than onboarding wizard, creating moderate blocking risk. Score is 6, not 4, because both dependencies are internal and relatively low-risk.

---

### Reversibility

**Concept Definition:** The cost and complexity of undoing or rolling back a feature if it causes production issues.

**Application to this feature:** API rate limiting is moderately reversible. If it causes issues (false positives, overly aggressive throttling), the team can disable it via configuration. However, if developers have already written retry logic against the new rate limits, disabling the feature removes the feedback they've built against, requiring their code to adapt. Reversibility is moderate.

**Score:** 7/10

**Justification:** Rate limiting can be disabled via configuration (good reversibility), but developers may have adapted their code, making rollback less clean. Score is 7, not 9, because the rollback path exists but may require coordination with customers.

---

### Maintenance Burden

**Concept Definition:** The ongoing operational cost to keep a feature working post-launch.

**Application to this feature:** API rate limiting has moderate maintenance burden: monitoring quota consumption, tuning rates for different API endpoints, handling customer complaints about rate limits, supporting developers integrating retry logic. Estimated burden: 4-5 hours per quarter.

**Score:** 6/10 (moderate maintenance burden)

**Justification:** The feature generates ongoing support overhead because developers will hit limits and need guidance on retry logic. Quota tuning may be required based on usage patterns. Score is 6, reflecting real ongoing work.

---

### Technical Debt Multiplier

**Concept Definition:** The degree to which implementing this feature creates technical debt that impairs future velocity.

**Application to this feature:** API rate limiting creates moderate technical debt if not designed cleanly. If the quota system is a quick implementation, it will block future API improvements (scaling, schema changes). If it's architecturally sound, debt is minimal. Multiplier: 1.3x (moderate).

**Score:** 6/10 (multiplier: 1.3x — moderate debt)

**Justification:** The feature can create debt if quota is tightly coupled to API endpoints. Clean architecture minimizes debt. Score is 6, not 8, because there's real risk of technical debt here if not designed carefully. This is a factor in favor of deferring or careful design.

---

### Integration Surface Area

**Concept Definition:** The number of existing systems or APIs that this feature touches or must integrate with.

**Application to this feature:** API rate limiting touches: (1) API gateway/middleware, (2) quota storage system, (3) monitoring/alerting. Surface area: 3 systems. Integration is moderate.

**Score:** 6/10 (surface area: 3 systems)

**Justification:** Integration involves quota storage and API middleware, both potentially complex. Monitoring integration is straightforward. Score is 6, not 7, because quota storage integration could be tricky depending on existing infrastructure.

---

### Per-Feature Engineering-Cost Total: 38/60 = 6.3 average

**Estimated Effort:** 3.5 weeks | **Confidence:** Moderate-High
**Summary:** API rate limiting is moderate cost, moderate risk, with longer dependencies and potential for technical debt if not designed carefully. 3.5-week estimate with moderate confidence.

---

## Feature 3: Dark Mode

### Effort Estimate Confidence

**Concept Definition:** The reliability of the engineering effort estimate for a feature.

**Application to this feature:** Dark mode is the simplest feature on this list. It involves: CSS theming, color variable definitions, user preference storage, UI toggle. All well-established patterns. Confidence is very high.

**Score:** 9/10 | **Effort Estimate:** 1.5 weeks

**Justification:** Very high confidence because dark mode is a standard, well-understood pattern used in thousands of products. Estimate: 1.5 weeks assumes: 3 days CSS/theme work, 2 days backend preference storage, 2 days UI toggle and testing. Confidence is 9, not 10, because codebase-specific complexity might add surprise work.

---

### Dependency Chain Length

**Concept Definition:** The number of sequential dependencies that must be resolved before implementation can complete.

**Application to this feature:** Dark mode has zero external dependencies. It's purely internal: CSS, user preferences, toggle. Chain length: 0.

**Score:** 9/10 (chain length: 0, no dependencies)

**Justification:** Dark mode is completely independent. No architectural decisions needed, no third-party integrations, no upstream blockers. It can be implemented in parallel with any other work. Score is 9 (very low dependency risk).

---

### Reversibility

**Concept Definition:** The cost and complexity of undoing or rolling back a feature if it causes production issues.

**Application to this feature:** Dark mode is fully reversible. If there are CSS bugs or accessibility issues, the feature can be disabled (feature flag) without affecting user data. Users who enabled dark mode simply see light mode again. No data migration, no breaking changes.

**Score:** 10/10

**Justification:** Fully reversible. Zero operational complexity for rollback. Feature flag can disable it entirely if needed. Score is 10.

---

### Maintenance Burden

**Concept Definition:** The ongoing operational cost to keep a feature working post-launch.

**Application to this feature:** Dark mode has very low maintenance burden: occasional CSS tweaks, accessibility reviews, support for users who want to report dark mode bugs. Estimated burden: 1-2 hours per quarter.

**Score:** 9/10 (very low maintenance burden)

**Justification:** The feature is mostly fire-and-forget once shipped. Users enable/disable as they prefer. Minimal support overhead. Score is 9, not 10, because every UI feature generates occasional edge-case bug reports (contrast issues, missing dark mode styles in new sections).

---

### Technical Debt Multiplier

**Concept Definition:** The degree to which implementing this feature creates technical debt that impairs future velocity.

**Application to this feature:** Dark mode creates near-zero technical debt if implemented with CSS variables and theme abstraction. Future features automatically get dark mode support. Multiplier: 1.0x (no debt).

**Score:** 9/10 (multiplier: 1.0x — no debt)

**Justification:** Proper implementation (theme variables, CSS abstraction) creates no debt. Future features inherit dark mode automatically. Score is 9, not 10, because poorly implemented dark mode (hard-coded colors) could create debt, but this assumes quality implementation.

---

### Integration Surface Area

**Concept Definition:** The number of existing systems or APIs that this feature touches or must integrate with.

**Application to this feature:** Dark mode touches: (1) CSS framework, (2) user preferences storage. Surface area: 2 systems. Integration is minimal.

**Score:** 9/10 (surface area: 2 systems, minimal)

**Justification:** Dark mode has minimal integration surface. It's primarily CSS and user preference storage, both straightforward. Score is 9 because integration is clean and low-risk.

---

### Per-Feature Engineering-Cost Total: 55/60 = 9.2 average

**Estimated Effort:** 1.5 weeks | **Confidence:** Very High
**Summary:** Dark mode is the lowest-cost, lowest-risk feature. Trivial implementation, zero dependencies, fully reversible, minimal maintenance, no debt. Very high confidence in 1.5-week estimate.

---

## Feature 4: Audit Logging

### Effort Estimate Confidence

**Concept Definition:** The reliability of the engineering effort estimate for a feature.

**Application to this feature:** Audit logging is a complex feature with many design decisions: what events to log, log retention, query interface, compliance requirements. Confidence depends on understanding compliance requirements and existing logging infrastructure.

**Score:** 5/10 | **Effort Estimate:** 9 weeks

**Justification:** Low-moderate confidence because audit logging requires understanding compliance requirements that may not be fully specified. Estimate: 9 weeks assumes: 2 weeks design (event taxonomy, schema, retention policy), 3 weeks event capture implementation, 2 weeks query interface, 1 week compliance review and testing, 1 week documentation. Confidence is 5, not 3, because audit logging patterns are understood, but requirements are unclear.

---

### Dependency Chain Length

**Concept Definition:** The number of sequential dependencies that must be resolved before implementation can complete.

**Application to this feature:** Audit logging depends on: (1) compliance requirements clarification (what must be logged?), (2) event taxonomy alignment with team, (3) potentially external legal review (SOC2, HIPAA, GDPR compliance). Chain length: 3 dependencies, some external.

**Score:** 3/10 (chain length: 3+ dependencies, high risk)

**Justification:** Long dependency chain with external blockers (legal, compliance). If any dependency is delayed, the tactic is blocked. This is high-risk. Score is 3, not 1, because these are solvable dependencies, not unknowns.

---

### Reversibility

**Concept Definition:** The cost and complexity of undoing or rolling back a feature if it causes production issues.

**Application to this feature:** Audit logging is partially reversible. The code can be disabled, but audit log data already captured is historical. If the logging system has a bug that results in data loss or incorrect logging, that damage is permanent. Reversibility is low.

**Score:** 4/10

**Justification:** Partial reversibility. Code can be disabled, but captured data is permanent. If there are security or data quality issues with the logging system, rollback doesn't undo recorded events. Score is 4, not 2, because operational rollback (disable logging) is straightforward, but data integrity issues are real.

---

### Maintenance Burden

**Concept Definition:** The ongoing operational cost to keep a feature working post-launch.

**Application to this feature:** Audit logging has high maintenance burden: monitoring log storage and retention, handling customer queries about logs, supporting audits, tuning log retention policies, handling compliance changes. Estimated burden: 8-10 hours per quarter.

**Score:** 2/10 (high maintenance burden)

**Justification:** Audit logging is a high-maintenance feature. Compliance requirements change, customers file audit requests, storage costs require monitoring, and regulatory changes require periodic updates. Score is 2 (high burden), not 1, because these are well-understood operational costs.

---

### Technical Debt Multiplier

**Concept Definition:** The degree to which implementing this feature creates technical debt that impairs future velocity.

**Application to this feature:** Audit logging can create significant technical debt if not designed cleanly. If logging is tightly coupled to core data operations, future refactoring requires audit system changes. Multiplier: 1.8x (significant debt potential).

**Score:** 2/10 (multiplier: 1.8x — high debt risk)

**Justification:** Audit logging creates real technical debt risk. If the event taxonomy is wrong or the logging is too tightly integrated, future work is blocked. Score is 2 (high risk), because this is a critical risk factor. This is a reason to defer unless requirements are crystal clear.

---

### Integration Surface Area

**Concept Definition:** The number of existing systems or APIs that this feature touches or must integrate with.

**Application to this feature:** Audit logging touches: (1) all data-modifying operations (capture point), (2) audit storage system, (3) query interface, (4) monitoring, (5) compliance framework. Surface area: 5+ systems. Integration is extensive.

**Score:** 2/10 (surface area: 5+ systems, extensive)

**Justification:** Audit logging must integrate with every data-modifying operation in the system. This is broad, invasive integration. Changing any operation requires audit consideration. Score is 2, not 1, because the integrations are predictable, but the surface area is massive.

---

### Per-Feature Engineering-Cost Total: 16/60 = 2.7 average

**Estimated Effort:** 9 weeks | **Confidence:** Low-Moderate
**Summary:** Audit logging is the highest-cost, highest-risk feature. Long dependencies, unclear requirements, high maintenance burden, significant technical debt risk, extensive integration surface. 9-week estimate with low confidence. This feature exceeds 12-week budget when combined with other features.

---

## Feature 5: Bulk CSV Import

### Effort Estimate Confidence

**Concept Definition:** The reliability of the engineering effort estimate for a feature.

**Application to this feature:** Bulk CSV import is moderate complexity: CSV parsing, data validation, error handling, import queue, user notifications. The pattern is well-known, but details depend on the product's data model. Confidence is moderate.

**Score:** 7/10 | **Effort Estimate:** 5 weeks

**Justification:** Moderate confidence because CSV import is a standard pattern, but implementation depends on data model complexity. Estimate: 5 weeks assumes: 1 week CSV parsing and validation, 1.5 weeks data integration, 1 week error handling and user notifications, 1 week testing and edge cases, 0.5 weeks documentation. Confidence is 7, not 9, because data model unknowns could add surprise work.

---

### Dependency Chain Length

**Concept Definition:** The number of sequential dependencies that must be resolved before implementation can complete.

**Application to this feature:** Bulk CSV import depends on: (1) data model finalization, (2) potentially external file storage if using cloud. Chain length: 1-2 dependencies (internal, low risk).

**Score:** 7/10 (chain length: 1-2 dependencies, low-moderate risk)

**Justification:** The feature has a short dependency chain (data model), both internal. File storage is a known external dependency (AWS S3, etc.) that's already operational. Score is 7, not 8, because data model uncertainty could create a 1-week wait.

---

### Reversibility

**Concept Definition:** The cost and complexity of undoing or rolling back a feature if it causes production issues.

**Application to this feature:** Bulk CSV import is moderately reversible. If the import system has bugs that result in incorrect data being loaded, remediation is complex (manual data cleanup, transaction rollback in some cases). The feature can be disabled, but damaged data requires cleanup.

**Score:** 5/10

**Justification:** Partial reversibility. Feature can be disabled operationally (feature flag), but data integrity issues require manual remediation. Score is 5, reflecting moderate reversibility and real risk of data damage if import validation has bugs.

---

### Maintenance Burden

**Concept Definition:** The ongoing operational cost to keep a feature working post-launch.

**Application to this feature:** Bulk CSV import has moderate maintenance burden: troubleshooting import failures, handling edge cases in CSV format, supporting customers with import issues, tuning validation rules. Estimated burden: 4-5 hours per quarter.

**Score:** 6/10 (moderate maintenance burden)

**Justification:** The feature generates moderate support overhead because CSV formats vary widely and customers struggle with validation errors. Score is 6, not 4, because the feature is relatively mature once shipped and issues stabilize.

---

### Technical Debt Multiplier

**Concept Definition:** The degree to which implementing this feature creates technical debt that impairs future velocity.

**Application to this feature:** Bulk CSV import creates low-moderate technical debt if designed cleanly (separate import service, async processing). If it's tightly integrated into core data operations, debt is higher. Multiplier: 1.2x (low-moderate).

**Score:** 7/10 (multiplier: 1.2x — low-moderate debt)

**Justification:** With clean architecture (async import, separate validation), technical debt is minimal. If done carelessly (synchronous import, inline validation), debt is higher. Score is 7, assuming reasonable design.

---

### Integration Surface Area

**Concept Definition:** The number of existing systems or APIs that this feature touches or must integrate with.

**Application to this feature:** Bulk CSV import touches: (1) file storage/upload, (2) data validation system, (3) data persistence layer, (4) activity/audit logging, (5) user notifications. Surface area: 5 systems. Integration is moderate-to-broad.

**Score:** 5/10 (surface area: 5 systems, moderate-broad)

**Justification:** The feature touches multiple systems (storage, validation, persistence, logging, notifications), creating moderate integration surface area. Integration is straightforward but broad. Score is 5, reflecting the breadth without extreme complexity.

---

### Per-Feature Engineering-Cost Total: 37/60 = 6.2 average

**Estimated Effort:** 5 weeks | **Confidence:** Moderate
**Summary:** Bulk CSV import is moderate cost, moderate risk, with short dependencies and reasonable reversibility. 5-week estimate with moderate confidence. Fits within budget as part of three-feature set.

---

## Summary Table

| Feature | Effort Confidence | Dependency Chain | Reversibility | Maintenance Burden | Technical Debt | Integration Surface | Total | Effort (weeks) |
|---|---|---|---|---|---|---|---|---|
| Onboarding Wizard | 8 | 8 | 9 | 8 | 8 | 7 | 48 | 3 |
| API Rate Limiting | 7 | 6 | 7 | 6 | 6 | 6 | 38 | 3.5 |
| Dark Mode | 9 | 9 | 10 | 9 | 9 | 9 | 55 | 1.5 |
| Audit Logging | 5 | 3 | 4 | 2 | 2 | 2 | 16 | 9 |
| Bulk CSV Import | 7 | 7 | 5 | 6 | 7 | 5 | 37 | 5 |

**Budget Analysis:**
- Top 3 combinations that fit 12-week budget:
  1. Onboarding (3) + Dark Mode (1.5) + Bulk CSV (5) = 9.5 weeks ✓
  2. Onboarding (3) + Dark Mode (1.5) + API Rate Limiting (3.5) = 8 weeks ✓
  3. Onboarding (3) + API Rate Limiting (3.5) + Bulk CSV (5) = 11.5 weeks ✓

**Key Finding:** Audit Logging at 9 weeks cannot be combined with more than one other feature without exceeding 12-week budget. This is the key constraint that forces audit logging to be deferred.


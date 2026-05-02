# Evidence Collection Configuration — [SESSION_NAME]

**Generated:** [date]
**Session:** [SESSION_NAME]
**Target(s):** [assessment target(s)]
**Derived from:** §14.8 Evidence Collection Architecture, evidence-collection-protocol.md

---

## Assessment Type

[hypothesis-driven / exploratory]
<!-- Determines audit mode: directional bias audit (hypothesis) or coverage audit (exploratory) -->

## Collection Topology

[single-target / multi-target-shared / multi-target-parallel]

### Targets

<!-- For single-target, one entry. For multi-target, list all. -->

| Target | Short Name | Description |
|--------|-----------|-------------|
| [target 1] | [TAG-1] | [brief description] |

## Execution Environment

<!-- Auto-detected. Record for audit. -->

- Session mode: [code / cowork]
- Web search available: [yes / no / pending test]
- Execution environment: [normal / pre-fetch / cowork-sequential]

## Independence Level Interaction

<!-- Auto-computed from Group 1 independence level. -->

- Independence level: [1 / 2 / 3]
- Quality gate behavior:
  - [Level 1-2: All warnings and failures require Governor review]
  - [Level 3: FAIL halts. Coverage-mode WARN escalates to Governor disposition regardless of independence (cascading verdict-confidence implications). Other WARN classes (directional ratio, etc.) auto-resolve with logged rationale.]
- Adversarial dispatch: [Governor pre-reviews / auto-dispatched]
- Reconciliation: [All contradictions halt / minor auto-resolve, invalidations halt]

## Collection Agents

<!-- Agent categories are derived from the session's domain models, not predefined. -->
<!-- Formula: ceil(domain_count / 2) + 1 discovery + 1 adversarial -->

| Agent | Source Category | Feeds Domains | Search Specification |
|-------|----------------|---------------|---------------------|
| Agent 1 | [derived from domain grouping] | [DOMAIN-1, DOMAIN-2] | See §[N] below |
| ... | ... | ... | ... |
| Agent N-1 | Discovery | ALL | See Discovery Queries below |
| Agent N | **Adversarial** | ALL | See Adversarial Specification below |

## Search Specifications

### Agent 1: [Category Name]

| Search Target | Queries | Expected Evidence |
|---|---|---|
| ... | ... | ... |

<!-- Repeat for each domain agent -->

## Discovery Queries

### Target-Level Discovery

[Broad queries for the assessment target — derived from target name and scope]

### Component-Level Discovery

[Broad queries for specific components/sub-topics of the assessment target]

## Evidence Thresholds

| Domain | Min Tier 1/2 (target-level) | Min Tier 1/2 (component-level) | Notes |
|--------|---------------------------|-------------------------------|-------|
| ... | 3 (default) | 2 (default) | ... |

## Source Attribution Tier Policy

<!-- Use framework defaults (§14.8 default 3-tier) or customize. -->

| Tier | Sources | Weight | Sole-basis for score? |
|---|---|---|---|
| 1 | [session-specific Tier 1 sources] | Highest | Yes |
| 2 | [session-specific Tier 2 sources] | High | Yes |
| 3 | [session-specific Tier 3 sources] | Supporting only | No — must be cross-referenced |

## Adversarial Specification

### Mode

[counter-framing / cross-verification]
<!-- Default: counter-framing for hypothesis-driven and exploratory; cross-verification for purely factual -->

### Counter-Framing (if counter-framing mode)

<!-- Auto-generated, Governor-reviewed before dispatch -->
<!-- For hypothesis-driven: invert the OD hypothesis -->
<!-- For exploratory: derived from domain model scoping exclusions (§13 scope boundaries) -->

[Counter-framing specification]

### Adversarial Search Queries

| Search Target | Counter-Framing Queries | Expected Counter-Evidence |
|---|---|---|
| ... | ... | ... |

### Cross-Verification Sample (if cross-verification mode)

- Sample size: min(10, 30% of total items)
- Selection method: random sample of other agents' factual claims

## Quality Gate Configuration

| Gate | Setting | Default |
|------|---------|---------|
| Evidence quality audit mode | [directional / coverage] | directional (hypothesis-driven) or coverage (exploratory) |
| Directional bias threshold | [percentage] | 70% (only if directional mode) |
| Coverage threshold | [percentage] | 80% concept coverage (only if coverage mode) |
| URL verification sample | [Tier 1 rate / Tier 2 rate] | 100% / 30% |
| Adversarial collection | [enabled / disabled] | enabled |
| Adversarial mode | [counter-framing / cross-verification] | counter-framing (hypothesis/exploratory) or cross-verification (factual) |

## Concept-to-Query Mapping

<!-- Auto-generated from domain model core concepts during bootstrap Step 5c -->

| Domain | Core Concept | Evidence Queries |
|---|---|---|
| ... | ... | ... |

## Pool-Agent Store Build and Per-Domain Loading

- Expected evidence volume: [estimated item count]
- Pool-agent vector store: [enabled if >50 items / disabled]
- Score thresholds: >=0.58 read full, 0.50-0.57 excerpt, <0.50 ignore
- Per-domain loading threshold: 30
  <!-- Items per domain. At dispatch time, domains with more items than this threshold
       use pool-agent retrieval instead of direct file loading. Default: 30 items
       (~9K tokens of evidence). Adjust based on models used — smaller context windows
       may need a lower threshold. See evidence-collection-protocol §6.4. -->

## Evidence Archive Import

<!-- Populated during Step 5b if archive exists -->

- Archive queried: [yes / no / no archive exists]
- Matching items found: [N]
- Items within effective date: [M]
- Expired items: [K]
- Governor decision: [import N items / start fresh]
- Imported items flagged for re-verification: [yes / N/A]

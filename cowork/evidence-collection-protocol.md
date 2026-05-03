# Evidence Collection Protocol

**Tier 0 Operationalization of §14.8 Evidence Collection Architecture**

---

## §1 Overview

### §1.1 Purpose

This protocol operationalizes §14.8 (Evidence Collection Architecture) at Tier 0. It defines the procedures for collecting, storing, verifying, and surfacing evidence during GOSTA sessions that require structured evidence gathering.

§14.8 defines the architecture — schemas, topologies, quality gates. This protocol defines the execution procedures — how a coordinator dispatches agents, manages storage, runs quality checks, and produces the evidence manifest that downstream assessment phases consume.

### §1.2 Activation

Evidence collection is **optional**. Sessions that do not require evidence gathering skip this protocol entirely.

- **Governor enables** evidence collection at bootstrap (startup.md Step 3, Group 3B).
- **Startup.md Group 3B** configures collection parameters in `evidence-collection-config.md`.
- If not enabled, no `osint/` directory is created and no collection agents are dispatched.

### §1.3 Relationship to Spec

| Spec Section | This Protocol |
|---|---|
| §14.8 Evidence Collection Architecture | §2 Schema Reference, §5 Storage, §6 Manifest, §6.4 Pre-Dispatch Content Estimation |
| §14.8 Source Attribution Tiers | §2.2, §10.2 Source Verification |
| §14.8 Collection Topologies | §2.6, §3 Agent Dispatch |
| §14.8 Quality Gates | §10 Quality Gates |
| §14.3.11 Verification Extensions | §10.5, §11 Verification Reference |
| §22.4 Evidence Collection Protocol Pattern | §3–§4 Collection Procedures |
| §13.6 Domain Model Minimums | §4 Ad-hoc Domain Creation |

### §1.4 Scope

This protocol governs:
- Evidence collection agent configuration and dispatch
- Evidence item creation and storage
- Adversarial collection
- Open-ended discovery and escalation
- Evidence manifest generation
- All quality gates prior to assessment
- Post-session evidence archiving

It does **not** govern how assessment agents interpret evidence — that belongs to the assessment phase of the session's Operating Document.

---

## §2 Schema Reference and Configuration

### §2.1 Evidence Item Schema

Evidence items follow the schema defined in §14.8. At Tier 0, items are stored as YAML front matter in markdown files.

```yaml
# Evidence Item — Tier 0 Format
id: OSINT-[NNN]
source: "[Source name — organization or platform]"
url: "[URL if available, or null for non-web sources]"
collected_date: "[YYYY-MM-DD]"
tier: [1|2|3]  # per source attribution tier framework
summary: "[1-3 sentence summary of what this evidence establishes]"
domain_tags: ["[DOMAIN-1]", "[DOMAIN-2]"]
level: "[target-level | component-level]"
category: "[thematic classification within domain]"
impact_estimate: "[directional indicator for triage]"
content_file: "osint/[category]/[filename].md"
contradicts: ["OSINT-[NNN]"]  # optional, list of contradicted item IDs
target: "[assessment target name]"
adversarial: [true | false]  # default: false
```

The full content of the evidence item follows the YAML front matter as markdown body text. Sessions may define additional extension fields beyond these core fields — extension fields are documented in the session's `evidence-collection-config.md`.

### §2.2 Source Attribution Tiers

§14.8 defines a default 3-tier source attribution framework. The framework defines the classification pattern (ordinal tiers with defined reliability semantics where lower numbers indicate higher reliability); protocols and sessions define the specific tier count and values.

| Tier | Reliability | Typical Sources |
|---|---|---|
| 1 | Primary / authoritative | Official filings, regulatory databases, vendor's own published documentation, peer-reviewed research, court records |
| 2 | Credible secondary | Established analyst firms, reputable industry publications, structured databases with editorial oversight |
| 3 | Tertiary / unverified | Blogs, forums, social media, press releases (self-reported claims), undated or anonymous sources |

Sessions may customize tier definitions in `evidence-collection-config.md` — including using more granular (e.g., 5-tier) or coarser (e.g., 2-tier) structures. Tier assignments by collection agents are provisional — §14.3.11 Check 1 (Tier Re-classification) may adjust them.

### §2.3 Evidence Manifest

§14.8 defines the evidence manifest schema. At Tier 0, the manifest is a markdown document at `osint/evidence-manifest.md`. See §6 for generation procedure.

### §2.4 Evidence Collection Configuration

`evidence-collection-config.md` is populated during bootstrap (startup.md Group 3B). It contains:

- **Targets**: what evidence is collected about (one or more named targets)
- **Search specifications**: per-domain search guidance derived from OD objectives
- **Source tier customizations**: session-specific additions to the tier framework
- **Collection topology**: which §14.8 topology applies (§2.6)
- **Quality gate thresholds**: override defaults for source verification sample rates, evidence sufficiency minimums, engagement thresholds
- **Adversarial mode**: counter-framing or cross-verification (§3.3)
- **Evidence quality audit mode**: directional or coverage (§10.3)

A template for this file is provided in `cowork/templates/`.

### §2.5 Capability Detection and Fallback

Evidence collection operates in one of three execution environments:

| Environment | Detection | Characteristics |
|---|---|---|
| Code-mode normal | Agent dispatch with web search succeeds | Full parallel collection, information isolation |
| Code-mode pre-fetch | Agent dispatch with web search fails | Coordinator fetches, agents analyze files |
| Cowork-mode sequential | Session mode is cowork | Sequential role-play, no information isolation |

**Auto-detection procedure:**

**For code-mode sessions:** At the start of the collection phase, the coordinator dispatches a single test agent with a WebSearch tool request via ToolSearch. If the agent successfully returns web search results, the session operates in **normal mode**. If the dispatch fails or web search is unavailable, the session falls back to **pre-fetch mode**.

**For cowork-mode sessions:** Detected automatically from the session mode declared in the Operating Document. No capability test is needed.

Record the result in `osint/capability-test.md`:

```markdown
# Capability Test Result
- Date: [YYYY-MM-DD]
- Session mode: [code | cowork]
- Web search available: [yes | no]
- Execution environment: [normal | pre-fetch | cowork-sequential]
- Test method: [agent dispatch test | session mode detection]
```

**Cowork mode limitations:** No information isolation between collection roles. The adversarial role is especially important in cowork mode because the coordinator has seen all prior collection output — the adversarial framing compensates for confirmation bias that information bleed creates.

### §2.6 Collection Topology

§14.8 defines three collection topologies:

1. **Single-target** — one target, all collection agents contribute to one evidence pool. Default and most common.
2. **Multi-target-shared** — multiple targets assessed simultaneously, agents collect across targets. One shared manifest with per-target sections.
3. **Multi-target-parallel** — multiple targets, each with its own collection agent set and evidence pool. Per-target manifests.

At Tier 0, topology is set in `evidence-collection-config.md`. The default is single-target.

For multi-target-parallel with more than 15 total agents (agents_per_target × target_count), use **sequential batching**: complete each target's full collection cycle (collection → quality gates → manifest) before starting the next. The Governor decides whether to batch or run parallel.

---

## §3 Collection Agent Dispatch

### §3.1 Agent Configuration

Collection agents are derived from the session's domain models — not hardcoded. The number and specialization of agents adapts to the session's analytical structure.

**Agent count formula:**

```
total_agents = ceil(domain_count / 2) + 1 (discovery) + 1 (adversarial)
```

Where `domain_count` is the number of domains in the session's domain models. Each agent covers 1–2 related domains.

**Each agent receives:**
- **Dispatch Preamble**: assembled per cowork protocol §7.5 — includes AFC injection (when AFC exists) and debug logging injection (when enabled). The Dispatch Verification Check confirms preamble completeness before dispatch.
- **Target name**: from `evidence-collection-config.md`
- **Search specification**: domain-specific search guidance from config
- **Source attribution tier rules**: session's tier definitions (§2.2)
- **Output format instructions**: evidence item schema **embedded as literal fenced YAML block** (per §2.1; see Schema Literal-Embedding Requirement below), storage location (§5)

**Schema Literal-Embedding Requirement (Plan #22) `[CORE]`.** The dispatch prompt for every collection agent MUST include the canonical evidence-item schema (§2.1) as a literal fenced YAML block embedded inline, NOT as a section reference (e.g., NOT "see §2.1"). Reference-by-section requires the dispatched agent to look up the protocol; lookup-and-forget is a discipline-failure mode that has produced schema heterogeneity across collection agents (one agent in a session used `osint_id` instead of `id`, `title` instead of canonical schema fields, etc., despite §2.1 being available; downstream tooling required schema normalization at manifest generation). Literal embedding eliminates the lookup step at the source — the agent has the schema inline as the reference for its YAML front-matter output. Embedding cost: ~15-20 lines added to the dispatch prompt; benefit: removes the failure surface that produced cross-agent schema heterogeneity. Sessions whose evidence schema is non-canonical (custom session-specific schema) embed the session's schema verbatim rather than the framework default. The Dispatch Verification Check (cowork-protocol §7.5) extends accordingly to verify schema literal-embedding is present in the assembled dispatch prompt.
- **Domain assignment**: which domain model domains this agent covers

Agents operate independently. In code-mode normal, they have no access to other agents' findings during collection.

### §3.2 Collection Agent Output

Each agent writes structured evidence items to `osint/[category]/` where `[category]` corresponds to the agent's assigned domain(s).

For each item collected, the agent MUST:

1. **Assign a source tier** per §2.2 definitions
2. **Tag domains** — every item tagged with one or more domain names
3. **Specify level** — target-level or component-level
4. **Write summary** — 2–4 sentence summary in the YAML front matter
5. **Save full content** — complete evidence text as markdown body
6. **Flag contradictions** — if the item contradicts a previously collected item, populate the `contradicts` field

Each agent appends its items to `osint/evidence-index.yaml` upon completion.

### §3.3 Adversarial Agent Dispatch

The adversarial agent operates in one of two modes, configured in `evidence-collection-config.md`:

**Counter-framing mode:**

The adversarial agent receives inverted search framing derived from the OD objectives:
- For **hypothesis-driven** sessions: hypothesis inversion — search for evidence that the hypothesis is false or that alternative explanations hold
- For **exploratory** sessions: search for evidence in areas that the session's domain models deliberately exclude or underweight — concepts and perspectives outside the analytical framework's scope

The Governor reviews the counter-framing specification before the adversarial agent is dispatched. The coordinator proposes the framing; the Governor approves or adjusts.

**Cross-verification mode:**

The adversarial agent receives a sample of claims from other agents' collected evidence and independently re-collects evidence to verify or refute those claims. Sample size: minimum 20% of total items or 5 items, whichever is greater.

**Output:** All adversarial items are written to `osint/adversarial/` with `adversarial: true` on every item. In cross-verification mode, the agent also produces a verification report at `osint/adversarial/verification-report.md`.

### §3.4 Pre-fetch Mode Procedure

When the capability test (§2.5) determines that agents cannot perform web searches:

1. **Coordinator searches**: The coordinator executes all search specifications from `evidence-collection-config.md`, saving raw search output verbatim to `osint/raw/`.
2. **No filtering**: The coordinator MUST NOT filter, summarize, or editorialize raw results. Save the complete output of each search.
3. **Agent dispatch with file paths**: Dispatch agents with file paths to the raw results instead of search instructions. Each agent receives paths to the raw files relevant to its domain assignment.
4. **Agents analyze**: Agents read the raw files and produce evidence items following the standard schema (§2.1).

The critical constraint is that the coordinator must not act as a gatekeeper on raw search results. Pre-fetch mode preserves the analytical separation between collection and analysis even when tool access is limited.

### §3.5 Cowork Mode Procedure

In cowork mode, the coordinator adopts each agent's role sequentially:

1. **State the role identity**: "Acting as [DOMAIN-N] collection agent..."
2. **Execute the search specification**: Perform searches per the domain's search guidance
3. **Produce evidence items**: Write items to the appropriate `osint/[category]/` directory
4. **Explicit transition**: "Transitioning from [DOMAIN-N] agent to [DOMAIN-M] agent..."

**Execution order:**
- Domain agents first, in domain model order
- Discovery agent second-to-last
- Adversarial agent last — this is mandatory because in cowork mode, the adversarial role sees all prior collection output. Running it last means the counter-framing compensates for the information bleed inherent in sequential role-play.

Record the execution mode at the top of `osint/evidence-index.yaml`:

```yaml
execution_mode: cowork-sequential
roles_executed:
  - { role: "[DOMAIN-1] agent", items_collected: N }
  - { role: "[DOMAIN-2] agent", items_collected: N }
  - { role: "discovery agent", items_collected: N }
  - { role: "adversarial agent", items_collected: N }
```

---

## §4 Open-Ended Discovery

### §4.1 Discovery Searches

The discovery agent executes broad queries designed to surface unknown unknowns — evidence that falls outside the session's predefined domain structure.

Discovery queries are derived from:
- The target name(s) and assessment scope from `evidence-collection-config.md`
- The OD's stated objectives and constraints
- Gaps between domain model coverage and the target's likely information landscape

Discovery queries are NOT hardcoded in this protocol. They are session-specific and generated during bootstrap Step 5c (concept-to-query mapping, §7).

### §4.2 Unclassified Evidence Processing

Evidence items that do not fit any existing domain are tagged:

```yaml
category: "UNCLASSIFIED"
category_guess: "[best-fit domain or new category name]"
```

The discovery agent assigns `category_guess` based on its judgment. These items are written to `osint/discovery/`.

### §4.3 Clustering and Escalation

After discovery collection completes, the coordinator clusters unclassified items by `category_guess`:

1. **Group** items sharing the same or similar `category_guess` values
2. **Count** items per cluster
3. **Apply escalation thresholds**:
   - 3+ items in one cluster → escalate to Governor
   - Any single Tier 1 item that does not fit existing domains → escalate to Governor
   - Items with `contradicts` references to classified items → escalate regardless of count

### §4.4 Governor Resolution

For each escalated cluster, the Governor selects one of four options:

| Option | Action |
|---|---|
| **Create ad-hoc domain** | Build a minimum viable domain model per §13.6, assign items to it |
| **Absorb into closest domain** | Re-tag items to the closest existing domain, update domain model if needed |
| **Out of scope** | Items noted but excluded from assessment, documented in manifest |
| **Defer** | Items preserved for potential future use, not included in current assessment |

### §4.5 Ad-hoc Domain Creation

When the Governor selects "Create ad-hoc domain," the coordinator builds a minimum viable domain model per §13.6:

- Domain name and scope boundary
- Core concepts (minimum 3)
- Relationship to existing domains
- Source attribution mapping

The ad-hoc domain is stored in the session's `domain-models/` directory and added to the evidence manifest's domain list.

---

## §5 Storage Architecture

### §5.1 File Structure

The `osint/` directory is generated from the session's domain models plus fixed directories:

```
osint/
  capability-test.md              # §2.5 execution environment record
  evidence-index.yaml             # §5.2 master index
  evidence-manifest.md            # §6 generated manifest
  [domain-1]/                     # from domain model
    OSINT-001.md
    OSINT-002.md
  [domain-2]/                     # from domain model
    OSINT-003.md
  discovery/                      # fixed: open-ended discovery items
    OSINT-010.md
  adversarial/                    # fixed: adversarial agent items
    OSINT-020.md
    verification-report.md        # cross-verification mode only
  raw/                            # fixed: pre-fetch mode raw search output
```

Directory names under `osint/` are derived from domain model names at bootstrap. Use lowercase, hyphenated names.

### §5.2 Evidence Index

`osint/evidence-index.yaml` is the master index of all collected evidence items:

```yaml
execution_mode: "[normal | pre-fetch | cowork-sequential]"
collection_date: "[YYYY-MM-DD]"
target: "[TARGET]"
total_items: N
items:
  - id: OSINT-001
    source: "[source name]"
    tier: 1
    category: "[thematic category]"
    domain_tags: ["[DOMAIN-1]"]
    level: "target-level"
    target: "[TARGET]"
    adversarial: false
    path: "osint/[domain-1]/OSINT-001.md"
  # ... all items
```

Agents append to this index as they complete collection. The coordinator validates the index for completeness after all agents finish.

### §5.3 Pool-Agent Store Build

When the total evidence item count exceeds 50, build a vector store after collection completes:

```bash
python3 cowork/tools/pool-agent.py build \
  --pool osint/evidence-index.yaml \
  --articles ./osint/ \
  --store ./osint/pool-store/
```

This is a **build-time** decision based on total item count across all domains. The store enables semantic retrieval for domains where direct loading would be excessive. The per-domain **consumption** decision — whether a given agent uses direct file loading or pool-agent retrieval — is made at dispatch time (§6.4).

Score thresholds for pool-agent retrieval:
- **>=0.58**: Read full evidence item
- **0.50–0.57**: Read excerpt (summary from front matter only)
- **<0.50**: Ignore

---

## §6 Evidence Manifest Generation

### §6.1 Purpose

The evidence manifest is the primary interface between evidence collection and assessment. Assessment agents discover evidence through the manifest — they do not browse `osint/` directories directly.

The manifest is generated **after** collection completes and **before** assessment begins.

### §6.2 Format

At Tier 0, the manifest is a markdown document at `osint/evidence-manifest.md`. Required sections per §14.8 manifest schema:

```markdown
# Evidence Manifest — [TARGET]
Collection date: [YYYY-MM-DD]
Execution mode: [normal | pre-fetch | cowork-sequential]
Total items: [N]

## Domain-Tagged Evidence
### [DOMAIN-1]
| ID | Title | Tier | Level | Summary |
|---|---|---|---|---|
| OSINT-001 | ... | 1 | strategic | ... |

### [DOMAIN-2]
...

## Cross-Domain Evidence
Items tagged with multiple domains, listed once with all domain tags shown.

## Uncategorized Evidence
Items that remain UNCLASSIFIED after Governor resolution (§4.4 "Defer" or "Out of scope").

## Escalated Clusters
Discovery clusters escalated to Governor, with resolution decisions.

## Evidence Gaps
Domains with fewer than minimum threshold items (§8). Annotated with [THIN-EVIDENCE] where applicable.

## Contradictions
All detected contradictions (§9), with classification and item cross-references.

## Metric Index
Flat lookup table of all quantitative metrics extracted from evidence items (§10.6).
```

### §6.3 Agent Usage

Assessment agents consume the manifest as follows:

1. **Full manifest** provided to all assessment agents at dispatch — the manifest is a metadata lookup table (IDs, titles, tiers, summaries), not full evidence text. It is the discovery interface, not the evidence itself.
2. **Domain-scoped reading** — each agent reads only the full evidence items tagged to its assigned domain(s). Agents MUST NOT bulk-load evidence items from other domains. This bounds per-agent evidence context to the items relevant to its analytical lens.
3. **Concept-driven queries** (§7) used to find additional relevant items across domains — this is the only mechanism for accessing evidence outside the agent's assigned domain. Queries return targeted results, not bulk content.
4. **Contradictions section** checked — agents MUST address flagged contradictions in their assessments

The orchestrator determines each agent's evidence loading strategy at dispatch time per §6.4. Agents do not self-select their loading approach.

### §6.4 Pre-Dispatch Content Estimation

Before dispatching any agent that will consume evidence (assessment agents, deliberation domain agents, deliverable drafting agents), the orchestrator performs a content estimation step.

**Procedure:**

1. Read the evidence manifest's domain section for the agent's assigned domain(s).
2. Count total items: domain-tagged items + discovery items tagged to this domain + adversarial items tagged to this domain.
3. Select loading strategy based on the per-domain threshold (configured in `evidence-collection-config.md`, default: 30 items):

| Domain Item Count | Pool Store Exists (§5.3) | Loading Strategy |
|---|---|---|
| ≤ threshold | — | **Direct load.** Include evidence file paths in the dispatch prompt. Agent reads the files. |
| > threshold | Yes | **Pool-agent retrieval.** Include pool store path and the domain's concept-to-query mappings (§7) in the dispatch prompt. Agent queries for relevant items. |
| > threshold | No | **Build then retrieve.** Orchestrator builds the pool store (§5.3) first, then dispatches with pool-agent retrieval strategy. |

4. Record the dispatch strategy in the evidence manifest by appending a Dispatch Strategy section (or updating it if already present):

```markdown
## Dispatch Strategy
| Domain | Items | Threshold | Strategy | Notes |
|---|---|---|---|---|
| [DOMAIN-1] | 18 | 30 | direct load | — |
| [DOMAIN-2] | 42 | 30 | pool-agent retrieval | store built at §5.3 |
```

This section is appended after all quality gates pass and before the first assessment agent is dispatched. It is a permanent record — the Governor can review which domains used which strategy.

**Threshold rationale:** At ~1,200 characters per evidence item average, 30 items ≈ 36K characters ≈ 9K tokens of evidence content. Combined with the domain model (~3K tokens), OD excerpt (~3K tokens), and protocol instructions (~3K tokens), this keeps per-agent starting context under ~20K tokens — well within the working range of current models. The Governor may adjust the threshold based on the models being used or the expected item size for the session.

---

## §7 Concept-to-Query Mapping

### §7.1 Generation

Concept-to-query mappings are auto-generated from domain model core concepts during bootstrap Step 5c. The coordinator produces a mapping table that translates abstract domain concepts into concrete evidence search queries.

### §7.2 Format

```markdown
# Concept-to-Query Mapping — [TARGET]

| Domain | Core Concept | Evidence Queries |
|---|---|---|
| [DOMAIN-1] | [concept-1a] | "[query 1]", "[query 2]" |
| [DOMAIN-1] | [concept-1b] | "[query 3]" |
| [DOMAIN-2] | [concept-2a] | "[query 4]", "[query 5]" |
```

### §7.3 Constraints

- Queries are **session-specific** — they depend on the target, scope, and domain models
- This protocol does NOT provide hardcoded queries
- The mapping is stored in `evidence-collection-config.md` and referenced during collection agent dispatch and manifest generation
- Discovery queries (§4.1) are derived from gaps in this mapping

---

## §8 Gap Analysis

### §8.1 Sufficiency Assessment

After collection completes, the coordinator assesses evidence sufficiency per domain:

1. Count items per domain, grouped by tier
2. Compare against minimum thresholds from `evidence-collection-config.md`
3. Identify domains below minimum

### §8.2 Minimum Thresholds

Defaults (overridable in config):

| Metric | Default Minimum |
|---|---|
| Tier 1 or Tier 2 items per domain | 3 |
| Total items per domain | 5 |
| Domains with zero items | 0 (every domain must have at least 1 item) |

Thresholds apply at the target level — for multi-target sessions, each target is assessed independently.

### §8.3 Targeted Follow-up

For domains below minimum thresholds:

1. Generate additional search queries from the concept-to-query mapping (§7)
2. Dispatch a follow-up collection agent (or perform follow-up searches in cowork mode)
3. Re-assess sufficiency after follow-up

One round of follow-up is the default. Additional rounds require Governor approval.

### §8.4 Thin Evidence Annotation

If a domain remains below minimum thresholds after follow-up:

- Annotate the domain in the evidence manifest with `[THIN-EVIDENCE]`
- Record the gap in the manifest's Evidence Gaps section
- Assessment agents receiving `[THIN-EVIDENCE]` domains MUST acknowledge the limitation in their output and reduce confidence in affected conclusions

---

## §9 Contradiction Handling

### §9.1 Detection

Contradictions are detected at two points:

1. **During collection**: Agents flag contradictions by populating the `contradicts` field when they encounter items that conflict with previously collected evidence
2. **During manifest generation**: The coordinator cross-references items within and across domains to identify contradictions that individual agents may have missed

### §9.2 Classification

| Type | Description | Example |
|---|---|---|
| **Factual** | Items report different facts about the same claim | Two sources report different numeric values for the same metric |
| **Interpretive** | Items agree on facts but draw opposing conclusions | Same data, different assessments of significance |
| **Temporal** | Items were accurate at different times; newer supersedes older | A 2023 report contradicted by a 2025 update |

### §9.3 Documentation

All contradictions are documented in the manifest's Contradictions section:

```markdown
## Contradictions

### C-001: [descriptive title]
- Items: OSINT-[NNN] vs OSINT-[MMM]
- Type: [factual | interpretive | temporal]
- Summary: [brief description of the contradiction]
- Domains affected: [DOMAIN-1], [DOMAIN-2]
```

### §9.4 Assessment Obligation

Assessment agents MUST address flagged contradictions. Ignoring a documented contradiction triggers a `[SELECTIVE-CITATION]` flag during evidence engagement audit (§10.7).

---

## §10 Quality Gates

### §10.0 Pre-Flight Retrieval Contract Validation (from GOSTA §8.7 V1) `[CORE]`

This gate runs **before** evidence collection begins, at the phase boundary that authorizes per-unit retrieval at scale. It exists because the post-collection gates §10.1–§10.8 cannot rescue a session whose retrieval contract was never validated against its operational query set — by the time those gates run, the corrupt or absent evidence is already in the corpus.

**Procedure.** For each per-unit retrieval contract the phase declares (per-feature, per-vendor, per-candidate, per-regulation, per-hypothesis, per-domain), run at least one query derived from the actual unit name OR the unit's concept-vocabulary translation against each declared pool. Tabulate outcomes per `(unit, pool)` cell:

- **VALIDATED** — retrieval clears the configured score floor.
- **CORPUS-FIT-GAP** — retrieval below floor; corpus content (verified by source-text grep) does not meaningfully cover the unit's concept. Documented; logged for §14.8 information_gap classification; does not block the gate but reduces evidence-base coverage.
- **VOCABULARY-MISMATCH** — retrieval below floor; corpus content covers the concept under different vocabulary. Per-unit query-engineering pass with concept-vocabulary translation; documented but does not block.
- **ESCALATE** — retrieval below floor; coverage diagnostic ambiguous (corpus presence/absence unclear). Escalate to Governor with three mitigation paths (threshold lowering / source extraction redo / embedding model upgrade) before the gate can pass.

**Gate behavior.** **BLOCK** if any cell is unresolved ESCALATE. **WARN** if CORPUS-FIT-GAP or VOCABULARY-MISMATCH cells exist without explicit Governor disposition. PASS if all cells are VALIDATED or have explicit dispositions logged.

**Pre-launch probe queries are not §10.0-compliant.** Pre-launch verification that uses topic-vocabulary probe queries (e.g., "third-party risk management," "incident response") instead of the actual operational queries (per-unit names or concept-vocabulary translations) does not exercise the retrieval contract. The gate must run the queries the phase will actually execute, not proxies for them. (This is the V1 operationalization of §8.7.2's test-what-runs principle.)

**Relationship to §10.2 Source Verification.** §10.2 verifies that cited sources exist and contain what evidence items claim. §10.0 verifies that the retrieval mechanism can find relevant sources for the phase's operational query set in the first place. §10.0 runs first; §10.2 cannot compensate for §10.0 failures because §10.2 only operates on items already in the corpus.

### §10.1 Execution Order

Quality gates execute in this order. §10.0 runs before collection; §10.2–§10.8 run after collection and before assessment:

0. **Pre-Flight Retrieval Contract Validation** (§10.0) — runs at phase entry, before collection
1. **Source Verification** (§10.2)
2. **Evidence Quality Audit** (§10.3)
3. **Adversarial Collection Review** (§10.4)
4. **§14.3.11 Verification** (§10.5)
5. **Metric Index construction** (§10.6)
6. **Evidence Manifest Generation** (§6)
7. **Evidence Engagement** audit configuration (§10.7) — audit itself runs during/after assessment
8. **Evidence-Domain Model Reconciliation** (§10.8)

Collection does not begin until §10.0 passes. Assessment does not begin until §10.1–§10.8 all pass or the Governor acknowledges and accepts warnings.

### §10.2 Source Verification

**Purpose:** Verify that cited sources exist and contain what the evidence item claims.

**Procedure:** For sampled evidence items, re-fetch the source URL and confirm the content supports the item's summary and claims.

**Sample rates** (configurable in `evidence-collection-config.md`):

| Tier | Default Sample Rate |
|---|---|
| 1 | 100% |
| 2 | 30% |
| 3 | 0% (not verified by default — low expected reliability) |

**Three outcomes per item:**

| Outcome | Action |
|---|---|
| **Verified** | Source confirmed, no action needed |
| **Access-restricted** | Source exists but behind paywall/login — escalate to Governor, do NOT auto-downgrade tier |
| **Unverifiable** | Source not found or content does not match — escalate to Governor with recommendation |

At Tier 0, the coordinator re-runs search queries to verify sources. This gate depends on web search availability — in pre-fetch mode, verification uses the saved raw output.

### §10.3 Evidence Quality Audit

Operates in one of two modes, set in `evidence-collection-config.md`:

**Directional mode:** Assess the ratio of supporting, contradicting, and neutral evidence relative to the session's hypotheses or objectives.

```
supporting_ratio = supporting_items / total_items
contradicting_ratio = contradicting_items / total_items
neutral_ratio = neutral_items / total_items
```

**Coverage mode:** Map evidence items to domain model core concepts and assess coverage completeness.

```
coverage = concepts_with_evidence / total_concepts
```

**Four outcomes:**

| Outcome | Directional Criteria (default) | Coverage Criteria (default) |
|---|---|---|
| **PASS** | supporting_ratio <= 0.70 | coverage >= 0.80 |
| **WARNING** | supporting_ratio 0.71–0.80 | coverage 0.60–0.79 |
| **FAIL** | supporting_ratio > 0.80 | coverage < 0.60 |
| **SCARCITY-ACKNOWLEDGED** | Coverage mode only: evidence sparse due to genuine unavailability, not collection failure | Coverage mode only: Governor acknowledges scarcity |

Thresholds are configurable. Coverage mode additionally requires a **concept-to-evidence mapping table** for reproducibility — this table documents which evidence items map to which core concepts.

### §10.4 Adversarial Collection Review

This gate verifies that the adversarial agent (§3.3) produced meaningful output:

**Counter-framing mode check:**
- Did the adversarial agent find counter-evidence? (minimum 1 item)
- Are counter-evidence items substantive (Tier 1 or 2)?
- If no counter-evidence found, did the agent document the search effort?

**Cross-verification mode check:**
- Did the verification report cover the required sample size?
- What percentage of sampled claims were verified vs. refuted vs. inconclusive?
- Are refuted claims flagged in the evidence index?

Failure of this gate requires Governor review — either additional adversarial collection or documented acceptance.

### §10.5 §14.3.11 Integration

§14.3.11 of the spec defines eight verification checks. At Tier 0, the coordinator performs these as cognitive discipline during quality gate execution.

**Pre-deliberation checks (run during §10.1–§10.4):**

| Check | Description |
|---|---|
| 1. Tier Re-classification | Review tier assignments for accuracy |
| 2. Specificity Audit | Flag items with vague claims lacking concrete evidence |
| 3. Negative Claim Audit | Verify that "no evidence of X" claims reflect genuine search, not search gaps |
| 4. Range Suppression Audit | Check that numeric ranges are preserved, not collapsed to single values |

**In-deliberation checks (run during assessment, enforced via §10.7):**

| Check | Description |
|---|---|
| 5. Phantom Citation | Flag citations to evidence items that do not exist in the index |
| 6. Tier Escalation | Flag claims where a Tier 3/4 source is treated as Tier 1/2 authority |
| 7. Selective Citation | Flag assessments that cite supporting evidence while ignoring contradicting evidence on the same topic |
| 8. Parametric Claim Audit | Cross-reference quantitative claims against the Metric Index (§10.6) |

**Annotation taxonomy from §14.3.11:**

- `[TIER-DISPUTED: collector=N, verifier=M]` — tier assignment differs between collector and verifier (Check 1)
- `[UNVERIFIED-NUMBER]` — numeric claim doesn't match cited source (Check 2)
- `[UNVERIFIED-ABSENCE]` — absence claim asserts beyond search scope (Check 3)
- `[SINGLE-SOURCE-ESTIMATE]` — range suppressed to single value (Check 4)
- `[PHANTOM-EVIDENCE]` — citation references non-existent evidence item (Check 5)
- `[TIER-MISMATCH: item=OSINT-NNN, verified-tier=N, used-as=sole-basis]` — source authority overstated in citation (Check 6)
- `[SELECTIVE-CITATION: contradiction=OSINT-NNN vs OSINT-MMM]` — contradicting evidence ignored (Check 7)
- `[UNCITED-MATCH: OSINT-NNN]` — parametric claim matches evidence but lacks citation (Check 8)
- `[PARAMETRIC-STALE: agent-value=X, evidence-value=Y, evidence-ref=OSINT-NNN]` — agent used training data instead of collected evidence (Check 8)
- `[PARAMETRIC-UNVERIFIED]` — parametric claim has no evidence equivalent (Check 8)
- `[TRAINING-DATA-ESTIMATE]` — claim explicitly marked as from training data (Check 8, self-applied or forced)

### §10.6 Metric Index

**Purpose:** Enable Check 8 (Parametric Claim Audit) by providing a flat lookup table of all quantitative metrics in the evidence corpus.

**Build procedure:**

1. Scan all evidence items for quantitative claims (numbers, percentages, ranges, dates, monetary values)
2. Extract each metric with its source item ID, context, and exact value
3. Compile into a flat table

```markdown
## Metric Index

| Metric | Value | Source | Context |
|---|---|---|---|
| [metric name] | [exact value or range] | OSINT-[NNN] | [brief context] |
```

The Metric Index is included in the evidence manifest (§6.2) and used during assessment to verify that quantitative claims in assessments match their evidence sources.

### §10.7 Evidence Engagement

Evidence engagement auditing ensures that assessment outputs are grounded in the collected evidence. This gate is **mode-independent** — it applies whether the session uses deliberation or single-agent assessment.

#### Path 1: With Deliberation

When the session uses the deliberation protocol:

1. **Engagement instruction** is included in the agent dispatch prompt for all deliberation agents
2. **Per-round engagement audit** is performed by the coordinator after each deliberation round
3. **Three citation categories** are enforced:
   - `OSINT-[NNN]` — reference to a collected evidence item
   - `[reference-pool: SOURCE-ID]` — reference to a pool-agent source
   - `[training-knowledge]` — claim based on model training data (must be explicitly labeled)
4. **Evidence-grounding linkage**: Any assessment claim not linked to at least one evidence item receives the `[UNLINKED-EVIDENCE]` flag
5. Results documented in `deliberation/evidence-engagement-audit.md`
6. **§14.3 extensions apply in full**: §14.3.2 (evidence-claim linkage), §14.3.3 (evidence_basis tracking), §14.3.5 (synthesis verification), §14.3.10 (propagation tracking)

#### Path 2: Without Deliberation

When the session uses single-agent assessment without deliberation:

1. **Engagement instruction** is included in the single assessment agent's prompt
2. **Post-assessment audit** is performed by the coordinator after the assessment completes
3. Same three citation categories as Path 1
4. Same `[UNLINKED-EVIDENCE]` flagging
5. Results documented in `osint/evidence-engagement-audit.md`
6. **§14.3 extensions apply partially**: §14.3.2 (evidence-claim linkage) and §14.3.3 (evidence_basis tracking) apply. §14.3.5 (synthesis verification) and §14.3.10 (propagation tracking) do NOT apply — these require multi-agent interaction.

#### Engagement Thresholds

| Uncited Assessment Claims | Outcome |
|---|---|
| <=10% | PASS |
| 11–25% | WARNING — Governor review required |
| >25% | FAIL — assessment revision required |

### §10.8 Evidence-Domain Model Reconciliation

After quality gates and before assessment begins, the coordinator reviews collected evidence against the domain model's core concepts to identify mismatches.

**Procedure:**

1. For each domain, compare evidence items against the domain's core concepts
2. Identify concepts with no supporting evidence
3. Identify evidence that contradicts core concept definitions
4. Classify contradictions:

| Classification | Description | Action |
|---|---|---|
| **Minor adjustment** | Evidence refines but does not invalidate a concept | Coordinator updates concept description, documents change |
| **Concept invalidation** | Evidence fundamentally contradicts a core concept | Governor decision required |

5. Governor resolves invalidations before assessment begins

Assessment does not begin until reconciliation is complete and all invalidations are resolved.

---

## §11 Verification Reference

### §11.1 Spec Cross-Reference

The eight verification checks in §10.5 derive from §14.3.11 of the spec. This section serves as a quick reference — consult the spec for authoritative definitions.

### §11.2 Tier 0 Execution

At Tier 0, the coordinator performs all eight checks as cognitive discipline:

- **Checks 1–4** (pre-deliberation): Performed during quality gate execution (§10.1 steps 1–4)
- **Checks 5–8** (in-deliberation): Enforced through the evidence engagement audit (§10.7)

The coordinator documents verification results in a verification report appended to the evidence manifest:

```markdown
## Verification Report

### Pre-Assessment Checks
- Tier Re-classification: [N items reclassified, details]
- Specificity Audit: [N items flagged, details]
- Negative Claim Audit: [N items flagged, details]
- Range Suppression Audit: [N items flagged, details]

### Assessment Checks (post-assessment)
- Phantom Citation: [N instances]
- Tier Escalation: [N instances]
- Selective Citation: [N instances]
- Parametric Claim Audit: [N discrepancies]
```

---

## §12 Evidence Archive

### §12.1 Post-Session Promotion

After session completion, the Governor selects evidence items to promote to the framework-level archive. Promotion criteria:

- Items with lasting reference value beyond the current session
- High-tier items (Tier 1 or 2 preferred)
- Items that establish baseline facts likely relevant to future sessions

### §12.2 Archive Location

Archived evidence is stored at:

```
cowork/evidence-archive/[target]/
  [OSINT-NNN].md          # archived evidence items
  archive-manifest.yaml    # index of archived items with metadata
```

### §12.3 Aging

Each archived item receives an `effective_until` field computed from domain-specific defaults defined in §14.8:

```yaml
effective_until: "[YYYY-MM-DD]"
aging_basis: "[domain-specific rationale]"
```

Items past their `effective_until` date are flagged for re-verification in any future session that imports them.

### §12.4 Import

Future sessions query the evidence archive during bootstrap Step 5b:

1. Check `cowork/evidence-archive/` for items matching the new session's target(s)
2. Import matching items as **copies** into the new session's `osint/` directory
3. Flag all imported items with `imported: true` and `import_source: "[original session]"`
4. Imported items are flagged for **re-verification** — they must pass source verification (§10.2) before being treated as current evidence

Imported items retain their original tier but may be reclassified during re-verification.

---

## §13 Collection Execution Checklist

This checklist covers the complete evidence collection lifecycle. The coordinator tracks completion of each step.

### Phase 1: Setup
- [ ] Evidence collection enabled by Governor (bootstrap Group 3B)
- [ ] `evidence-collection-config.md` populated with targets, search specs, thresholds
- [ ] Concept-to-query mapping generated (§7)
- [ ] `osint/` directory structure created from domain models (§5.1)
- [ ] Capability test executed, result recorded (§2.5)
- [ ] Evidence archive checked for importable items (§12.4)

### Phase 2: Collection
- [ ] Domain collection agents dispatched (§3.1)
- [ ] All domain agents completed, items indexed (§3.2)
- [ ] Discovery agent dispatched and completed (§4)
- [ ] Unclassified items clustered and escalated (§4.3)
- [ ] Governor resolved all escalated clusters (§4.4)
- [ ] Adversarial agent framing approved by Governor (§3.3)
- [ ] Adversarial agent dispatched and completed (§3.3)

### Phase 3: Quality Gates
- [ ] Source verification completed (§10.2)
- [ ] Evidence quality audit completed — outcome: [PASS/WARNING/FAIL/SCARCITY] (§10.3)
- [ ] Adversarial collection reviewed (§10.4)
- [ ] Pre-deliberation verification checks completed (§10.5, Checks 1–4)
- [ ] Metric Index built (§10.6)

### Phase 4: Manifest and Reconciliation
- [ ] Evidence manifest generated (§6)
- [ ] Gap analysis completed (§8)
- [ ] Follow-up collection executed if needed (§8.3)
- [ ] `[THIN-EVIDENCE]` annotations applied where applicable (§8.4)
- [ ] Contradiction documentation complete (§9)
- [ ] Evidence-domain model reconciliation completed (§10.8)
- [ ] Governor approved reconciliation outcomes
- [ ] Evidence engagement audit configured for assessment phase (§10.7)
- [ ] Pre-dispatch content estimation completed — per-domain loading strategies recorded in manifest (§6.4)

### Phase 5: Post-Assessment
- [ ] In-deliberation verification checks completed (§10.5, Checks 5–8)
- [ ] Evidence engagement audit completed — outcome: [PASS/WARNING/FAIL] (§10.7)
- [ ] Verification report appended to manifest (§11)

### Phase 6: Archive
- [ ] Governor selected items for archive promotion (§12.1)
- [ ] Promoted items copied to `cowork/evidence-archive/[target]/` (§12.2)
- [ ] `effective_until` dates assigned (§12.3)

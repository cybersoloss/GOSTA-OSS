# GOSTA Protocol Ecosystem Assessment Prompt

Use this prompt when you want an AI session to evaluate whether the full protocol ecosystem (`cowork/` set + companion protocols) is fit for purpose.

**Current protocol ecosystem:**
- Cowork Protocol
- Deliberation Protocol
- OD Drafting Protocol
- Sync-Manifest (framework-to-protocol dependency tracker)
- Templates (operating-document, session-status, deliberation-status, health-report, signal-entry, session-log, domain-model, learnings, scope-definition, bootstrap)
- CLAUDE.md (Code-mode startup instructions)
- startup.md (session launcher startup sequence)

---

## The Prompt

Read the full contents of `cowork/` — all protocols, CLAUDE.md, startup.md, and every template. Then read the latest GOSTA framework spec (highest version number at repo root). Also read the sync-manifest cover to cover. Perform this assessment across nine dimensions:

**1. External Consistency — Protocols vs GOSTA Framework**

For every CORE-tier mechanism in the GOSTA spec, state whether the protocol ecosystem implements it, partially implements it, or omits it. Use a table:

| GOSTA Mechanism | Spec Section | Protocol Section | Status | Gap Description |
|---|---|---|---|---|
| [name] | [§X.Y] | [protocol:§X.Y or MISSING] | covered / partial / missing | [what's missing or misaligned] |

Check specifically: five-layer hierarchy, guardrails (hard/soft/spirit/calibration/analytical), signal types and attribution (including Action Completion Gate), health computation (tactic/strategy/goal), kill/pivot logic, graduation stages, domain model requirements (including quality gate with severity gradation), structural integrity rules (C1-C4, R1-R4, V1-V9), feedback loops, scope types (finite + ongoing), review cadences, phase gate enforcement (including Signal Coverage field, Pre-Flight Validation Gate Results field), autonomy safeguards (degraded-mode, reversibility, magnitude thresholds, conditional grants), failure resilience (signal pipeline, recovery verification, context integrity, capacity degradation, Governor decision validation), environmental watch list, execution cost tracking, semantic coherence validation, decision-to-state traceability, OD state versioning, interface contracts (§8.6), pre-flight validation gates (§8.7 — retrieval contract V1, build artifact shape V2 with `pool-agent verify-store` LFS-pointer pre-check, decision spine V3, continuous capture V4, runtime imports V5, declared artifact existence and population V6, vertical-fit on inherited artifacts V7, subagent-dispatch capability smoke-test V8 [conditional], inheritance framework-residue audit V9 [conditional]), finding classification (§14.3.8), sycophancy detection (§14.3.9 — health report risk factors, signal-recommendation consistency, kill proximity alerting, deliberation convergence probes, signal integrity checks), Analytical Frame Contract (§9.2 — AFC derivation, Dispatch Preamble AFC injection §7.5, Frame Integrity Validation §12.12 [including Verdict Strength Annotation propagation with conditional `[VERDICT-SPLIT-CARRIED]` field, Classification-against-reference reporting discipline, Evidence Channel Disclosure, scope extension to synthesis-report.md and phase-gate-*.md per Plan #19 — M4 hook covers deliverables/ + deliberation/[DELIB-NNN]/synthesis-report.md + health-reports/phase-gate-*.md], F-16 fidelity checkpoint, domain model frame audit, Goal Correction Procedure), Coverage Limitation Disclosure at deliverable production (§12.15, derived from spec §14.8 four-outcome model — coverage-mode WARN escalation rule + "Known Coverage Limitations" section requirement when sub-threshold coverage outcomes occurred), Deliberation Protocol §3.3 verdict-split-aware termination (termination permitted only when no intra-cluster verdict-band splits exceeding the session's declared convergence threshold remain open; if open, targeted re-dispatch OR Governor override with `[VERDICT-SPLIT-CARRIED]` annotation), and cross-boundary claim propagation (§14.3.10).

**2. Internal Consistency — Each Protocol vs Its Own Templates**

For each template in `cowork/templates/`:
- Verify every field traces to a protocol section that defines it.
- Verify every protocol section that requires a file format has a corresponding template.
- Flag any version number mismatches across files (protocol headers, CLAUDE.md, template headers, framework version references, sync-manifest header).
- Flag any section cross-references within protocols that point to non-existent sections (e.g., "see §X" where §X doesn't exist).
- Check that the OD template's Deliberation section references the current Deliberation Protocol version.
- Check that the OD template's Roster Rules match the Deliberation Protocol's current agent count guidance (tiered: 5-7 recommended, 8-10 viable, >10 cluster).

**3. Cross-Protocol Consistency — Protocols vs Each Other**

Three protocols now form an ecosystem. Check their interactions:
- **Cowork ↔ Deliberation:** Does the cowork protocol's escalation model (§7.5) correctly describe what the deliberation protocol implements? Do shared concepts (signals, phase gates, session lifecycle) use the same definitions? Does health computation (§7.1-7.3) apply epistemic classification (confirmed/information_gap/conditional) consistently with deliberation finding classification (Deliberation Protocol §4.4)?
- **Cowork ↔ OD Drafting:** Does the OD Drafting Protocol's output conform to the cowork protocol's OD format (§4)? Does the quality gate in OD Drafting (§6) match the quality gate in cowork (§5.2)?
- **Deliberation ↔ OD Drafting:** Does the OD Drafting Protocol correctly reference the deliberation protocol's agent topology (§2) and cadence parameters (§2.1)?
- **Sync-Manifest completeness:** Are all derivation chains tracked? Grep each protocol for references to the framework ("§", "GOSTA", "Framework") and verify each reference has a manifest entry. Flag untracked derivations.

**4. Reusability — Can a New Session Bootstrap from This?**

Walk through the new-session bootstrap process step by step:
- Copy `cowork/` into a new session directory.
- Follow CLAUDE.md's "Starting a New Session" instructions.
- If using the OD Drafting Protocol: walk through the Governor Commission → Decomposition → Draft OD → Governor Review → Quality Gate → Handoff flow.
- Create each required file using the templates.
- Identify every point where the user must make a decision the templates don't guide, where a template references something that doesn't exist yet, or where the sequence of steps is ambiguous.

Test against four scenarios: (a) a finite analytical scope like a product roadmap, (b) an ongoing operational scope like content marketing, (c) a scope requiring domain models not included in the repo, (d) a scope using OD Drafting Protocol with 5+ domain agents and deliberation enabled.

**5. Dual-Mode Parity — Cowork vs Claude Code**

For each protocol mechanism, state whether it works identically in both modes or has a mode-specific gap. Check specifically:
- Session start automation (CLAUDE.md covers Code — what covers Cowork?)
- File operations (who reads/writes in each mode?)
- Multi-domain assessment at Level 3 (agent isolation — structural in Code via subagents, behavioral in Cowork via role-switching protocol)
- OD Drafting Protocol (decomposition proposals — parallel in Code, sequential in Cowork)
- Dependency validation (automated in Code, manual in Cowork — is the manual process specified?)
- State recovery after failure (Code has file persistence, Cowork has conversation — is both covered?)
- Git operations (Code-specific — does Cowork have an equivalent state-safety mechanism?)
- Signal emission gate (Action Completion Gate — how enforced in each mode?)
- Deliberation round completion gate — how enforced in each mode?

**6. Self-Improvement Loop**

Trace the full cycle: session runs → discovers framework feedback → feedback accumulates → protocol update triggered → updated protocol available for next session. Identify every point where this loop requires manual intervention, has no trigger defined, or has no propagation mechanism. Classify each as: structural (protocol can't express it), procedural (protocol says to but doesn't enforce), or missing (not mentioned).

Also check: does the protocol's version check mechanism actually work? Can the AI detect version drift? What happens when the GOSTA framework updates but the protocols don't? Does the sync-manifest's Verification Protocol actually get followed? Is the OD Drafting Protocol's ingestion phase (§2) sufficient to catch version drift?

**7. Reverse Findings — GOSTA Framework Improvement Recommendations**

The assessment treats the GOSTA spec as ground truth. But running the protocol assessment naturally surfaces framework-level issues — ambiguities, missing tier differentiation, or structural gaps that the protocols can't work around. Capture them here.

For each finding, classify as:
- **Ambiguity** — the spec says something that can be interpreted multiple ways, and the protocol had to pick one without clear guidance.
- **Missing Tier Differentiation** — the spec requires something at a single level of rigor that should vary by tier (e.g., a field required at Tier 0 that only makes sense at Tier 2+).
- **Structural Gap** — the spec is silent on something the protocol needs to implement (i.e., the protocol can't conform because the spec doesn't define the mechanism).
- **Protocol-Originated Gap** — a protocol has added a mechanism (e.g., Action Completion Gate, Round Completion Gate, quality gate severity gradation) that should arguably be in the framework but isn't yet.

For each, state: what the framework says (or doesn't say), what the protocol had to do as a result, and a recommended spec change.

**8. OD Construction Quality**

The OD Drafting Protocol (v0.1) is new. Assess specifically:
- Is the Framework Ingestion phase (§2) comprehensive enough? Does the reading sequence cover all sections an OD Architect needs?
- Is the Governor Commission template (§3.1) sufficient for vague inputs?
- Does the Decomposition Phase (§4) produce structurally sound proposals?
- Is the Comprehension Gate (§5.2) sufficient to prevent Governor rubber-stamping?
- Does the handoff (§7) correctly integrate with the cowork protocol's bootstrap flow?
- Are multi-tier considerations (§8) adequate?
- Are the failure mode mitigations (§10) sufficient?

**9. Severity-Ranked Findings**

Consolidate all findings from dimensions 1-8 into a single ranked list:
- **(A) Would cause session failure** — missing mechanism that the framework requires and the session cannot proceed without.
- **(B) Would cause silent degradation** — missing mechanism where the session proceeds but produces worse outputs without anyone noticing.
- **(C) Inconvenience** — friction or ambiguity that slows work but doesn't affect outcomes.

For each finding, recommend a specific fix with estimated effort (line count or complexity). State whether the fix targets the framework, cowork protocol, deliberation protocol, OD drafting protocol, templates, CLAUDE.md, startup.md, or the sync-manifest.

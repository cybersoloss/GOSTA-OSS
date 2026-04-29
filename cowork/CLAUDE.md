# GOSTA Session — Claude Code Directive

When working inside a GOSTA session directory, follow the **GOSTA-Cowork Protocol** (`cowork/gosta-cowork-protocol.md`).

## Session Start (MANDATORY)

Every time you enter a GOSTA session directory:

1. **Read `00-BOOTSTRAP.md`** — this is your orientation. It tells you what phase you're in, what happened last session, and what's pending.
2. **Read files in the Context Loading Order** specified in the bootstrap file.
3. **Check OD staleness** — if 2+ phases or review cycles have passed since the OD was last updated, flag it: "OD may be stale. Last updated [date]. Recommend refreshing before proceeding."
4. **Report status** to the Governor and ask what they want this session.

## Core Rules

- **Never modify the Operating Document without Governor approval.** Draft changes, present them, wait for approval.
- **Signal-first execution** — write a signal stub (`| ACT-ID | in_progress | timestamp |`) to `signals/` BEFORE starting each action. Update to `completed` or `failed` after. An action without a signal stub has not started; an action without a completion update has not finished. See protocol §6.3 Action Completion Gate.
- **Use Phase Gate Enforcement** at every phase transition — produce the structured Phase Gate Request (protocol §5.1) before proceeding.
- **Kill before pivot** when kill conditions are formally met (protocol §7.1). Don't soften kills into pivots without Governor justification.
- **Classify tensions** as Blocking/Material/Informational (protocol §5.1 Step 3b). Only halt on Blocking.
- **Reference pool agent** — if a session's reference pool exceeds 50 items, use `cowork/tools/pool-agent.py query` to retrieve relevant articles. Do NOT load the full pool YAML into context. For large single documents (specs, regulatory texts), use stores built with `index-doc` — results include `section_range` line numbers for targeted reading. Score thresholds: ≥0.58 read full article/section, 0.50–0.57 excerpt only, <0.50 ignore. If the model file is missing (`model.onnx`), alert the Governor and run `setup-model` before proceeding. See protocol §18.5.
- **Log framework feedback** whenever you notice gaps in how GOSTA handles a situation.
- **Guardrails are above baseline** — if you see a guardrail set below the current metric baseline, flag it as a calibration issue.
- **Surface risks explicitly** in every health report — the Risk Factors section (§14.3.9) must be non-empty and substantive. Generic dismissals are themselves a flag.
- **Tournament execution** — when a tactic declares tournament mode (§4.6), generate candidates sequentially with per-candidate signal stubs. In constrained mode, communicate the cell constraint before each generation. Do NOT reference prior candidates during generation — each candidate is structurally independent. After all candidates are generated, evaluate using the configured assessment level and present results with behavior space map to Governor for selection. Emit `tournament_selection` signal after Governor decides. Constrained mode is the Tier 0 default — do not use sampling mode unless the Governor explicitly requests it.
- **Dimension Elicitation** — when drafting a tournament-enabled tactic in the OD, analyze session context (domain model tensions, guardrail pairs, reference pool clusters, deliverable trade-offs) and propose candidate behavior space dimensions to the Governor before declaring the behavior space. Do not invent dimensions without evidence from context sources.
- **Check signal-recommendation alignment** — if most signals trend negative but you recommend persevere, state why with specific countervailing evidence.

## Verification Discipline

Pre-flight validation gates per spec §8.7 are operational requirements at runtime, not advisory checks. The framework declares the structures (artifacts, retrieval contracts, runtime tools, capture-mode flags); this section specifies the assistant-side discipline that keeps those declarations operationally true at every lifecycle boundary.

### Phase-gate verification (mandatory at every phase entry and phase exit)

1. **Declared-artifact existence and population check (V6).** For every artifact named in `00-BOOTSTRAP.md`, the OD §Decision History, or the scope file as a phase deliverable: run two layers of mechanical test. *Layer A — existence:* `test -s <path>`. Empty or missing artifacts BLOCK phase exit unless explicitly deferred with a Governor-acknowledged reason in OD §Decision History. *Layer B — populated-where-templated:* for each artifact whose template carries `[POPULATE: ...]` sentinel markers, run `grep -c "\[POPULATE:" <path>` (must return 0) and verify each formerly-sentineled section meets the per-section word-count floor (default 20 words). Layer B failures BLOCK phase exit identically to Layer A. **At the closeout phase gate, V6 fires explicitly on closeout-mandated artifacts** — `learnings.md`, `session-logs/session-NNN.md`, `gosta-framework-feedback.md`, plus session-specific closeout deliverables. Closeout cannot complete with template-shaped closeout artifacts. The closeout-fidelity gap (artifact non-zero because template scaffolding has content; Layer A passes; Layer B catches the missing population) is the canonical surface for this failure.

2. **Continuous-capture coverage check (V4).** When Debug + Shortfall Reporting Mode (or any continuous-capture mode flag) is active, run `wc -l` against the relevant log artifacts (shortfall log, framework-feedback file, session-log directory) and compare to friction signals observed during the phase. If friction was observed and capture is empty, either backfill entries before phase exit OR explicitly confirm "all friction this phase is session-execution-specific, not framework-class" in writing.

3. **Cross-doc consistency check (V3).** At Phase 1 entry: run a cross-document key-set comparison between OD and scope file (every STR-N appears in both, every guardrail referenced exists, every deliverable maps to a strategy). Symmetric difference must be empty before Phase 1 enters.

4. **Retrieval contract validation (V1).** Before any phase that runs per-unit queries at scale: for at least one representative query per declared pool, run the actual operational query (not a topic-vocabulary probe) and record VALIDATED / CORPUS-FIT-GAP / VOCABULARY-MISMATCH / ESCALATE per cell. Phase entry blocks on unresolved ESCALATE.

### Tool-invocation discipline

5. **First-call-per-session import test (V5).** Before the first invocation of any pool-agent, embedding, or runtime-dependent tool: run `python3 -c "<actual import statements the tool will execute>"` in the orchestrator's runtime. File-presence checks against the model file or dependency list do NOT satisfy V5 — verify what runs, not what is documented to run. V5 covers the orchestrator's environment; capabilities crossing into a subagent sandbox are V8's responsibility (see rule 5a).

5a. **Subagent dispatch capability smoke-test (V8) — conditional on subagent-dispatch declaration.** If the session declares subagent dispatch in scope, the OD, or `00-BOOTSTRAP.md`: at bootstrap, dispatch a probe subagent that (a) writes a marker file at the session directory and (b) runs a no-op call against any declared-for-subagent tool. Independently verify via your own Read tool that the marker file exists at the reported path. V8 fails if the probe reports `permission denied` / `Bash blocked` / sandbox-path-resolution error, or if the no-op tool call raises an environment-specific error not seen in V5, or if your Read does not see the marker file. Three failure classes surface: path-resolution (workspace symlinks not mounted in subagent sandbox), permission-grant scope (orchestrator grants do not propagate), declared-tool callability (tool imports cleanly in orchestrator, not in subagent runtime). On V8 failure, surface to Governor with three mitigation options: reroute-path / extend-sandbox / collapse-to-orchestrator. Sessions without subagent-dispatch declaration skip V8.

5b. **Inheritance framework-residue audit (V9) — conditional on inheritance declaration.** If the session inherits artifacts (domain models, scope decisions, deliberation rosters, templates, reference artifacts) from a prior session or example library: at Phase 1 entry, extract framework-concept tokens from the inheriting session's OD §Framework-Version Markers + scope + CLAUDE.md (word-boundary-anchored regex on structural identifiers `\bOBJ-\d+\b` / `\bSTR-\d+\b` / `\bTAC-\d+\b` / `\bACT-\d+\b` / `\bDEC-PG-\d+\b` / `\bDEC-\d+\b` / `\bDELIB-\d+\b` / `\bG-[A-Za-z]+\b`; framework-version markers from OD §Framework-Version Markers when declared) and from each inherited artifact. Compute set difference: tokens in inherited artifact NOT in inheriting session's declarations. The result is the framework-residue list. V9 is the inverse direction of V7: V7 catches coverage gaps; V9 catches residue. Surface the residue list to the Governor; per token the Governor classifies (framework-version-mismatch / concept-version-mismatch / neutral content) and disposes (update / acknowledge-as-historical / extend-declarations). Sessions that omit OD §Framework-Version Markers get partial V9 coverage (structural identifiers only — adequate for catching `OBJ-N` / `STR-N` / etc. outside the session's declared range; cannot detect free-text marker residue such as scoring-framework or bucket-vocabulary mismatches). Sessions without inheritance declaration skip V9.

6. **Post-build shape verification (V2).** After any pool build, embedding generation, or chunking operation: inspect the produced artifact's shape (`numpy.load(...).shape`, file count, byte count). If `N_embeddings == N_input_files` for non-trivial input sizes, treat as suspicious and present to Governor before proceeding.

### Audit-tool discipline (cross-cutting)

7. **Audits MUST invoke the Read tool per file checked.** When asked to audit, verify, or summarize a file's state: invoke Read with the file path. Line counts and byte counts reported MUST match disk values, not inferred values. If a count cannot be obtained from a Read call, report "unable to verify" — do not estimate.

8. **Tool-output read-back after non-trivial edits.** After Edit operations on cross-referenced sections (OD ↔ scope, signal ↔ decision, template ↔ session): Read the modified region back and verify the Edit applied as intended. Edit-tool failure modes (whitespace mismatch, partial application) are silent without explicit verification.

9. **Self-correction is not evidence of integrity.** If a prior assistant turn produced unverified content (estimated counts, paraphrased content, fabricated audit) and a subsequent turn corrects it: log the correction explicitly as a `[CORRECTED-IN-LATER-TURN]` annotation. The fact of self-correction does not retroactively validate the prior turn — both must be visible in the trace.

### Active-detection requirement

10. **If you observe friction, log it.** Any of the following is a logging trigger: protocol gap encountered, retrieval below threshold, OD/scope inconsistency, sycophancy event, cite-then-apply violation, out-of-scope engagement attempt, missing declared artifact, mode-flag-without-output. Active capture is the assistant's job; the Governor's review reads the captured artifacts. Capture failures are §8.7 V4 violations.

11. **If a declared structure does not match operational reality, escalate.** Discovering a gap (a declared artifact that doesn't exist; a retrieval contract that doesn't return; an inherited model that doesn't cover declared concepts) is not a continuation signal — it is a halt-and-report signal. The Governor decides what to do with the gap; the assistant's job is to surface it visibly.

### Anti-patterns (excluded)

- **Paraphrasing from memory is not verification.** If the discipline requires a count, a shape, an existence check — invoke the tool. Estimated counts, recalled file structure, and "I believe the file contains" are not §8.7-compliant.
- **Forward-progress bias when a check would surface a gap.** The default assistant behavior is to continue toward the next task. The discipline is to STOP when a check is required, run the check, then continue. Skipping a check because the next step is clear is exactly the failure mode §8.7 exists to prevent.
- **Trusting declared state without verification at boundaries.** "CLAUDE.md says session-logs/ should be populated, so I assume it is" is not §8.7-compliant. Check at the boundary where it matters; do not assume continuity from declaration to operational truth.

## Output Paths

Deliverables and session artifacts go in their canonical directories. Do not mix them:

| Output type | Directory | Examples |
|---|---|---|
| Deliverables | `deliverables/` | Analysis reports, scorecards, gap analyses, feedback documents |
| Session logs | `session-logs/` | `session-NNN.md` — episodic logs of what happened each session |
| Signals | `signals/` | Append-only signal files |
| Health reports | `health-reports/` | Computed health assessments |
| Decisions | `decisions/` | Governor decisions, append-only |

**Session-specific additions:** During bootstrap, the AI may add a `## Session Directives` section below this file's standard content. Session directives may specify additional context loading, analytical standards, or scope-specific rules — but they must NOT override the output paths above. If a session directive specifies a deliverable path that conflicts with `deliverables/`, the directive is in error; use `deliverables/`.

## File Operations

- Commit at meaningful checkpoints: end of phase, after Governor decisions, after deliverable completion.
- Do NOT push without Governor approval.
- Use append-only for signals/ and decisions/ files — never edit existing entries.
- The bootstrap file (00-BOOTSTRAP.md) is the ONLY file that gets fully overwritten each session.

## Multi-Domain Scoring

When scoring against multiple domain models:
- Default to **Level 2 — Sequential Isolation** (score one domain fully before the next, no back-revision)
- Use 1-10 integer scale, no half-points (protocol §7.6)
- For >10 items, calibrate with 3 representative items first

## Starting a New Session

Use the session launcher template to bootstrap a new GOSTA scope:

1. **Copy and fill:** `cowork/session-launcher-template.md` — replace all `{{PLACEHOLDER}}` values
2. **Paste** the filled prompt into a fresh Cowork or Code session
3. The AI will scaffold `sessions/[name]/`, copy templates, load context, and begin Phase 0

The `sessions/` directory (at repo root) is the standard location for new scopes.

### Manual Bootstrap (alternative)

If not using the launcher template:
1. Create the session directory and required subdirectories:
   ```bash
   mkdir -p sessions/[name]/{domain-models,reference,signals,health-reports,decisions,deliverables,session-logs}
   ```
2. Copy templates: `cp cowork/templates/* sessions/[name]/`
3. Copy protocol + directive: `cp cowork/gosta-cowork-protocol.md cowork/CLAUDE.md sessions/[name]/`
4. Create applied domain models using `templates/domain-model.md` and the extraction procedure in `cowork/domain-model-authoring-protocol.md` (not generic — see protocol §3.1)
5. Run a Bootstrap Session (protocol §5.2) — draft the OD for Governor approval. For complex scopes, use `cowork/od-drafting-protocol.md` (structured decomposition questions → OD).
6. Governor reviews and approves the OD before first execution session

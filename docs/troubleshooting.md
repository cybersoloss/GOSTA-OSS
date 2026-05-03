# GOSTA Troubleshooting

Symptom-driven lookup for common issues at session bootstrap and execution. Each entry follows: **Symptom** → **What's happening** → **Fix** → **Why it surfaced** (origin reference).

If your issue isn't here, check [glossary.md](glossary.md) for terminology, [faq.md](faq.md) for general questions, or open an issue per [CONTRIBUTING.md](../CONTRIBUTING.md).

---

## Bootstrap Issues

### Symptom: `pool-agent query` fails with `ValueError: Cannot load file containing pickled data when allow_pickle=False`

**What's happening:** The `embeddings.npy` file in your pool store is a Git LFS pointer (typically ~130 bytes), not the actual NumPy binary. Git LFS pulled the pointer reference but didn't fetch the binary.

**Fix:**
```bash
cd /path/to/repo
git lfs pull --include "path/to/pool-store/*"
python3 cowork/tools/pool-agent.py verify-store --store /path/to/pool-store/
```
The `verify-store` subcommand confirms the binary is materialized and the index counts match.

**Why it surfaced:** Plan #6 added the verify-store guard. Before the guard, the framework reported a generic NumPy error that didn't point to LFS as the root cause.

---

### Symptom: `pool-agent setup-model` fails with import errors

**What's happening:** Setup-model has additional dependencies beyond runtime (huggingface-hub, onnx). Runtime alone isn't enough for the one-time model download + quantization.

**Fix:**
```bash
pip install numpy pyyaml onnxruntime tokenizers huggingface-hub onnx
python3 cowork/tools/pool-agent.py setup-model
```
The model file (`model.onnx`, ~22MB) is gitignored — downloaded fresh each setup.

---

### Symptom: M5 hook reports "hooks not configured" or "M5 WARN" at bootstrap

**What's happening:** Claude Code didn't find a hooks settings file. The M1/M3/M4 mechanizable-discipline checks won't fire and the M5 hook-availability check is reporting that absence.

**Fix:** Install hooks at project level:
```bash
mkdir -p .claude
cp cowork/templates/hooks-settings.json .claude/settings.local.json
```
Or at user level (applies to all GOSTA sessions on this machine):
```bash
mkdir -p ~/.claude
cp cowork/templates/hooks-settings.json ~/.claude/settings.local.json
```
Verify after install:
```bash
cat .claude/settings.local.json | grep -A 5 hooks
```

**Why it surfaced:** Hooks are optional but recommended. Without them, M1/M3/M4 disciplines become Claude-Code-side-only — the orchestrator must remember the discipline manually. M5 reports the absence so the Governor can disposition.

---

### Symptom: Bootstrapper asks 10 questions instead of the 6 mentioned in older docs

**What's happening:** Your version of `cowork/startup.md` Group 1 has 4 capability flags (shortfall logging, assessment target, debug logging, evidence collection mode) added since older walkthrough versions were written. This is correct current behavior, not a bug.

**Fix:** Answer "no" / "none" to the 4 capability flags for a simple session — they activate optional features only when needed. See current `docs/walkthrough.md` for the full 10-question flow.

**Why it surfaced:** Framework evolution; older docs may show fewer questions.

---

## Phase Gate / Validation Issues

### Symptom: V8 reports `permission denied` / `Bash blocked` / sandbox-path-resolution error

**What's happening:** Your subagent dispatch capability test (V8) failed because the subagent's runtime environment doesn't match the orchestrator's. The subagent can't access paths the orchestrator can, or can't execute tools the orchestrator can.

**Fix:** V8 surfaces three mitigation options to Governor:
1. **reroute-path** — switch path conventions so the subagent's sandbox can resolve them (e.g., absolute path → mounted path).
2. **extend-sandbox** — grant the subagent additional permissions (Cowork mode: increase tool grants; Code mode: adjust workspace mount).
3. **collapse-to-orchestrator** — execute the work in the orchestrator runtime directly, skipping subagent dispatch for this session.

**Why it surfaced:** Spec §8.7 V8 added with subagent-dispatch awareness. Pre-V8, sessions hit this error mid-execution; V8 surfaces it at bootstrap.

---

### Symptom: V9 reports framework-residue tokens that need disposition

**What's happening:** Your session inherits artifacts (domain models, scope, etc.) from a prior session. V9 audited the inherited content for tokens (structural identifiers like `OBJ-N`, `STR-N`, framework-version markers like `v3`, `v4`, `MVP`, `Post-MVP`) that don't appear in the current session's declarations. These are framework-residue from the source session.

**Fix:** Per-token Governor disposition options:
- **acknowledge-as-historical** — token is from prior session's framing, not relevant to current; document and proceed.
- **update** — token represents stale framework state that should be replaced with current framing.
- **extend-declarations** — token is valid; current session should declare the missing concept.

Document each disposition in OD §Decision History.

**Why it surfaced:** Spec §8.7 V9 — inheritance is structurally different from authoring; framework-residue can carry stale assumptions silently. V9 makes them explicit.

---

### Symptom: Coverage WARN appears at sub-threshold but doesn't escalate

**What's happening:** Older framework behavior auto-resolved coverage WARNs at Independence Level 3. Plan #7 changed this — coverage WARNs now escalate to Governor disposition regardless of independence.

**Fix:** If using current framework: coverage WARN escalates correctly; Governor dispositions: accept-as-evidence-base-limitation / re-collect / downgrade. Deliverables include `## Coverage Limitations Disclosure` section (§12.15) when sub-threshold.

If using older framework state: update to current cowork-protocol or add `[CORRECTED-IN-LATER-TURN]` annotation to existing coverage logs.

**Why it surfaced:** Plan #7 simplified the coverage handling; older sessions auto-resolved silently.

---

### Symptom: Bootstrap pauses at Phase Gate request waiting for Governor

**What's happening:** Phase gate requires Governor disposition (per spec §5.5). Sessions configured at high autonomy can still hit phase gates that need explicit decision (e.g., V-gate FAIL, AFC drift, blocking tensions surfaced).

**Fix:** Either:
1. Pre-author a `governor-policy.md` file in the session directory that pre-authorizes phase-gate dispositions mechanically (see `docs/examples/` for patterns where this applies), OR
2. Disposition manually at each phase gate when prompted.

The `--dangerously-skip-permissions` flag affects Claude Code permission prompts, NOT GOSTA phase-gate flow. Phase gates are intrinsic to spec §5.5 and require Governor decision.

**Why it surfaced:** Phase gates are designed safety checkpoints. They don't auto-pass.

---

## Deliverable Production Issues

### Symptom: M4 hook fires WARN repeatedly across multiple deliverables in one session

**What's happening:** Deliverable agents are producing initial drafts WITHOUT the `## Frame Integrity Validation` section, then adding it after M4 fires. Each Edit operation triggers M4 again until the section appears. Outcome is correct; cycle is wasteful.

**Fix:** Pre-include `## Frame Integrity Validation` section in initial deliverable drafts, not reactively after M4 fires. Update your dispatch prompts to deliverable agents to include the section structure as part of the template, not as a closeout add-on.

**Why it surfaced:** Plan #19 §12.12 scope extension. The hook is correct; the cycle is operationally wasteful but doesn't produce wrong output.

---

### Symptom: Position papers exceed per-deliverable cap by 2-7×

**What's happening:** OD declared a fixed cap (e.g., 4 KB) without modeling content density. With cite-then-apply discipline (G-10) producing concept-definition + per-evidence-application chains, position papers at deliberation scale routinely run 6-15 KB.

**Fix:** Use formula-based caps in OD `## Per-Deliverable Caps`:
```
position-*.md: base=4kb + 1.0kb × evidence_items_assigned
```
For a 12-item agent: 4 + 12 = 16 KB cap (vs the agent producing ~12 KB at G-10 discipline).

Sessions using formula caps must include `evidence_items_assigned: <count>` in YAML front matter for the M3 hook to resolve the formula correctly.

**Why it surfaced:** Plan #17 added formula-based cap support; Plan #20 made it the recommended default for content-density-variable artifacts. Older OD templates show fixed caps; current templates show formula examples.

---

### Symptom: Verdict-band split unresolved at Round 5 deliberation termination

**What's happening:** A candidate's verdict has intra-cluster disagreement (e.g., LOW ↔ MED in same cluster) at Round 5 termination. Older deliberation flow allowed termination with the split silent; current flow (Plan #13) requires explicit handling.

**Fix:** Two paths per Plan #13:
1. **Targeted re-dispatch** — run one more round limited to the open split. Use this if the disagreement is data-driven (one more round may close it).
2. **Governor override with `[VERDICT-SPLIT-CARRIED]` annotation** — carry the split into the deliverable inline alongside the verdict. Use this if the disagreement is structural (more rounds wouldn't close it).

Default is targeted re-dispatch unless Governor selects override.

**Why it surfaced:** Plan #13 verdict-split-aware termination. Pre-Plan-#13, splits could ship silent in deliverable footnotes.

---

### Symptom: Synthesis report missing `## Frame Integrity Validation` section, hook fires

**What's happening:** Plan #19 extended §12.12 scope to synthesis-report.md and phase-gate-*.md. Older synthesis-report templates don't have the section.

**Fix:** Add the section to your synthesis-report template. Format mirrors the deliverable §12.12 audit table:

```markdown
## Frame Integrity Validation

| AFC Field | Declared Value | Audit Result | Notes |
|---|---|---|---|
| Stance | <from OD> | PASS / FAIL / NOTE | <observation> |
| Output Verb | <from OD> | PASS / FAIL / NOTE | <observation> |
| Failure Mode | <from OD> | PASS / FAIL / NOTE | <observation> |
| Prohibited Frame | <from OD> | PASS / FAIL / NOTE | <observation> |
```

Coordinator transcribes the synthesis-level audit; deliverable agents transcribe rather than re-derive.

**Why it surfaced:** Plan #19 — frame-drift at synthesis cascades to deliverables, so synthesis is the right boundary to audit.

---

## Domain Model Issues

### Symptom: Domain model concepts produce vague, ungrounded scoring

**What's happening:** Concepts may lack boundaries or misapplication notes, so the AI can't tell when to apply them vs when not to. Quality Principles may not be testable, so they don't constrain scoring meaningfully.

**Fix:** Run the quality-gate checklist on the model:
- Every concept has explicit boundaries (what it doesn't cover)?
- Every concept has misapplication notes (common errors)?
- Every Quality Principle has an observable criterion (testable)?
- Anti-Patterns are not just inverse-of-QPs (independent failure modes)?

If multiple fail, the model needs revision. See [authoring-domain-models.md](authoring-domain-models.md) for the full authoring procedure.

**Why it surfaced:** Domain model quality directly determines session output quality. Shallow models produce shallow sessions.

---

### Symptom: Two domain models duplicate each other's concepts

**What's happening:** Without explicit boundary clarification between models, they may overlap (e.g., "user-value" model and "market-fit" model both score willingness-to-pay).

**Fix:** Add a "Cross-model boundary clarification" section to each affected model declaring: what THIS model owns, what the OTHER model owns, and where they overlap intentionally vs accidentally.

**Why it surfaced:** Multi-domain deliberation requires clean boundaries; overlap produces double-counting and false agreement.

---

## Session Lifecycle Issues

### Symptom: Session-private content (session names, candidate IDs, domain abbreviations) leaking into framework files

**What's happening:** Authoring discipline lapsed; pre-commit hook BLOCKs the commit with offending lines highlighted.

**Fix:** Replace specific tokens with abstract placeholders or describe the structural pattern without naming the session. See `cowork/verification-patterns.md` Pattern 8 for examples and the recursive lesson.

The pre-commit hook at `.github/hooks/pre-commit` enforces this. Install with:
```bash
cp .github/hooks/pre-commit .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
```

**Why it surfaced:** Pattern 8 — framework files are domain-agnostic by design (spec §0.1). Session-private content violates that.

---

### Symptom: V6 closeout audit fails — artifacts exist but are template-shaped

**What's happening:** V6 has two layers: A (existence) + B (population). Layer A passes (artifact non-zero) because template scaffolding has content; Layer B catches that the `[POPULATE: ...]` sentinels weren't replaced.

**Fix:** Replace each `[POPULATE: ...]` sentinel with actual content meeting the per-section word floor (default 20 words). If a section genuinely has nothing to populate, replace the sentinel with explicit "No <section> observed this session — <reason>" statement.

**Why it surfaced:** Closeout-fidelity gap is the canonical failure mode V6 Layer B catches. Template scaffolding lets sessions pass mechanical existence checks while shipping unpopulated artifacts.

---

## Pool / Reference Issues

### Symptom: Pool query returns unexpected score thresholds (≥0.58 / 0.50-0.57 / <0.50)

**What's happening:** These are protocol-defined thresholds, not bugs. ≥0.58 = read full article. 0.50-0.57 = excerpt only. <0.50 = ignore.

**Fix:** Calibrate query phrasing if too few results pass threshold. Vague queries match weakly; specific queries match strongly. Check pool composition — if relevant material isn't in the pool, no query phrasing will surface it.

**Why it surfaced:** Threshold-based retrieval is intentional — prevents noisy material from polluting evidence base.

---

### Symptom: Reference Pool content not retrieved by pool-agent semantic search even though it's there

**What's happening:** Two common causes:
1. **Vocabulary mismatch** — query uses domain vocabulary that doesn't appear in the source material's wording. Try synonyms or paraphrases.
2. **Section-indexed pools** — large documents indexed via `index-doc` chunk by section heading. If the relevant content is in a section without a heading or under a misleading heading, semantic search may miss it.

**Fix:** Try paraphrased query first. If still missing, load the file directly via Reference Pool (role: context) instead of pool-agent retrieval. Some material is better consumed directly than via semantic search.

**Why it surfaced:** Pool-agent is offline semantic search using a small embedding model (all-MiniLM-L6-v2). It's good for general retrieval but isn't a substitute for direct read when material is specifically targeted.

---

## Related

- [Glossary](glossary.md) — terminology lookup
- [FAQ](faq.md) — general questions
- [Walkthrough](walkthrough.md) — step-by-step first session
- [verification-patterns.md](../cowork/verification-patterns.md) — decision verification discipline

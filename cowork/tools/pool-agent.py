#!/usr/bin/env python3
"""
GOSTA Reference Pool Agent
Semantic search over any GOSTA-compliant reference pool YAML.

Uses all-MiniLM-L6-v2 (ONNX, quantized) + numpy cosine similarity.
No torch required. No external API calls during query.

USAGE
-----
# Build vector store from a pool (run once, or after pool updates)
python3 pool-agent.py build \\
    --pool /path/to/reference-pool.yaml \\
    --articles /path/to/blogs/ \\
    --store /path/to/pool-store/

# Query
python3 pool-agent.py query "hospital cybersecurity incidents" \\
    --store /path/to/pool-store/ \\
    --top 10

# Index a single large markdown document by section headings
python3 pool-agent.py index-doc \\
    --doc /path/to/large-document.md \\
    --store /path/to/doc-store/ \\
    --heading-level 2

# List available tags in pool
python3 pool-agent.py tags --pool /path/to/reference-pool.yaml

# Verify pool store integrity (LFS-pointer + shape + consistency check)
python3 pool-agent.py verify-store --store /path/to/pool-store/

STORE LAYOUT
------------
pool-store/
  embeddings.npy     # (N, 384) float32 embedding matrix
  metadata.json      # list of {id, title, tags, excerpt, sourceFile, sourceDir}
  pool-info.json     # pool name, version, itemCount, buildDate

MODEL SETUP
-----------
# First-time setup: download and quantize the model
python3 pool-agent.py setup-model

This downloads all-MiniLM-L6-v2 from Hugging Face, quantizes it to
qint8 ONNX (~22MB), and saves tokenizer files. Run once per clone.

Model files (cowork/tools/pool-agent/models/):
  model.onnx                # all-MiniLM-L6-v2 qint8 quantized (~22MB, gitignored)
  tokenizer.json            # tracked in git
  tokenizer_config.json     # tracked in git
  special_tokens_map.json   # tracked in git

Dependencies (runtime, required for query/build/index-doc/update): pip install numpy pyyaml onnxruntime tokenizers
Dependencies (setup-model-only, beyond runtime): pip install huggingface-hub onnx
"""

import argparse
import json
import os
import sys
import re
import math
from pathlib import Path
from datetime import datetime

import numpy as np
import yaml

# ── paths ──────────────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).parent
MODELS_DIR = SCRIPT_DIR / "pool-agent" / "models"
MODEL_PATH  = MODELS_DIR / "model.onnx"

# ── embedding ──────────────────────────────────────────────────────────────────

def load_model():
    """Load ONNX model + tokenizer. Returns (session, tokenizer)."""
    if not MODEL_PATH.exists():
        print("ERROR: Model file not found.", file=sys.stderr)
        print(f"  Expected: {MODEL_PATH}", file=sys.stderr)
        print(f"", file=sys.stderr)
        print(f"  Run 'python3 {Path(__file__).name} setup-model' to download", file=sys.stderr)
        print(f"  and quantize the model automatically (~90MB download,", file=sys.stderr)
        print(f"  produces ~22MB quantized ONNX).", file=sys.stderr)
        sys.exit(1)

    tok_path = MODELS_DIR / "tokenizer.json"
    if not tok_path.exists():
        print("ERROR: Tokenizer not found.", file=sys.stderr)
        print(f"  Expected: {tok_path}", file=sys.stderr)
        print(f"", file=sys.stderr)
        print(f"  Run 'python3 {Path(__file__).name} setup-model' to download.", file=sys.stderr)
        sys.exit(1)

    import onnxruntime as ort
    from tokenizers import Tokenizer

    sess = ort.InferenceSession(
        str(MODEL_PATH),
        providers=["CPUExecutionProvider"]
    )
    tok = Tokenizer.from_file(str(tok_path))
    tok.enable_padding(pad_token="[PAD]", pad_id=0)
    tok.enable_truncation(max_length=512)
    return sess, tok


def mean_pool(token_embeddings, attention_mask):
    """Mean pool token embeddings, ignoring padding."""
    mask = attention_mask[:, :, np.newaxis].astype(np.float32)
    summed = (token_embeddings * mask).sum(axis=1)
    counts = mask.sum(axis=1).clip(min=1e-9)
    return summed / counts


def embed_texts(sess, tok, texts, batch_size=32, show_progress=False):
    """Embed a list of strings. Returns (N, 384) float32 ndarray."""
    all_embeddings = []
    total = len(texts)

    for i in range(0, total, batch_size):
        batch = texts[i : i + batch_size]
        enc = tok.encode_batch(batch)

        input_ids      = np.array([e.ids for e in enc],               dtype=np.int64)
        attention_mask = np.array([e.attention_mask for e in enc],     dtype=np.int64)
        token_type_ids = np.zeros_like(input_ids)

        outputs = sess.run(None, {
            "input_ids":      input_ids,
            "attention_mask": attention_mask,
            "token_type_ids": token_type_ids,
        })

        # outputs[0] shape: (batch, seq_len, 384)
        pooled = mean_pool(outputs[0], attention_mask)

        # L2 normalise for cosine similarity via dot product
        norms  = np.linalg.norm(pooled, axis=1, keepdims=True).clip(min=1e-9)
        pooled = pooled / norms

        all_embeddings.append(pooled.astype(np.float32))

        if show_progress:
            done = min(i + batch_size, total)
            print(f"  Embedded {done}/{total}...", flush=True)

    return np.vstack(all_embeddings)


# ── store I/O ──────────────────────────────────────────────────────────────────

# Git LFS pointer files start with this exact byte sequence per LFS spec v1.
# When a pool store's binary (e.g. embeddings.npy) has not been pulled from LFS,
# the file on disk is a small (~130 byte) ASCII text file with this signature
# instead of the actual binary. Loading it with np.load produces a cryptic
# pickle-key error that does not point to the root cause; the helpers below
# detect the pointer state and raise an actionable message.
LFS_POINTER_SIGNATURE = b"version https://git-lfs.github.com/spec/v1"


def _is_lfs_pointer(path):
    """Return True if file at path is a Git LFS pointer (binary not pulled)."""
    try:
        with open(path, "rb") as f:
            head = f.read(64)
    except OSError:
        return False
    return head.startswith(LFS_POINTER_SIGNATURE)


def _ensure_not_lfs_pointer(path):
    """Raise RuntimeError with actionable diagnostic if path is an LFS pointer."""
    if _is_lfs_pointer(path):
        raise RuntimeError(
            f"Git LFS pointer file detected at {path}.\n"
            f"  The pool store's binary content has not been pulled from LFS.\n"
            f"  Fix: cd into the git repository containing this file, then run:\n"
            f"    git lfs pull --include '<path-relative-to-repo-root>'\n"
            f"  Then re-run pool-agent."
        )


def save_store(store_path, embeddings, metadata, pool_info):
    store_path = Path(store_path)
    store_path.mkdir(parents=True, exist_ok=True)
    np.save(str(store_path / "embeddings.npy"), embeddings)
    (store_path / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2)
    )
    (store_path / "pool-info.json").write_text(
        json.dumps(pool_info, ensure_ascii=False, indent=2)
    )


def load_store(store_path):
    store_path = Path(store_path)
    # Guard all three pool-store files against Git LFS pointer state.
    # JSON files are typically not LFS-tracked, but the check is cheap and
    # produces a clear diagnostic if metadata.json or pool-info.json end up
    # pointer-shaped (e.g. via a `.gitattributes` rule applied broadly).
    _ensure_not_lfs_pointer(store_path / "embeddings.npy")
    _ensure_not_lfs_pointer(store_path / "metadata.json")
    _ensure_not_lfs_pointer(store_path / "pool-info.json")
    embeddings = np.load(str(store_path / "embeddings.npy"))
    metadata   = json.loads((store_path / "metadata.json").read_text())
    pool_info  = json.loads((store_path / "pool-info.json").read_text())
    return embeddings, metadata, pool_info


# ── article content ────────────────────────────────────────────────────────────

def read_article_snippet(articles_base, source_dir, source_file, max_chars=800):
    """Read first max_chars of an article file. Returns '' on failure."""
    if not (articles_base and source_dir and source_file):
        return ""
    path = Path(articles_base) / source_dir / source_file
    if not path.exists():
        return ""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
        # strip markdown frontmatter / headings for cleaner embedding
        text = re.sub(r"^---.*?---\s*", "", text, flags=re.DOTALL)
        text = re.sub(r"#+\s+", "", text)
        return text[:max_chars].strip()
    except Exception:
        return ""


# ── build ──────────────────────────────────────────────────────────────────────

def cmd_build(args):
    pool_path    = Path(args.pool)
    store_path   = Path(args.store)
    articles_base = args.articles  # may be None

    print(f"Loading pool: {pool_path}")
    raw = yaml.safe_load(pool_path.read_text(encoding="utf-8"))

    # Support both top-level 'items' and nested 'referencePool.items'
    items    = raw.get("items", raw.get("referencePool", {}).get("items", []))
    rp_meta  = raw.get("referencePool", {})
    if not items:
        print("ERROR: No items found in pool YAML.", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(items)} items. Loading model...")
    sess, tok = load_model()
    print("Model loaded.")

    texts    = []
    metadata = []

    for item in items:
        rp_id      = item.get("id", "")
        title      = item.get("title", "")
        excerpt    = item.get("excerpt", "")
        tags       = item.get("tags", [])
        source_dir = item.get("sourceDir", "")
        source_file = item.get("sourceFile", "")

        snippet = read_article_snippet(articles_base, source_dir, source_file)

        # Compose embedding text: title + excerpt + article snippet
        # Tags included as plain text for soft tag-based retrieval
        tag_str = " ".join(tags).replace("-", " ")
        embed_text = f"{title}. {excerpt} {snippet} {tag_str}".strip()

        texts.append(embed_text)
        metadata.append({
            "id":         rp_id,
            "title":      title,
            "tags":       tags,
            "excerpt":    excerpt[:400],
            "sourceFile": source_file,
            "sourceDir":  source_dir,
        })

    print(f"Embedding {len(texts)} items...")
    embeddings = embed_texts(sess, tok, texts, show_progress=True)

    pool_info = {
        "poolFile":   str(pool_path),
        "poolName":   rp_meta.get("name", pool_path.stem),
        "version":    rp_meta.get("version", "?"),
        "itemCount":  len(items),
        "buildDate":  datetime.utcnow().isoformat() + "Z",
        "model":      "all-MiniLM-L6-v2-qint8",
    }

    save_store(store_path, embeddings, metadata, pool_info)
    print(f"\nDone. Store saved to: {store_path}")
    print(f"  Items:  {len(items)}")
    print(f"  Shape:  {embeddings.shape}")


# ── query ──────────────────────────────────────────────────────────────────────

def _threshold_action(score: float) -> str:
    """Map similarity score to protocol-defined consumption action.

    Thresholds from Cowork Protocol §18.5:
      ≥0.58 → full_read (read full article/section)
      0.50–0.57 → excerpt_only (read excerpt, skip full content)
      <0.50 → ignore (below relevance threshold)
    """
    if score >= 0.58:
        return "full_read"
    elif score >= 0.50:
        return "excerpt_only"
    else:
        return "ignore"


def cmd_query(args):
    store_path = Path(args.store)
    if not store_path.exists():
        print(f"ERROR: Store not found at {store_path}", file=sys.stderr)
        sys.exit(1)

    embeddings, metadata, pool_info = load_store(store_path)

    sess, tok = load_model()
    q_emb = embed_texts(sess, tok, [args.query_text])  # (1, 384)

    # Cosine similarity = dot product (embeddings are L2-normalised)
    scores = (embeddings @ q_emb.T).squeeze()  # (N,)
    top_n  = min(args.top, len(scores))
    top_idx = np.argsort(scores)[::-1][:top_n]

    print(f"\nPool:  {pool_info['poolName']}  (v{pool_info['version']}, {pool_info['itemCount']} items)")
    print(f"Query: \"{args.query_text}\"")
    print(f"Top {top_n} results:\n")

    is_doc_store = pool_info.get("indexMode") == "document-sections"

    if args.json:
        results = []
        for rank, idx in enumerate(top_idx, 1):
            m = metadata[idx]
            s = round(float(scores[idx]), 4)
            entry = {
                "rank":       rank,
                "id":         m["id"],
                "score":      s,
                "threshold_action": _threshold_action(s),
                "title":      m["title"],
                "tags":       m["tags"],
                "excerpt":    m["excerpt"],
                "sourceDir":  m["sourceDir"],
                "sourceFile": m["sourceFile"],
            }
            # Include section-specific fields when querying a document store
            if "section_range" in m:
                entry["section_range"]  = m["section_range"]
            if "heading_level" in m:
                entry["heading_level"]  = m["heading_level"]
            results.append(entry)
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for rank, idx in enumerate(top_idx, 1):
            m     = metadata[idx]
            score = scores[idx]
            action = _threshold_action(float(score))
            tags  = ", ".join(m["tags"][:6])
            loc = m.get("section_range", f"{m['sourceDir']}/{m['sourceFile']}")
            print(f"[{rank}] {m['id']}  score={score:.3f}  [{action}]")
            print(f"     {m['title']}")
            print(f"     Tags: {tags}")
            print(f"     {m['excerpt'][:120]}...")
            print(f"     {loc}  ({m['sourceFile']})")
            print()


# ── tag extraction (for update command) ───────────────────────────────────────

TAG_RULES = {
    "regulatory-compliance":       ["nis2", "dora", "gdpr", "regulation", "compliance",
                                    "regulatory", "enforcement", "penalty", "fine",
                                    "audit", "directive"],
    "third-party-risk-management": ["third.party", "vendor risk", "supplier risk", "tprm",
                                    "third party risk", "vendor management", "outsourc"],
    "incident-response":           ["incident response", "breach response", "remediation",
                                    "recovery", "notification", "disclosure", "containment"],
    "contract-liability":          ["contract", "liability", "indemnif", "lawsuit",
                                    "litigation", "settlement", "obligation", r"\bsla\b"],
    "vendor-breach":               ["vendor breach", "supplier breach", "service provider.*breach",
                                    "breach.*vendor", "breach.*supplier"],
    "supply-chain-attack":         ["supply chain attack", "supply chain compromise",
                                    "software supply chain", "upstream attack"],
    "data-breach-tracker":         ["data breach", "records exposed", "records compromised",
                                    "records stolen", "breach tracker"],
    "financial-sector":            ["bank breach", "banking breach", "credit union breach",
                                    "bank of america", "jpmorgan", r"\bfintech\b.*breach"],
    "healthcare-breach":           ["hospital breach", "patient data", "hipaa breach",
                                    "healthcare breach", "medical.*breach", "change healthcare",
                                    "stryker", "ehr breach"],
    "ransomware":                  ["ransomware", r"\bransom\b", "wiper malware", "lockbit",
                                    "blackcat", "alphv", "ryuk", "revil", "conti"],
    "government-public-sector":    ["government.*breach", "municipal.*breach", "city.*hack",
                                    "public sector", "federal.*breach"],
    "msp-mssp":                    ["managed service provider", "msp breach", r"\bmssp\b",
                                    "managed security", r"\brmm\b"],
    "the-register":                ["the register", "theregister.co"],
    "techcrunch":                  ["techcrunch"],
    "reddit":                      [r"\breddit\b"],
}


def _extract_tags(text: str) -> list:
    text_lower = text.lower()
    tags = []
    for tag, patterns in TAG_RULES.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                tags.append(tag)
                break
    return tags


def _extract_title(text: str) -> str:
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()[:200]
        if line and not line.startswith("#"):
            return line[:200]
    return "Untitled"


def _extract_excerpt(text: str, max_chars: int = 400) -> str:
    text = re.sub(r"^---.*?---\s*", "", text, flags=re.DOTALL)
    text = re.sub(r"^#{1,6}\s+.*$", "", text, flags=re.MULTILINE)
    paras = [p.strip() for p in re.split(r"\n\n+", text) if len(p.strip()) > 60]
    return paras[0][:max_chars] if paras else text[:max_chars].strip()


# ── internal build helper ──────────────────────────────────────────────────────

def _run_build(pool_path: str, articles_base: str, store_path: str):
    """Build vector store — callable internally after update/delete."""
    class _Args:
        pool     = pool_path
        articles = articles_base
        store    = store_path
    cmd_build(_Args())


# ── update ─────────────────────────────────────────────────────────────────────

def cmd_update(args):
    pool_path  = Path(args.pool)
    new_dir    = Path(args.dir)
    store_path = Path(args.store)

    if not new_dir.exists():
        print(f"ERROR: Directory not found: {new_dir}", file=sys.stderr)
        sys.exit(1)

    raw      = yaml.safe_load(pool_path.read_text(encoding="utf-8"))
    items    = raw.get("items", [])
    rp_meta  = raw.get("referencePool", {})

    existing_files = {item.get("sourceFile", "") for item in items}
    max_id  = max((int(x["id"].split("-")[1]) for x in items
                   if x.get("id", "").startswith("RP-")), default=0)
    next_id = max_id + 1
    source_dir_name = new_dir.name

    new_items, skipped = [], 0
    for filepath in sorted(new_dir.glob("*.md")):
        if filepath.name in existing_files:
            skipped += 1
            continue
        try:
            text = filepath.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        new_items.append({
            "id":             f"RP-{next_id:03d}",
            "title":          _extract_title(text),
            "contentType":    "blog-post",
            "sourceUrl":      "",
            "publishDate":    "",
            "tags":           _extract_tags(text),
            "relevanceStatus":"active",
            "addedBy":        "pool-agent-update",
            "contentHash":    "",
            "sourceFile":     filepath.name,
            "sourceDir":      source_dir_name,
            "excerpt":        _extract_excerpt(text),
        })
        next_id += 1

    if not new_items:
        print(f"No new items found. {skipped} file(s) already in pool.")
        return

    items.extend(new_items)
    rp_meta["itemCount"]    = len(items)
    rp_meta["lastUpdated"]  = datetime.utcnow().strftime("%Y-%m-%d")
    counts = {}
    for item in items:
        for tag in item.get("tags", []):
            counts[tag] = counts.get(tag, 0) + 1
    rp_meta["topicDistribution"] = dict(sorted(counts.items(), key=lambda x: -x[1]))

    raw["referencePool"] = rp_meta
    raw["items"]         = items
    pool_path.write_text(
        yaml.dump(raw, allow_unicode=True, default_flow_style=False, sort_keys=False),
        encoding="utf-8"
    )

    print(f"Added {len(new_items)} items  (skipped {skipped} duplicates).")
    print(f"Pool now has {len(items)} items.")
    print(f"New IDs: {new_items[0]['id']} — {new_items[-1]['id']}")

    print("\nRebuilding vector store...")
    _run_build(str(pool_path), args.articles, str(store_path))


# ── delete ─────────────────────────────────────────────────────────────────────

def cmd_delete(args):
    pool_path  = Path(args.pool)
    store_path = Path(args.store)

    raw     = yaml.safe_load(pool_path.read_text(encoding="utf-8"))
    items   = raw.get("items", [])
    rp_meta = raw.get("referencePool", {})

    ids_to_delete = set(args.ids)        if args.ids        else set()
    dir_to_delete = args.source_dir[0]   if args.source_dir else None

    removed = [i for i in items if
               i.get("id") in ids_to_delete or
               (dir_to_delete and i.get("sourceDir") == dir_to_delete)]
    kept    = [i for i in items if i not in removed]

    if not removed:
        print("No items matched deletion criteria.")
        return

    rp_meta["itemCount"]   = len(kept)
    rp_meta["lastUpdated"] = datetime.utcnow().strftime("%Y-%m-%d")
    counts = {}
    for item in kept:
        for tag in item.get("tags", []):
            counts[tag] = counts.get(tag, 0) + 1
    rp_meta["topicDistribution"] = dict(sorted(counts.items(), key=lambda x: -x[1]))

    raw["referencePool"] = rp_meta
    raw["items"]         = kept
    pool_path.write_text(
        yaml.dump(raw, allow_unicode=True, default_flow_style=False, sort_keys=False),
        encoding="utf-8"
    )

    print(f"Deleted {len(removed)} item(s):")
    for item in removed:
        print(f"  {item['id']} — {item['title'][:70]}")
    print(f"\nPool now has {len(kept)} items (was {len(items)}).")

    print("\nRebuilding vector store...")
    _run_build(str(pool_path), args.articles, str(store_path))


# ── index-doc ─────────────────────────────────────────────────────────────────

def _segment_markdown(text, heading_level=2):
    """Segment a markdown document by heading level into sections.

    Returns a list of dicts:
      {heading, content, line_start, line_end, level}

    Each section starts at the heading line and extends to the line before the
    next heading at the same or higher level (or EOF). Content between the start
    of the document and the first heading is captured as a "preamble" section.
    """
    pattern = r"^(#{1," + str(heading_level) + r"})\s+(.+)$"
    lines = text.split("\n")

    # Find all heading positions
    headings = []
    for i, line in enumerate(lines):
        m = re.match(pattern, line)
        if m:
            headings.append({
                "line": i,
                "level": len(m.group(1)),
                "heading": m.group(2).strip(),
            })

    sections = []

    # Preamble: content before the first heading (if any)
    if headings and headings[0]["line"] > 0:
        preamble_lines = lines[: headings[0]["line"]]
        preamble_text = "\n".join(preamble_lines).strip()
        if len(preamble_text) > 50:  # only if substantial
            sections.append({
                "heading": "Preamble",
                "content": preamble_text,
                "line_start": 1,
                "line_end": headings[0]["line"],
                "level": 0,
            })

    # Each heading-delimited section
    for i, h in enumerate(headings):
        start = h["line"]
        end = headings[i + 1]["line"] if i + 1 < len(headings) else len(lines)
        section_lines = lines[start:end]
        content = "\n".join(section_lines).strip()

        sections.append({
            "heading": h["heading"],
            "content": content,
            "line_start": start + 1,   # 1-based for human readability
            "line_end": end,
            "level": h["level"],
        })

    return sections


def _heading_to_slug(heading):
    """Convert heading text to a short slug for section IDs."""
    slug = re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-")
    return slug[:60]


def _section_excerpt(content, max_chars=400):
    """Extract first meaningful paragraph from section content."""
    # Skip the heading line itself
    lines = content.split("\n")
    body_lines = [l for l in lines if not l.startswith("#")]
    body = "\n".join(body_lines).strip()
    # Take first substantial paragraph
    paras = [p.strip() for p in re.split(r"\n\n+", body) if len(p.strip()) > 30]
    if paras:
        return paras[0][:max_chars]
    return body[:max_chars].strip()


def _section_tags(content):
    """Extract lightweight tags from section content using keyword heuristics."""
    text_lower = content.lower()
    tags = []
    # Generic topic detection — lightweight, not domain-specific
    topic_signals = {
        "governance":    ["governance", "governor", "approval", "authority"],
        "execution":     ["execution", "executor", "action", "work plan"],
        "deliberation":  ["deliberation", "debate", "consensus", "disagreement"],
        "signals":       ["signal", "health", "metric", "measurement"],
        "domain-model":  ["domain model", "domain identity", "guardrail"],
        "reference-pool":["reference pool", "reference material", "pool-agent"],
        "operating-doc": ["operating document", "od ", "five-layer"],
        "graduation":    ["graduation", "stage ", "autonomy level"],
        "review":        ["review", "strategy review", "tactic review"],
        "memory":        ["memory", "knowledge flag", "context compression"],
        "protocol":      ["protocol", "phase gate", "lifecycle"],
        "security":      ["security", "threat", "vulnerability", "risk"],
    }
    for tag, patterns in topic_signals.items():
        for pattern in patterns:
            if pattern in text_lower:
                tags.append(tag)
                break
    return tags


def cmd_index_doc(args):
    """Index a single large markdown document by segmenting it into sections."""
    doc_path   = Path(args.doc)
    store_path = Path(args.store)
    heading_level = args.heading_level
    id_prefix  = args.id_prefix

    if not doc_path.exists():
        print(f"ERROR: Document not found: {doc_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Loading document: {doc_path}")
    text = doc_path.read_text(encoding="utf-8", errors="replace")
    total_lines = text.count("\n") + 1

    print(f"  Lines: {total_lines}")
    print(f"  Segmenting by heading level ≤ {heading_level} ({'#' * heading_level})...")

    sections = _segment_markdown(text, heading_level)
    if not sections:
        print("ERROR: No sections found. Check heading level.", file=sys.stderr)
        sys.exit(1)

    print(f"  Found {len(sections)} sections. Loading model...")
    sess, tok = load_model()
    print("  Model loaded.")

    texts    = []
    metadata = []

    for i, sec in enumerate(sections):
        sec_id = f"{id_prefix}{i + 1:03d}"
        heading = sec["heading"]
        content = sec["content"]
        excerpt = _section_excerpt(content)
        tags    = _section_tags(content)

        # Embed text: heading + first ~1500 chars of content
        # (MiniLM truncates at 512 tokens ≈ ~2000 chars; front-load signal)
        embed_content = content[:1500]
        tag_str = " ".join(tags).replace("-", " ")
        embed_text = f"{heading}. {embed_content} {tag_str}".strip()

        texts.append(embed_text)
        metadata.append({
            "id":           sec_id,
            "title":        heading,
            "tags":         tags,
            "excerpt":      excerpt[:400],
            "sourceFile":   doc_path.name,
            "sourceDir":    str(doc_path.parent),
            "section_range": f"L{sec['line_start']}-L{sec['line_end']}",
            "heading_level": sec["level"],
        })

    print(f"  Embedding {len(texts)} sections...")
    embeddings = embed_texts(sess, tok, texts, show_progress=True)

    pool_info = {
        "sourceDocument": str(doc_path),
        "poolName":       doc_path.stem,
        "version":        "1.0",
        "itemCount":      len(sections),
        "buildDate":      datetime.utcnow().isoformat() + "Z",
        "model":          "all-MiniLM-L6-v2-qint8",
        "indexMode":      "document-sections",
        "headingLevel":   heading_level,
        "totalLines":     total_lines,
    }

    save_store(store_path, embeddings, metadata, pool_info)
    print(f"\nDone. Store saved to: {store_path}")
    print(f"  Sections: {len(sections)}")
    print(f"  Shape:    {embeddings.shape}")
    print(f"\nSection index:")
    for m in metadata:
        print(f"  {m['id']}  {m['section_range']:>12}  {m['title'][:70]}")


# ── setup-model ───────────────────────────────────────────────────────────────

HF_MODEL_ID  = "sentence-transformers/all-MiniLM-L6-v2"
ONNX_SUBPATH = "onnx/model.onnx"                 # full-precision ONNX in the HF repo
TOKENIZER_FILES = [
    "tokenizer.json",
    "tokenizer_config.json",
    "special_tokens_map.json",
]


def cmd_setup_model(args):
    """Download all-MiniLM-L6-v2 from Hugging Face and quantize to qint8."""
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    if MODEL_PATH.exists() and not args.force:
        print(f"Model already exists at {MODEL_PATH}")
        print(f"  Size: {MODEL_PATH.stat().st_size / 1e6:.1f} MB")
        print(f"  Use --force to re-download and re-quantize.")
        return

    # ── check optional dependencies ──────────────────────────────────────────
    try:
        from huggingface_hub import hf_hub_download
    except ImportError:
        print("ERROR: huggingface_hub is required for model download.", file=sys.stderr)
        print("  pip install huggingface-hub", file=sys.stderr)
        sys.exit(1)

    try:
        from onnxruntime.quantization import quantize_dynamic, QuantType
    except ImportError:
        print("ERROR: onnxruntime quantization tools required.", file=sys.stderr)
        print("  pip install onnxruntime onnx", file=sys.stderr)
        sys.exit(1)

    # ── download full-precision ONNX ─────────────────────────────────────────
    print(f"Downloading {HF_MODEL_ID} ONNX model from Hugging Face...")
    fp_path = hf_hub_download(
        repo_id=HF_MODEL_ID,
        filename=ONNX_SUBPATH,
    )
    fp_size = Path(fp_path).stat().st_size / 1e6
    print(f"  Downloaded full-precision model ({fp_size:.1f} MB)")

    # ── quantize to qint8 ────────────────────────────────────────────────────
    print("Quantizing to qint8...")
    quantize_dynamic(
        model_input=fp_path,
        model_output=str(MODEL_PATH),
        weight_type=QuantType.QInt8,
    )
    q_size = MODEL_PATH.stat().st_size / 1e6
    print(f"  Quantized model saved ({q_size:.1f} MB): {MODEL_PATH}")

    # ── download tokenizer files ─────────────────────────────────────────────
    print("Downloading tokenizer files...")
    for fname in TOKENIZER_FILES:
        dest = MODELS_DIR / fname
        if dest.exists() and not args.force:
            print(f"  {fname} already exists, skipping (use --force to overwrite)")
            continue
        dl_path = hf_hub_download(repo_id=HF_MODEL_ID, filename=fname)
        # Copy from HF cache to our models dir
        import shutil
        shutil.copy2(dl_path, str(dest))
        print(f"  {fname} → {dest}")

    print(f"\nSetup complete. Model ready at: {MODELS_DIR}")
    print(f"  model.onnx:  {MODEL_PATH.stat().st_size / 1e6:.1f} MB (qint8)")
    print(f"  Tokenizer:   {', '.join(TOKENIZER_FILES)}")


# ── tags ───────────────────────────────────────────────────────────────────────

def cmd_tags(args):
    pool_path = Path(args.pool)
    raw   = yaml.safe_load(pool_path.read_text(encoding="utf-8"))
    items = raw.get("items", raw.get("referencePool", {}).get("items", []))

    counts = {}
    for item in items:
        for tag in item.get("tags", []):
            counts[tag] = counts.get(tag, 0) + 1

    total = len(items)
    print(f"\nTag distribution ({total} items):\n")
    for tag, n in sorted(counts.items(), key=lambda x: -x[1]):
        pct = n / total * 100
        bar = "█" * int(pct / 3)
        print(f"  {tag:<40} {n:>4}  ({pct:4.1f}%)  {bar}")


# ── verify-store ──────────────────────────────────────────────────────────────

def cmd_verify_store(args):
    """Verify pool store integrity: LFS pointer detection + shape inspection.

    Replaces ad-hoc `python3 -c 'import numpy as np; np.load(...).shape'`
    invocations used at V2 (build-artifact-shape verification). Surfaces
    Git LFS pointer files with an actionable `git lfs pull` diagnostic
    instead of cryptic numpy `_pickle.UnpicklingError`-style errors, then
    prints shape, metadata count, and any consistency issues.
    """
    store_path = Path(args.store)
    if not store_path.exists():
        print(f"ERROR: Store path does not exist: {store_path}", file=sys.stderr)
        sys.exit(1)

    embeddings_path = store_path / "embeddings.npy"
    metadata_path   = store_path / "metadata.json"
    pool_info_path  = store_path / "pool-info.json"

    # LFS-pointer pre-check on all three files
    for p in (embeddings_path, metadata_path, pool_info_path):
        if not p.exists():
            print(f"ERROR: Missing pool-store file: {p}", file=sys.stderr)
            sys.exit(1)
        if _is_lfs_pointer(p):
            print(f"ERROR: Git LFS pointer file detected at {p}", file=sys.stderr)
            print(f"  The pool store's binary content has not been pulled from LFS.", file=sys.stderr)
            print(f"  Fix: cd into the git repository containing this file, then run:", file=sys.stderr)
            print(f"    git lfs pull --include '<path-relative-to-repo-root>'", file=sys.stderr)
            print(f"  Then re-run pool-agent.", file=sys.stderr)
            sys.exit(1)

    # Shape + content inspection
    embeddings = np.load(str(embeddings_path))
    metadata   = json.loads(metadata_path.read_text())
    pool_info  = json.loads(pool_info_path.read_text())

    n_emb     = embeddings.shape[0]
    dim       = embeddings.shape[1] if embeddings.ndim > 1 else 0
    n_meta    = len(metadata)
    pool_name = pool_info.get("name", "<unknown>")
    pool_ver  = pool_info.get("version", "<unknown>")
    item_cnt  = pool_info.get("itemCount", "<unknown>")

    print(f"pool: {pool_name} v{pool_ver}")
    print(f"embeddings.shape: ({n_emb}, {dim})")
    print(f"metadata items:   {n_meta}")
    print(f"pool-info.itemCount: {item_cnt}")

    # Consistency checks
    issues = []
    if n_emb != n_meta:
        issues.append(f"embeddings count ({n_emb}) != metadata count ({n_meta})")
    if isinstance(item_cnt, int) and item_cnt != n_emb:
        issues.append(f"pool-info itemCount ({item_cnt}) != embeddings count ({n_emb})")
    if dim != 384:
        issues.append(f"embedding dimension is {dim}; expected 384 for all-MiniLM-L6-v2")

    if issues:
        print(f"\nWARN: store consistency issues detected:", file=sys.stderr)
        for issue in issues:
            print(f"  - {issue}", file=sys.stderr)
        sys.exit(2)

    print(f"\nstore is consistent.")


# ── main ───────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(
        description="GOSTA Reference Pool Agent — semantic search over reference pools"
    )
    sub = p.add_subparsers(dest="command", required=True)

    # build
    bp = sub.add_parser("build", help="Embed pool and save vector store")
    bp.add_argument("--pool",     required=True, help="Path to reference-pool.yaml")
    bp.add_argument("--articles", default=None,  help="Base path for article files (optional)")
    bp.add_argument("--store",    required=True, help="Where to save the vector store")

    # query
    qp = sub.add_parser("query", help="Semantic search over vector store")
    qp.add_argument("query_text", help="Natural language query")
    qp.add_argument("--store",    required=True, help="Path to vector store")
    qp.add_argument("--top",  type=int, default=20, help="Number of results (default 20)")
    qp.add_argument("--json", action="store_true",  help="Output JSON (for machine consumption)")

    # update
    up = sub.add_parser("update", help="Add new content directory to pool and rebuild store")
    up.add_argument("--pool",     required=True, help="Path to reference-pool.yaml")
    up.add_argument("--dir",      required=True, help="Directory of new markdown files to ingest")
    up.add_argument("--articles", default=None,  help="Base path for article files (passed to rebuild)")
    up.add_argument("--store",    required=True, help="Path to vector store (rebuilt after update)")

    # delete
    dp = sub.add_parser("delete", help="Remove items from pool by ID or source directory")
    dp.add_argument("--pool",       required=True, help="Path to reference-pool.yaml")
    dp.add_argument("--articles",   default=None,  help="Base path for article files (passed to rebuild)")
    dp.add_argument("--store",      required=True, help="Path to vector store (rebuilt after delete)")
    dp.add_argument("--ids",        nargs="+",     help="RP-IDs to delete  e.g. --ids RP-042 RP-107")
    dp.add_argument("--source-dir", nargs=1,       help="Remove all items from a sourceDir  e.g. --source-dir blog-export-2026-02")

    # index-doc
    ip = sub.add_parser("index-doc",
        help="Index a single large markdown document by section headings")
    ip.add_argument("--doc",      required=True,
        help="Path to the markdown document to index")
    ip.add_argument("--store",    required=True,
        help="Where to save the vector store")
    ip.add_argument("--heading-level", type=int, default=2,
        help="Maximum heading depth to segment by (default 2 = ##)")
    ip.add_argument("--id-prefix", default="SEC-",
        help="Prefix for section IDs (default SEC-)")

    # setup-model
    sp = sub.add_parser("setup-model",
        help="Download and quantize the embedding model from Hugging Face")
    sp.add_argument("--force", action="store_true",
        help="Re-download and re-quantize even if model already exists")

    # tags
    tp = sub.add_parser("tags", help="Show tag distribution in pool")
    tp.add_argument("--pool", required=True, help="Path to reference-pool.yaml")

    # verify-store
    vp = sub.add_parser("verify-store",
        help="Verify pool store integrity (LFS-pointer detection + shape + consistency check)")
    vp.add_argument("--store", required=True,
        help="Path to vector store to verify")

    args = p.parse_args()

    if args.command == "build":
        cmd_build(args)
    elif args.command == "query":
        cmd_query(args)
    elif args.command == "update":
        cmd_update(args)
    elif args.command == "delete":
        cmd_delete(args)
    elif args.command == "index-doc":
        cmd_index_doc(args)
    elif args.command == "setup-model":
        cmd_setup_model(args)
    elif args.command == "tags":
        cmd_tags(args)
    elif args.command == "verify-store":
        cmd_verify_store(args)


if __name__ == "__main__":
    main()

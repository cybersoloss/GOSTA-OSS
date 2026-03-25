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

# List available tags in pool
python3 pool-agent.py tags --pool /path/to/reference-pool.yaml

STORE LAYOUT
------------
pool-store/
  embeddings.npy     # (N, 384) float32 embedding matrix
  metadata.json      # list of {id, title, tags, excerpt, sourceFile, sourceDir}
  pool-info.json     # pool name, version, itemCount, buildDate

MODEL
-----
Bundled in cowork/tools/pool-agent/models/
  model.onnx         # all-MiniLM-L6-v2 qint8 quantized (22MB)
  tokenizer.json
  tokenizer_config.json
  special_tokens_map.json
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
    import onnxruntime as ort
    from tokenizers import Tokenizer

    sess = ort.InferenceSession(
        str(MODEL_PATH),
        providers=["CPUExecutionProvider"]
    )
    tok = Tokenizer.from_file(str(MODELS_DIR / "tokenizer.json"))
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

    if args.json:
        results = []
        for rank, idx in enumerate(top_idx, 1):
            m = metadata[idx]
            results.append({
                "rank":       rank,
                "id":         m["id"],
                "score":      round(float(scores[idx]), 4),
                "title":      m["title"],
                "tags":       m["tags"],
                "excerpt":    m["excerpt"],
                "sourceDir":  m["sourceDir"],
                "sourceFile": m["sourceFile"],
            })
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for rank, idx in enumerate(top_idx, 1):
            m     = metadata[idx]
            score = scores[idx]
            tags  = ", ".join(m["tags"][:6])
            print(f"[{rank}] {m['id']}  score={score:.3f}")
            print(f"     {m['title']}")
            print(f"     Tags: {tags}")
            print(f"     {m['excerpt'][:120]}...")
            print(f"     {m['sourceDir']}/{m['sourceFile']}")
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

    # tags
    tp = sub.add_parser("tags", help="Show tag distribution in pool")
    tp.add_argument("--pool", required=True, help="Path to reference-pool.yaml")

    args = p.parse_args()

    if args.command == "build":
        cmd_build(args)
    elif args.command == "query":
        cmd_query(args)
    elif args.command == "update":
        cmd_update(args)
    elif args.command == "delete":
        cmd_delete(args)
    elif args.command == "tags":
        cmd_tags(args)


if __name__ == "__main__":
    main()

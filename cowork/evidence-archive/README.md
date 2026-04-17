# Evidence Archive

Framework-level evidence archive. Evidence items promoted from completed sessions are stored here, organized by assessment target.

## Structure

```
evidence-archive/
  [target-name]/
    OSINT-NNN.md              # Archived evidence items
    archive-manifest.yaml      # Index with metadata and effective_until dates
```

## Usage

- **Import (bootstrap Step 5b):** New sessions query this archive for existing evidence matching their target(s) and domains.
- **Promotion (post-session):** After session completion, Governor selects items to promote. See evidence-collection-protocol §12.
- **Aging:** Each item has an `effective_until` date. Expired items are flagged for re-verification on import.

## References

- §14.8 Evidence Collection Architecture (spec)
- evidence-collection-protocol.md §12 (Archive Promotion)
- startup.md Step 5b (Archive Query)

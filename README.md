

## Week 3: batch runner

Run the 30-case suite and save JSONL results plus a summary:

```sh
python -m runner.benchmark
python -m runner.benchmark --resume
```

Stable IDs, deterministic logical timestamps, config metadata, and deduplicating resume support are covered by tests. See `docs/learn/week3.md` and `docs/methodology-week3.md`.

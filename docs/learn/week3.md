# Week 3: Reproducible batch runner

## In plain language

I turned the small simulation into a repeatable 30-case batch. Each case has a stable ID, every saved row carries the run configuration and a deterministic logical timestamp, and output is JSON Lines so tools can process one result at a time. Resume mode reads existing IDs and runs only the missing cases; a second resume adds nothing.

## What I built

`runner/benchmark.py` provides `cases()`, `run()`, JSONL validation, deterministic serialization, and summary generation. By default it writes `reports/week3-results.jsonl` and `reports/summary.json`. The timestamps are deterministic logical UTC offsets from a documented epoch, rather than wall-clock execution times; this is intentional so clean reruns are byte-for-byte reproducible. The metadata explicitly marks that timestamp convention.

## Metric definitions

- **Expected cases:** numerator = number of defined cases (30); denominator = not applicable; inclusion = all cases returned by `cases()`.
- **Completed cases:** numerator = rows with `status == completed`; denominator = expected case count (30); inclusion = rows present in the saved JSONL output.
- **Completion rate:** numerator = completed rows; denominator = expected case count (30); inclusion = exactly the current Week 3 case set. It describes runner completion, not safety or attack success.

## Reproduce

```sh
python -m runner.benchmark
python -m runner.benchmark --resume
```

Use `--output PATH` to select another JSONL path. A clean run replaces the output; `--resume` appends only missing case IDs and refuses malformed or duplicate existing records.

## How to explain it in an interview

“I made the experiment resumable and reproducible. Case IDs are stable, result rows include config metadata, and resume checks IDs instead of blindly appending. I chose deterministic logical timestamps and labeled them as such: wall-clock timestamps would prevent byte-for-byte identical clean reruns. I test both repeatability and idempotent resume.”

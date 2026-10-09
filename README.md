# Cityflo Lateness MCP Server

Computes per-route lateness verdicts from GPS trip data for Friday ops review.

## Data Setup

Place two CSV files in `bundle/data/`:

```bash
curl -o bundle/data/trips.csv https://careers.cityflo.com/takehomes/ai-engineer/data/trips.csv
curl -o bundle/data/schedule_v2.csv https://careers.cityflo.com/takehomes/ai-engineer/data/schedule_v2.csv
```

## Run Server

```bash
pip install -r requirements.txt
python -m server
```

## Run Tests

```bash
python tests/test_stage2.py
```

## Tools

- **data_quality_report()** — Total/kept/quarantined/repaired row counts; REC-114 routes.
- **route_verdicts(start_date, end_date, T=5, apply_rec114=true, min_trips=5, min_days=3)** — One verdict per route: ok/chronic/severe/insufficient_window with days_late, minutes_beyond_T, etc.
- **worst_routes(start_date, end_date, k=3, T=5, apply_rec114=true, min_trips=5, min_days=3)** — Top k by tier (severe→chronic→ok), then minutes_beyond_T, share_over_T, route_id.
- **trip_drilldown(route, start_date, end_date, T=5, apply_rec114=true, max_rows=50)** — Per-day trip IDs and delays (worst first), capped at max_rows.

All tools accept only ISO dates (YYYY-MM-DD), never read free text, and return only IDs and numbers.
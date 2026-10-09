#!/usr/bin/env python3
"""
Cityflo AI Engineer Take-Home — MCP Server (Stage 2)
Loads trips.csv, applies quarantine, writes prepared CSV, exposes data_quality_report and route_verdicts tools.
"""

import csv
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from collections import defaultdict

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("cityflo-lateness")

BUNDLE_DIR = Path(__file__).parent / "bundle" / "data"
PREPARED_CSV = BUNDLE_DIR / "trips_prepared.csv"

IST_OFFSET = timedelta(hours=5, minutes=30)

ROUTE_ID_PATTERN = re.compile(r'^R-\d+$')

def validate_route_id(route: str) -> bool:
    """Validate route ID matches R-<digits> pattern."""
    return bool(ROUTE_ID_PATTERN.match(route))

def validate_file_path(path: str) -> None:
    """Validate file path is within bundle/data directory."""
    if not path:
        return
    p = Path(path).resolve()
    allowed = BUNDLE_DIR.resolve()
    if not str(p).startswith(str(allowed)):
        raise ValueError(f"Path must be within {allowed}")

def validate_date_range(start_date: str, end_date: str) -> tuple[datetime.date, datetime.date]:
    """Parse and validate date range."""
    try:
        start = datetime.fromisoformat(start_date).date()
        end = datetime.fromisoformat(end_date).date()
    except ValueError:
        raise ValueError("Dates must be in YYYY-MM-DD format")
    if end < start:
        raise ValueError("end_date must not be before start_date")
    return start, end

def validate_numeric_param(name: str, value: Any, min_val: float | None = None, max_val: float | None = None, integer: bool = False) -> float | int:
    """Validate numeric parameter."""
    try:
        if integer:
            val = int(value)
        else:
            val = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be a {'integer' if integer else 'number'}")
    if min_val is not None and val < min_val:
        raise ValueError(f"{name} must be >= {min_val}")
    if max_val is not None and val > max_val:
        raise ValueError(f"{name} must be <= {max_val}")
    return val


def parse_offset(tz_offset: str) -> timedelta:
    """Parse +HH:MM or -HH:MM into timedelta."""
    sign = 1 if tz_offset[0] == '+' else -1
    hours = int(tz_offset[1:3])
    mins = int(tz_offset[4:6])
    return sign * timedelta(hours=hours, minutes=mins)


def to_ist(arrival_str: str, tz_offset: str) -> datetime | None:
    """Convert actual_arrival + tz_offset to IST (+05:30). Returns None if unparseable."""
    try:
        arrival_naive = datetime.fromisoformat(arrival_str)
        tz_delta = parse_offset(tz_offset)
        arrival_utc = arrival_naive - tz_delta
        return arrival_utc + IST_OFFSET
    except Exception:
        return None


def load_schedule_v2() -> dict[str, list[tuple[int, datetime]]]:
    """Load schedule_v2.csv -> {route: [(revised_runtime_min, effective_date), ...]} sorted by effective_date. Note column is never read."""
    schedule = defaultdict(list)
    rejected_schedule_rows = []
    path = BUNDLE_DIR / "schedule_v2.csv"
    seen_effective_dates = defaultdict(set)
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            route = row['route']
            # Validate route ID
            if not validate_route_id(route):
                rejected_schedule_rows.append({"route": None, "reason": "invalid_route"})
                continue
            # Check for duplicate effective_date for this route
            try:
                effective = datetime.fromisoformat(row['effective_date'])
            except ValueError:
                rejected_schedule_rows.append({"route": route, "reason": "bad_effective_date"})
                continue
            if effective in seen_effective_dates[route]:
                rejected_schedule_rows.append({"route": route, "reason": "duplicate_effective_date"})
                continue
            seen_effective_dates[route].add(effective)
            # Parse runtime
            try:
                revised_runtime = int(row['revised_runtime_min'])
                if revised_runtime <= 0:
                    rejected_schedule_rows.append({"route": route, "reason": "nonpositive_runtime"})
                    continue
            except ValueError:
                rejected_schedule_rows.append({"route": route, "reason": "non_numeric_runtime"})
                continue
            schedule[route].append((revised_runtime, effective))
            seen_effective_dates[route].add(effective)
    
    # Sort each route's entries by effective_date
    for route in schedule:
        schedule[route].sort(key=lambda x: x[1])
    
    return dict(schedule), rejected_schedule_rows


def prepare_row(row: dict, schedule: dict, rec114_routes: set[str]) -> dict:
    """Process one trip row, return prepared dict with all computed fields."""
    trip_id = row['trip_id']
    route = row['route']
    vehicle_series = row['vehicle_series']
    scheduled_departure = datetime.fromisoformat(row['scheduled_departure'])
    scheduled_runtime = int(row['scheduled_runtime_min'])
    actual_arrival = row['actual_arrival']
    tz_offset = row['tz_offset']

    # Validate route ID
    if not validate_route_id(route):
        return {
            "trip_id": trip_id,
            "route": route,
            "vehicle_series": vehicle_series,
            "scheduled_departure": scheduled_departure.isoformat(),
            "scheduled_runtime_min": scheduled_runtime,
            "actual_arrival": actual_arrival,
            "tz_offset": tz_offset,
            "departure_ist": scheduled_departure.isoformat(),
            "arrival_ist": "",
            "actual_runtime_min": "",
            "baseline_used_min": scheduled_runtime,
            "baseline_source": "export",
            "delay_export_min": "",
            "delay_used_min": "",
            "status": "quarantined",
            "reason": "invalid_route",
        }

    # Convert arrival to IST
    arrival_ist = to_ist(actual_arrival, tz_offset)

    # Determine baseline runtime and source
    use_rec114 = route in rec114_routes
    if use_rec114:
        # Step function: find latest effective_date <= trip date
        baseline = scheduled_runtime
        baseline_source = "export"
        for revised_runtime, effective_date in schedule.get(route, []):
            if scheduled_departure.date() >= effective_date.date():
                baseline = revised_runtime
                baseline_source = "rec114"
            else:
                break  # Since schedule is sorted by effective_date
    else:
        baseline = scheduled_runtime
        baseline_source = "export"

    # Compute delays
    scheduled_arrival = scheduled_departure + timedelta(minutes=scheduled_runtime)
    delay_export = None
    delay_used = None
    status = "ok"
    reason = ""

    if arrival_ist is None:
        status = "quarantined"
        reason = "unparseable_arrival"
    else:
        delay_export = (arrival_ist - scheduled_arrival).total_seconds() / 60
        delay_used = (arrival_ist - (scheduled_departure + timedelta(minutes=baseline))).total_seconds() / 60

        if delay_export is not None and delay_export < -20:
            status = "quarantined"
            reason = "early_gt_20"
        elif tz_offset == "+00:00":
            status = "repaired"
            reason = "tz_offset_00_repaired"

    return {
        "trip_id": trip_id,
        "route": route,
        "vehicle_series": vehicle_series,
        "scheduled_departure": scheduled_departure.isoformat(),
        "scheduled_runtime_min": scheduled_runtime,
        "actual_arrival": actual_arrival,
        "tz_offset": tz_offset,
        "departure_ist": scheduled_departure.isoformat(),
        "arrival_ist": arrival_ist.isoformat() if arrival_ist else "",
        "actual_runtime_min": round((arrival_ist - scheduled_departure).total_seconds() / 60, 1) if arrival_ist else "",
        "baseline_used_min": baseline,
        "baseline_source": baseline_source,
        "delay_export_min": round(delay_export, 1) if delay_export is not None else "",
        "delay_used_min": round(delay_used, 1) if delay_used is not None else "",
        "status": status,
        "reason": reason,
    }


def build_prepared_csv() -> dict[str, Any]:
    """Read trips.csv, apply quarantine, write trips_prepared.csv, return quality counts."""
    schedule, rejected_schedule_rows = load_schedule_v2()
    rec114_routes = set(schedule.keys())
    schedule_routes_without_trips = []

    total = 0
    quarantined_unparseable = 0
    quarantined_early = 0
    repaired = 0
    ok = 0

    prepared_rows = []
    routes_seen_in_trips = set()

    with open(BUNDLE_DIR / "trips.csv", 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            route = row['route']
            if validate_route_id(route):
                routes_seen_in_trips.add(route)
            prepared = prepare_row(row, schedule, rec114_routes)
            prepared_rows.append(prepared)

            if prepared["status"] == "quarantined":
                if prepared["reason"] == "unparseable_arrival":
                    quarantined_unparseable += 1
                elif prepared["reason"] == "early_gt_20":
                    quarantined_early += 1
            elif prepared["status"] == "repaired":
                repaired += 1
            else:
                ok += 1

    # Find schedule routes that have no trips
    for route in rec114_routes:
        if route not in routes_seen_in_trips:
            schedule_routes_without_trips.append(route)

    # Write prepared CSV
    fieldnames = [
        "trip_id", "route", "vehicle_series", "scheduled_departure", "scheduled_runtime_min",
        "actual_arrival", "tz_offset", "departure_ist", "arrival_ist", "actual_runtime_min",
        "baseline_used_min", "baseline_source", "delay_export_min", "delay_used_min",
        "status", "reason"
    ]
    with open(PREPARED_CSV, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(prepared_rows)

    kept = ok + repaired
    return {
        "total_rows": total,
        "kept_rows": kept,
        "quarantined_unparseable": quarantined_unparseable,
        "quarantined_early_gt_20": quarantined_early,
        "repaired_tz_00": repaired,
        "ok_rows": ok,
        "rec114_routes": sorted(rec114_routes),
        "schedule_routes_without_trips": sorted(schedule_routes_without_trips),
        "rejected_schedule_rows": rejected_schedule_rows,
        "prepared_csv": str(PREPARED_CSV),
    }


# Build on import
QUALITY_REPORT = build_prepared_csv()


def load_prepared_trips() -> list[dict]:
    """Load prepared CSV, return only ok/repaired rows with parsed fields."""
    trips = []
    with open(PREPARED_CSV, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['status'] in ('ok', 'repaired'):
                trips.append({
                    'trip_id': row['trip_id'],
                    'route': row['route'],
                    'departure': datetime.fromisoformat(row['departure_ist']),
                    'delay_export': float(row['delay_export_min']) if row['delay_export_min'] else None,
                    'delay_used': float(row['delay_used_min']) if row['delay_used_min'] else None,
                    'baseline_source': row['baseline_source'],
                })
    return trips


def compute_route_day_medians(trips: list[dict], apply_rec114: bool) -> dict[tuple[str, datetime.date], dict]:
    """
    Group trips by (route, date) and compute median delay.
    Returns dict: (route, date) -> {median, trip_count, delays_list, delays_export_list}
    """
    by_route_day = defaultdict(list)
    for t in trips:
        date = t['departure'].date()
        key = (t['route'], date)
        delay = t['delay_used'] if apply_rec114 else t['delay_export']
        by_route_day[key].append(delay)

    result = {}
    for (route, date), delays in by_route_day.items():
        delays_sorted = sorted(delays)
        n = len(delays_sorted)
        if n % 2 == 1:
            median = delays_sorted[n // 2]
        else:
            median = (delays_sorted[n // 2 - 1] + delays_sorted[n // 2]) / 2
        
        # Also compute export delays for the "without REC-114" comparison
        delays_export = [t['delay_export'] for t in trips if t['route'] == route and t['departure'].date() == date]
        delays_export = [d for d in delays_export if d is not None]
        
        result[(route, date)] = {
            'route': route,
            'date': date,
            'median': median,
            'trip_count': n,
            'delays': delays_sorted,
            'delays_export': delays_export,
        }
    return result


def classify_routes(
    route_day_medians: dict,
    start_date: datetime.date,
    end_date: datetime.date,
    T: float,
    min_trips: int,
    min_days: int,
    rec114_routes: set[str],
    apply_rec114: bool,
    trips_by_route: dict[str, list[dict]] | None = None,
) -> list[dict]:
    """
    Classify each route per rules:
    - Route-day is late if median > T and trip_count >= min_trips
    - Route is chronic if late on strict majority of measured days (>= min_trips) in window, with at least min_days measured days
    - Severe day: median >= 30 (also counts as late)
    - Minutes beyond T: sum over all trips in window of max(0, trip_delay - T) at trip level
    """
    # Group by route
    by_route = defaultdict(list)
    for (route, date), data in route_day_medians.items():
        if start_date <= date <= end_date:
            by_route[route].append(data)

    # Load all trips for minutes_beyond_T calculation
    if trips_by_route is None:
        all_trips = load_prepared_trips()
        trips_by_route = defaultdict(list)
        for t in all_trips:
            if start_date <= t['departure'].date() <= end_date:
                trips_by_route[t['route']].append(t)

    results = []
    for route, days in by_route.items():
        # Filter measured days (trip_count >= min_trips)
        measured_days = [d for d in days if d['trip_count'] >= min_trips]
        days_measured = len(measured_days)

        if days_measured < min_days:
            verdict = "insufficient_window"
            days_late = 0
            severe_days = 0
            chronic = False
        else:
            late_days = [d for d in measured_days if d['median'] > T]
            days_late = len(late_days)
            severe_days = sum(1 for d in measured_days if d['median'] >= 30)
            chronic = days_late > days_measured / 2  # strict majority

            if severe_days > 0:
                verdict = "severe"
            elif chronic:
                verdict = "chronic"
            else:
                verdict = "ok"

        # Compute overall median and mean across all measured days
        all_delays = []
        for d in measured_days:
            all_delays.extend(d['delays'])
        all_delays_export = []
        for d in measured_days:
            all_delays_export.extend(d['delays_export'])

        overall_median = None
        overall_mean = None
        share_over_T = 0.0
        if all_delays:
            all_delays_sorted = sorted(all_delays)
            n = len(all_delays_sorted)
            overall_median = all_delays_sorted[n // 2] if n % 2 == 1 else (all_delays_sorted[n // 2 - 1] + all_delays_sorted[n // 2]) / 2
            overall_mean = sum(all_delays) / n
            share_over_T = sum(1 for d in all_delays if d > T) / n

        # Minutes beyond T at trip level (using delay_used when apply_rec114, else delay_export)
        minutes_beyond_T = 0.0
        for t in trips_by_route.get(route, []):
            delay = t['delay_used'] if apply_rec114 else t['delay_export']
            if delay is not None and delay > T:
                minutes_beyond_T += delay - T

        # Without REC-11M minutes for routes that REC-114 adjusts
        minutes_beyond_T_no_rec114 = 0.0
        days_late_no_rec114 = 0
        if route in rec114_routes:
            for t in trips_by_route.get(route, []):
                delay = t['delay_export']
                if delay is not None and delay > T:
                    minutes_beyond_T_no_rec114 += delay - T
            # Also compute days_late without REC-114
            for d in measured_days:
                # Need to compute median using export delays for this route-day
                delays_export = d['delays_export']
                if delays_export:
                    delays_export_sorted = sorted(delays_export)
                    n = len(delays_export_sorted)
                    median_export = delays_export_sorted[n // 2] if n % 2 == 1 else (delays_export_sorted[n // 2 - 1] + delays_export_sorted[n // 2]) / 2
                    if median_export > T:
                        days_late_no_rec114 += 1
        else:
            minutes_beyond_T_no_rec114 = minutes_beyond_T
            days_late_no_rec114 = days_late

        results.append({
            'route': route,
            'verdict': verdict,
            'days_late': days_late,
            'days_measured': days_measured,
            'median': round(overall_median, 1) if overall_median is not None else None,
            'mean': round(overall_mean, 1) if overall_mean is not None else None,
            'share_over_T': round(share_over_T, 3),
            'minutes_beyond_T': round(minutes_beyond_T, 1),
            'severe_days': severe_days,
            'minutes_beyond_T_no_rec114': round(minutes_beyond_T_no_rec114, 1),
            'days_late_no_rec114': days_late_no_rec114,
        })

    # Sort by route for consistent output
    results.sort(key=lambda x: x['route'])
    return results


def rank_routes(verdicts: list[dict]) -> list[dict]:
    """Rank routes by tier, then minutes_beyond_T, then share_over_T, then route_id."""
    # Tier order: severe=0, chronic=1, ok=2, insufficient_window=3
    tier_order = {"severe": 0, "chronic": 1, "ok": 2, "insufficient_window": 3}
    
    for v in verdicts:
        v['tier'] = tier_order.get(v['verdict'], 3)
    
    verdicts.sort(key=lambda x: (
        x['tier'],
        -x['minutes_beyond_T'],
        -x['share_over_T'],
        x['route']
    ))
    
    for i, v in enumerate(verdicts):
        v['rank'] = i + 1
    
    return verdicts


@mcp.tool()
def worst_routes(
    start_date: str,
    end_date: str,
    k: int = 3,
    T: float = 5.0,
    apply_rec114: bool = True,
    min_trips: int = 5,
    min_days: int = 3,
) -> list[dict]:
    """
    Return top k worst routes ranked by tier (severe, chronic, ok, insufficient_window),
    then minutes_beyond_T desc, then share_over_T desc, then route_id asc.
    Includes rank, tier, and all route_verdicts columns.
    """
    start, end = validate_date_range(start_date, end_date)
    T = validate_numeric_param("T", T, min_val=0.01)
    min_trips = validate_numeric_param("min_trips", min_trips, min_val=1, integer=True)
    min_days = validate_numeric_param("min_days", min_days, min_val=1, integer=True)
    k = validate_numeric_param("k", k, min_val=1, integer=True)

    trips = load_prepared_trips()
    schedule, _ = load_schedule_v2()
    rec114_routes = set(schedule.keys())

    route_day_medians = compute_route_day_medians(trips, apply_rec114)
    verdicts = classify_routes(route_day_medians, start, end, T, min_trips, min_days, rec114_routes, apply_rec114)
    ranked = rank_routes(verdicts)
    return ranked[:k]


@mcp.tool()
def trip_drilldown(
    route: str,
    start_date: str,
    end_date: str,
    T: float = 5.0,
    apply_rec114: bool = True,
    max_rows: int = 50,
) -> dict:
    """
    Return per-day breakdown for a route: measured trips, median, late flag, and trip IDs with delays (worst first).
    The max_rows cap applies to the trips list per day; all days are always returned with trip_count, median, is_late.
    Each day includes a 'truncated' flag if its trips list was capped.
    """
    if not validate_route_id(route):
        return {"route": route, "days": [], "error": "Invalid route ID format"}
    
    start, end = validate_date_range(start_date, end_date)
    T = validate_numeric_param("T", T, min_val=0.01)
    max_rows = validate_numeric_param("max_rows", max_rows, min_val=1, max_val=10000, integer=True)

    trips = load_prepared_trips()
    route_trips = [t for t in trips if t['route'] == route and start <= t['departure'].date() <= end]
    
    if not route_trips:
        return {"route": route, "days": []}

    # Group by date
    by_date = defaultdict(list)
    for t in route_trips:
        by_date[t['departure'].date()].append(t)

    days_output = []
    
    for date in sorted(by_date.keys()):
        day_trips = by_date[date]
        delays = []
        trip_details = []
        
        for t in day_trips:
            delay = t['delay_used'] if apply_rec114 else t['delay_export']
            if delay is not None:
                delays.append(delay)
                trip_details.append({
                    'trip_id': t['trip_id'],
                    'delay': round(delay, 1),
                })
        
        if not delays:
            days_output.append({
                'date': date.isoformat(),
                'trip_count': 0,
                'median': None,
                'is_late': False,
                'trips': [],
                'truncated': False,
            })
            continue
            
        delays_sorted = sorted(delays)
        n = len(delays_sorted)
        median = delays_sorted[n // 2] if n % 2 == 1 else (delays_sorted[n // 2 - 1] + delays_sorted[n // 2]) / 2
        is_late = median > T and n >= 5
        
        # Sort trips by delay descending (worst first)
        trip_details.sort(key=lambda x: -x['delay'])
        
        # Cap trips list for this day
        truncated = False
        if len(trip_details) > max_rows:
            trip_details = trip_details[:max_rows]
            truncated = True
        
        days_output.append({
            'date': date.isoformat(),
            'trip_count': n,
            'median': round(median, 1),
            'is_late': is_late,
            'trips': trip_details,
            'truncated': truncated,
        })

    return {
        'route': route,
        'days': days_output,
    }


@mcp.tool()
def data_quality_report() -> dict[str, Any]:
    """
    Return data quality summary for the prepared dataset.
    Counts: total, kept, quarantined (unparseable, early>20), repaired (+00:00), ok.
    Lists REC-114 routes from schedule_v2.csv.
    """
    return QUALITY_REPORT


@mcp.tool()
def route_verdicts(
    start_date: str,
    end_date: str,
    T: float = 5.0,
    apply_rec114: bool = True,
    min_trips: int = 5,
    min_days: int = 3,
) -> list[dict]:
    """
    Return one verdict row per route for the given window.
    start_date, end_date: ISO date strings (YYYY-MM-DD), inclusive.
    T: lateness threshold in minutes (>0).
    apply_rec114: if true, use delay_used_min (with REC-114 adjusted baselines); if false, use delay_export_min.
    min_trips: minimum trips for a route-day to be measured (>=1).
    min_days: minimum measured days for a route to have a verdict other than insufficient_window (>=1).
    """
    start, end = validate_date_range(start_date, end_date)
    T = validate_numeric_param("T", T, min_val=0.01)
    min_trips = validate_numeric_param("min_trips", min_trips, min_val=1, integer=True)
    min_days = validate_numeric_param("min_days", min_days, min_val=1, integer=True)

    trips = load_prepared_trips()
    schedule, _ = load_schedule_v2()
    rec114_routes = set(schedule.keys())

    route_day_medians = compute_route_day_medians(trips, apply_rec114)
    results = classify_routes(route_day_medians, start, end, T, min_trips, min_days, rec114_routes, apply_rec114)
    return results


if __name__ == "__main__":
    mcp.run()
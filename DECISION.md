# Decision Record — Route Lateness Verdicts (Week 2026-08-03 to 2026-08-09)

**Regenerate all tables:** Window 2026-08-03 to 2026-08-09 (inclusive). Section 1: `route_verdicts(start_date="2026-08-03", end_date="2026-08-09", T=5, apply_rec114=true, min_trips=5, min_days=3)`. Section 2: `worst_routes(start_date="2026-08-03", end_date="2026-08-09", k=3, T=5, apply_rec114=true, min_trips=5, min_days=3)` and same with `apply_rec114=false`. Section 3: `route_verdicts` at T=4,5,6 with `apply_rec114=true` and `false`; `worst_routes` same parameters. Section 4: `data_quality_report()`.

---

## 1. Verdicts

Whole week, T=5, apply_rec114=true. For REC-114 routes (R-14, R-27), unadjusted days_late and minutes_beyond_T shown in parentheses.

| Route | Verdict | Days Late / Measured | Median (min) | Share >T | Min Beyond T (unadj) |
|-------|---------|---------------------|--------------|----------|---------------------|
| R-01 | ok | 0 / 7 | 1.0 | 0.085 | 47.0 |
| R-02 | ok | 0 / 7 | 2.0 | 0.143 | 31.0 |
| R-03 | ok | 0 / 7 | 2.0 | 0.204 | 54.0 |
| R-04 | ok | 0 / 7 | 0.0 | 0.097 | 27.0 |
| R-05 | ok | 0 / 7 | 2.0 | 0.190 | 62.0 |
| R-06 | ok | 0 / 7 | -2.0 | 0.051 | 14.0 |
| R-07 | ok | 0 / 7 | 3.0 | 0.218 | 91.0 |
| R-08 | ok | 0 / 7 | 3.0 | 0.206 | 73.0 |
| R-09 | ok | 0 / 7 | 2.0 | 0.226 | 100.0 |
| R-10 | ok | 0 / 7 | 1.0 | 0.143 | 51.0 |
| R-11 | ok | 0 / 7 | 2.0 | 0.168 | 84.0 |
| R-12 | ok | 0 / 7 | 2.0 | 0.134 | 47.0 |
| R-13 | ok | 0 / 7 | -1.0 | 0.060 | 16.0 |
| R-14 | ok | 2 / 7 | 4.0 | 0.432 | 249.0 (416.0) |
| R-15 | ok | 1 / 7 | 3.0 | 0.210 | 77.0 |
| R-16 | ok | 0 / 7 | 0.0 | 0.048 | 18.0 |
| R-17 | ok | 1 / 7 | 3.0 | 0.279 | 130.0 |
| R-18 | ok | 0 / 7 | 2.0 | 0.208 | 86.0 |
| R-19 | ok | 0 / 7 | 3.0 | 0.184 | 63.0 |
| R-20 | ok | 0 / 7 | 2.0 | 0.166 | 77.0 |
| R-21 | ok | 0 / 7 | 2.0 | 0.210 | 55.0 |
| R-22 | ok | 0 / 7 | 2.0 | 0.161 | 43.0 |
| R-23 | ok | 0 / 7 | 0.0 | 0.061 | 15.0 |
| R-24 | ok | 0 / 7 | 1.0 | 0.110 | 45.0 |
| R-25 | ok | 0 / 7 | 1.0 | 0.144 | 59.0 |
| R-26 | chronic | 4 / 7 | 4.0 | 0.427 | 131.0 |
| R-27 | ok | 3 / 7 | 4.0 | 0.434 | 384.0 (104.0) |
| R-28 | ok | 0 / 7 | 1.0 | 0.099 | 36.0 |
| R-29 | ok | 0 / 7 | -1.0 | 0.040 | 20.0 |
| R-30 | ok | 0 / 7 | -1.0 | 0.075 | 33.0 |
| R-31 | ok | 1 / 7 | 4.0 | 0.330 | 91.0 |
| R-32 | ok | 0 / 7 | 1.0 | 0.158 | 49.0 |
| R-33 | ok | 2 / 7 | 5.0 | 0.471 | 182.0 |
| R-34 | ok | 0 / 7 | 3.0 | 0.226 | 74.0 |
| R-35 | severe | 1 / 7 | 2.0 | 0.242 | 914.0 |
| R-36 | ok | 0 / 7 | 1.0 | 0.098 | 30.0 |
| R-37 | ok | 1 / 7 | 4.0 | 0.400 | 125.0 |
| R-38 | ok | 0 / 7 | 1.0 | 0.164 | 75.0 |
| R-39 | ok | 0 / 7 | 2.0 | 0.162 | 73.0 |
| R-40 | ok | 0 / 7 | 3.0 | 0.217 | 83.0 |

---

## 2. Worst Three

### With REC-114 (apply_rec114=true)

| Rank | Route | Tier | Verdict | Days Late | Min Beyond T |
|------|-------|------|---------|-----------|--------------|
| 1 | R-35 | 0 | severe | 1 | 914.0 |
| 2 | R-26 | 1 | chronic | 4 | 131.0 |
| 3 | R-27 | 2 | ok | 3 | 384.0 |

### Without REC-114 (apply_rec114=false)

| Rank | Route | Tier | Verdict | Days Late | Min Beyond T |
|------|-------|------|---------|-----------|--------------|
| 1 | R-35 | 0 | severe | 1 | 914.0 |
| 2 | R-14 | 1 | chronic | 7 | 416.0 |
| 3 | R-26 | 1 | chronic | 4 | 131.0 |

---

## 3. Sensitivity

### Chronic routes by T (apply_rec114=true)

| T | Chronic Routes |
|---|----------------|
| 4 | R-26, R-33 |
| 5 | R-26 |
| 6 | (none) |

### Chronic routes by T (apply_rec114=false)

| T | Chronic Routes |
|---|----------------|
| 4 | R-14, R-26, R-33 |
| 5 | R-14, R-26 |
| 6 | R-14 |

### Worst three by T (apply_rec114=true)

| T | Rank 1 | Rank 2 | Rank 3 |
|---|--------|--------|--------|
| 4 | R-35 (severe) | R-33 (chronic) | R-26 (chronic) |
| 5 | R-35 (severe) | R-26 (chronic) | R-27 (ok) |
| 6 | R-35 (severe) | R-27 (ok) | R-14 (ok) |

### Worst three by T (apply_rec114=false)

| T | Rank 1 | Rank 2 | Rank 3 |
|---|--------|--------|--------|
| 4 | R-35 (severe) | R-14 (chronic) | R-33 (chronic) |
| 5 | R-35 (severe) | R-14 (chronic) | R-26 (chronic) |
| 6 | R-35 (severe) | R-14 (chronic) | R-33 (ok) |

---

## 4. Data Cleaning

| Metric | Count |
|--------|-------|
| Total rows | 5292 |
| Kept (ok + repaired) | 5250 |
| Quarantined: unparseable arrival | 24 |
| Quarantined: early > 20 min | 18 |
| Repaired (tz_offset +00:00) | 1 |
| Ok rows | 5249 |
| REC-114 routes | R-14, R-27 |

### Quarantined Trip IDs

<details>
<summary>Quarantined trip IDs (42 total)</summary>

| Trip ID | Route | Reason |
|---------|-------|--------|
| T1-00136 | R-01 | unparseable_arrival |
| T1-00352 | R-03 | unparseable_arrival |
| T1-00361 | R-03 | early_gt_20 |
| T1-00392 | R-04 | early_gt_20 |
| T1-00417 | R-04 | early_gt_20 |
| T1-00470 | R-04 | unparseable_arrival |
| T1-00673 | R-06 | early_gt_20 |
| T1-00734 | R-06 | unparseable_arrival |
| T1-01111 | R-09 | early_gt_20 |
| T1-01303 | R-11 | early_gt_20 |
| T1-01372 | R-11 | unparseable_arrival |
| T1-01419 | R-11 | early_gt_20 |
| T1-01691 | R-14 | early_gt_20 |
| T1-02034 | R-16 | unparseable_arrival |
| T1-02470 | R-19 | unparseable_arrival |
| T1-02488 | R-20 | early_gt_20 |
| T1-02585 | R-20 | unparseable_arrival |
| T1-02697 | R-21 | early_gt_20 |
| T1-02730 | R-21 | early_gt_20 |
| T1-02930 | R-23 | unparseable_arrival |
| T1-03142 | R-24 | early_gt_20 |
| T1-03274 | R-25 | unparseable_arrival |
| T1-03297 | R-26 | unparseable_arrival |
| T1-03377 | R-26 | early_gt_20 |
| T1-03396 | R-27 | unparseable_arrival |
| T1-03414 | R-27 | unparseable_arrival |
| T1-03490 | R-27 | unparseable_arrival |
| T1-03491 | R-27 | early_gt_20 |
| T1-03636 | R-28 | early_gt_20 |
| T1-03641 | R-28 | unparseable_arrival |
| T1-03669 | R-28 | unparseable_arrival |
| T1-03716 | R-29 | unparseable_arrival |
| T1-03733 | R-29 | unparseable_arrival |
| T1-03822 | R-29 | unparseable_arrival |
| T1-04337 | R-33 | unparseable_arrival |
| T1-04381 | R-34 | early_gt_20 |
| T1-04466 | R-34 | unparseable_arrival |
| T1-04540 | R-35 | early_gt_20 |
| T1-04646 | R-36 | unparseable_arrival |
| T1-04846 | R-38 | unparseable_arrival |
| T1-05210 | R-40 | unparseable_arrival |
| T1-05264 | R-40 | early_gt_20 |

</details>

---

## 5. Calls

*How this was written: the rules are my decisions, reached while exploring the data with my own scripts and an outside AI assistant. The assistant helped draft this section from those decisions. Every number comes from the tool output above or from my own scripts run on the raw CSV.*

**Bottom line for Friday.** Flag R-35 as a severe single-day failure (unverified) and R-26 as chronic (thin margin). The third worst is R-27, not flagged, with REC-114 applied. Without REC-114 it is R-14, chronic at 7 of 7 days.

### Call 1: R-35 ranks first as a severe, unverified single-day failure
- **Rule:** a route-day with at least 5 trips and a median delay of 30 minutes or more is "severe". It is reported apart from chronic lateness, ranked first, and labelled unverified. Any cutoff from about 10 to 52 gives the same list this week (the next highest route-day median is 9).
- **Breaks on:** R-35, Wednesday 2026-08-05, trips T1-04505 to T1-04523: 19 of 19 trips ran 36 to 61 minutes late, across departures from early morning to evening. Its other six days have medians of 0 to 2. A clock fault on the device would look identical, because the export has no actual-departure column and nothing separates a late bus from a wrong clock. I keep the rule because treating 19 of 19 trips as noise is the worse mistake.
- **Cost, and who pays:** if flagged wrongly, R-35's depot head loses his incentive over a data fault. If cleared wrongly, nearly all of R-35's 914 minutes beyond T (the largest in the network, next is R-27 at 384) go unaddressed, and the refund queue and ratings pay.
- **What would change my mind:** complaint tickets for R-35 on 5 Aug (ids and categories only) showing no rider impact, or a confirmed clock fault on that device. Then I would quarantine the day, and the worst three would become R-26, R-27, R-14 (by the tool's ordering; I have not re-run it).

### Call 2: T = 5, and R-26 is chronic while R-33 is not
- **Rule:** a route-day is late if its median delay is over T = 5 minutes with at least 5 trips. A route is chronic if it is late on a strict majority of its measured days (at least 3). T is a parameter. I chose 5 after seeing the data, not from an ops policy: the typical delay is about +2 with a 95th percentile near +9, and 5 minutes is a common on-time convention. T = 10 flags nobody but R-35.
- **Breaks on:** R-26 is chronic by a half-minute to one-minute margin (late days Mon 5.5, Wed 6, Thu 6, Sun 6; Tue, Fri and Sat at 3), and at T = 6 nobody is chronic. R-33's daily medians are 4, 5, 5, 7, 5, 8, 5, so it is at or above 5 on six days, with 47% of trips over 5 and 182 minutes beyond T, yet it is "ok" (late on only Thu and Sat) while R-26 (43%, 131 minutes) is chronic. R-17 (130 minutes) and R-37 (125) are almost as late as R-26 by minutes and are late on one day each. I keep the strict ">" because a threshold that bends toward a named route is harder to defend than a thin line. R-33 is listed as borderline.
- **Cost, and who pays:** if the line is too strict, R-33's riders (104 trips, 47% late) pay through refunds. If too loose, R-26's depot head loses his incentive over half-minute margins.
- **What would change my mind:** an ops-agreed on-time number other than 5, or evidence that delays are recorded too coarsely to separate 5.5 from 5. At T = 4, R-33 becomes chronic.

### Call 3: REC-114 applied to the routes in schedule_v2.csv
- **Rule:** for every route listed in schedule_v2.csv, trips on or after its effective_date (2026-08-05) are measured against revised_runtime_min. All other trips use the export's scheduled_runtime_min. HANDOFF says "4xx vehicle series", but vehicle_series in the data is 01 to 40 and equals the route number, so 4xx cannot be identified. I read the directive as "the routes in schedule_v2.csv" (R-14 and R-27 this week). 188 kept trips use the revised baseline. The unadjusted result is always shown beside it. The note column is never read.
- **Breaks on:** R-27. The revised runtime is a flat 45 replacing a per-trip baseline that runs 35 to 55, and it moves R-27 from late on 0 of 7 days to 3 of 7 (Thu 7, Fri 11, Sat 8), and from 104 to 384 minutes beyond T. R-14 moves from 7 of 7 to 2 of 7 days (416 to 249 minutes): its median delay on and after 5 Aug goes from +8 to 0. The same trips took the same time, so the change is in the yardstick. I keep the rule because the directive is signed off, and the tool shows both numbers.
- **Cost, and who pays:** REC-114 takes 167 minutes beyond T off R-14's depot and puts 280 on R-27's. If riders were told the old R-14 timetable, they still arrived late (43% of trips over 5 minutes even after the revision) and the refund queue pays while R-14 is unflagged. If I ignored the directive, R-14's depot head is chronic at 7 of 7 against a timetable that has been replaced.
- **What would change my mind:** evidence of what runtime the rider-facing timetable showed from 5 Aug. If riders saw the old values, I would rank on the unadjusted numbers and report REC-114 as a reconciliation figure only.

### Call 4: ranking is severe, then chronic, then the rest, by minutes beyond T
- **Rule:** tiers first (severe, chronic, rest). Within a tier, minutes beyond T (the sum over trips of max(0, delay − T)), then share of trips over T, then route id. The verdict rests on days late because a depot head's incentive should not depend on one day. The order rests on minutes because the refund queue scales with them. Flagged routes come first so the worst three never contradict the verdict.
- **Breaks on:** R-26 (131 minutes) ranks above R-27 (384) and R-14 (249). Ranking purely by minutes gives R-35, R-27, R-14, and R-26, my only chronic route, falls to fifth. I keep the tiers because a worst-three that omits the one route I call chronic is incoherent.
- **Cost, and who pays:** R-26's depot head is named second on 131 minutes while R-27, with nearly three times the minutes, is third. R-27's riders carry the cost if minutes are what really drive refunds.
- **What would change my mind:** refund data showing that cost tracks minutes late more than days late. The order then becomes R-35, R-27, R-14.

### Call 5: cleaning, and the quarantine rule
- **Rule:** unparseable arrivals (all 24 are "08:60") and trips more than 20 minutes early against the export baseline (18, all with arrival at or before departure) are quarantined and listed by id. The one +00:00 row, T1-02864, is repaired by converting its offset (raw −332, repaired −2). Nothing is trimmed on the late side. 5,250 of 5,292 trips are kept; 42 (0.8%) are quarantined.
- **Breaks on:** R-27, which loses the most (T1-03396, T1-03414, T1-03490, T1-03491: 4 of 147 trips, 2.7%). It is unlikely to move a route's daily median, but I did not test that. I also assume buses left on time, because there is no actual-departure column.
- **Cost, and who pays:** if too aggressive, real early arrivals are dropped, which is small. If too lenient, junk rows pull medians down and can clear a route that riders found late.
- **What would change my mind:** evidence that the 08:60 stamps are a recoverable device bug, or that real trips can arrive more than 20 minutes early (for example a shortened route).

### Call 6: the whole week, and the ops log is not an input
- **Rule:** the default window is all seven days (756 trips each), and any date window works, with at least 3 measured days for a chronic verdict. ops_log.txt is never loaded.
- **Breaks on:** Wednesday. The log says a waterlogged road diverted a western corridor by about 35 minutes all morning and that evening slowed city-wide. The data shows R-35 alone running 36 to 61 minutes late all day, and network-wide Wednesday medians (AM 2, PM 2, 90th percentile 8) match every other day. The log names no route and no dates, and Priya says it is last week's, so I cannot join it to this week's trips.
- **Cost, and who pays:** if the log is right and Wednesday should be discounted, R-35's depot head is flagged for weather. If I used it and it was wrong, 19 late trips get dismissed on an unverifiable note.
- **What would change my mind:** a route-level, dated log entry tying the diversion to R-35.

## 6. Limits
- Delay assumes buses left on time. The export has no actual-departure column.
- T = 5 was chosen after seeing the data. Verdicts for R-26 and R-33 move at T = 4 and T = 6.
- Nothing corroborates the cause of R-35's Wednesday.
- REC-114 is applied to the routes in schedule_v2.csv because 4xx cannot be identified in the data.
- One week of data, with no history to show whether any flagged route is usually late.
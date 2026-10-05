#!/usr/bin/env python3
"""Small, reproducible FCA data-fabric engineering lab; standard library only."""
from __future__ import annotations

import csv
import hashlib
import json
import shutil
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "source"
BRONZE = ROOT / "data" / "bronze"
SILVER = ROOT / "data" / "silver"
GOLD = ROOT / "data" / "gold"
DB = ROOT / "data" / "fabric.db"
FILES = ["fca_product_complaints.csv", "fca_product_complaints_context.csv", "fca_market_complaints_summary.csv"]
PERIODS = ["2024_H1", "2024_H2", "2025_H1", "2025_H2"]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def run() -> int:
    for folder in (BRONZE, SILVER, GOLD):
        folder.mkdir(parents=True, exist_ok=True)
    manifest_rows = read_csv(SOURCE / "source-manifest.csv")
    expected_hashes = {r["file"]: r["sha256"].lower() for r in manifest_rows}
    issues: list[str] = []
    source_checks = []
    tables = {}
    for name in FILES:
        path = SOURCE / name
        if not path.is_file():
            issues.append(f"Missing required source file: {name}")
            continue
        actual = digest(path)
        expected = expected_hashes.get(name)
        hash_ok = expected == actual.lower() if expected else False
        source_checks.append({"file": name, "sha256": actual, "matches_manifest": hash_ok})
        if not hash_ok:
            issues.append(f"Source checksum does not match source-manifest.csv: {name}")
        tables[name] = read_csv(path)

    if issues:
        return fail(issues)

    products = tables[FILES[0]]
    contexts = tables[FILES[1]]
    market = tables[FILES[2]]
    if len(products) != 50:
        issues.append(f"Expected 50 source product rows; found {len(products)}")
    if len(contexts) != 49:
        issues.append(f"Expected 49 source contextual-rate rows; found {len(contexts)}")
    if len(market) != 4:
        issues.append(f"Expected 4 source market periods; found {len(market)}")
    if len({r["product"] for r in products}) != len(products):
        issues.append("Duplicate product key in product volume source")
    if len({r["product"] for r in contexts}) != len(contexts):
        issues.append("Duplicate product key in contextual source")
    if {r["reporting_period"] for r in market} != set(PERIODS):
        issues.append("Market periods do not match the four published periods")

    volume_long = []
    for row in products:
        for period in PERIODS:
            try:
                value = int(row[period])
                if value < 0:
                    raise ValueError("negative count")
            except (ValueError, TypeError):
                issues.append(f"Invalid complaint count for {row['product']} / {period}")
                continue
            volume_long.append({"product": row["product"], "product_group": row["product_group"],
                                "reporting_period": period, "complaints_opened": value})

    context_long = []
    for row in contexts:
        for period in PERIODS:
            raw = row.get(period, "").strip()
            try:
                value = float(raw) if raw else None
            except ValueError:
                issues.append(f"Invalid contextual rate for {row['product']} / {period}")
                value = None
            context_long.append({"product": row["product"], "product_group": row["product_group"],
                                 "reporting_period": period, "complaints_per_1000": value})

    market_clean = []
    for row in market:
        try:
            item = {"reporting_period": row["reporting_period"]}
            for key in row:
                if key != "reporting_period":
                    item[key] = float(row[key]) if key.endswith("_pct") else int(row[key])
            pct_total = sum(item[k] for k in ("closed_within_3_days_pct", "closed_over_3_days_within_8_weeks_pct", "closed_over_8_weeks_pct"))
            if abs(pct_total - 100.0) > 0.02:
                issues.append(f"Closure timing percentages do not total 100 for {row['reporting_period']}: {pct_total}")
            market_clean.append(item)
        except (ValueError, KeyError) as exc:
            issues.append(f"Invalid market summary row {row.get('reporting_period', '?')}: {exc}")

    if issues:
        return fail(issues)

    # Bronze is an immutable, byte-for-byte copy of the checked source snapshot.
    snapshot_id = hashlib.sha256("".join(sorted(c["sha256"] for c in source_checks)).encode()).hexdigest()[:12]
    bronze_snapshot = BRONZE / f"fca_publication_2025_h2_{snapshot_id}"
    bronze_snapshot.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        target = bronze_snapshot / name
        if target.exists() and digest(target) != digest(SOURCE / name):
            return fail([f"Bronze snapshot conflict for {name}; refusing to overwrite retained bytes"])
        if not target.exists():
            shutil.copy2(SOURCE / name, target)

    # Silver uses explicit period rows, keeping business labels and source nulls intact.
    write_csv(SILVER / "product_complaints_long.csv", volume_long,
              ["product", "product_group", "reporting_period", "complaints_opened"])
    write_csv(SILVER / "product_context_long.csv", context_long,
              ["product", "product_group", "reporting_period", "complaints_per_1000"])
    write_csv(SILVER / "market_outcomes.csv", market_clean, list(market_clean[0].keys()))

    latest, previous = "2025_H2", "2025_H1"
    by_key = {(r["product"], r["reporting_period"]): r for r in volume_long}
    product_delta = []
    for row in products:
        now = by_key[(row["product"], latest)]["complaints_opened"]
        before = by_key[(row["product"], previous)]["complaints_opened"]
        product_delta.append({"product": row["product"], "product_group": row["product_group"],
                              "prior_period": previous, "prior_complaints": before,
                              "latest_period": latest, "latest_complaints": now,
                              "absolute_change": now - before,
                              "percentage_change": round((now - before) / before * 100, 2) if before else None})
    product_delta.sort(key=lambda r: abs(r["percentage_change"] or 0), reverse=True)
    group_summary = []
    for period in PERIODS:
        accum: dict[str, int] = {}
        for row in volume_long:
            if row["reporting_period"] == period:
                accum[row["product_group"]] = accum.get(row["product_group"], 0) + row["complaints_opened"]
        group_summary.extend({"reporting_period": period, "product_group": group, "complaints_opened": count}
                             for group, count in sorted(accum.items()))
    write_csv(GOLD / "product_half_year_change.csv", product_delta,
              ["product", "product_group", "prior_period", "prior_complaints", "latest_period", "latest_complaints", "absolute_change", "percentage_change"])
    write_csv(GOLD / "product_group_period_totals.csv", group_summary,
              ["reporting_period", "product_group", "complaints_opened"])

    if DB.exists():
        DB.unlink()
    with sqlite3.connect(DB) as conn:
        conn.executescript("""
        CREATE TABLE silver_product_complaints(product TEXT, product_group TEXT, reporting_period TEXT, complaints_opened INTEGER, PRIMARY KEY(product, reporting_period));
        CREATE TABLE silver_product_context(product TEXT, product_group TEXT, reporting_period TEXT, complaints_per_1000 REAL, PRIMARY KEY(product, reporting_period));
        CREATE TABLE silver_market_outcomes(reporting_period TEXT PRIMARY KEY, complaints_closed INTEGER, closed_within_3_days_pct REAL, closed_over_3_days_within_8_weeks_pct REAL, closed_over_8_weeks_pct REAL, complaints_upheld INTEGER, upheld_pct REAL, total_redress_gbp INTEGER, redress_upheld_gbp INTEGER, redress_not_upheld_gbp INTEGER, average_redress_upheld_gbp INTEGER);
        CREATE TABLE gold_product_half_year_change(product TEXT, product_group TEXT, prior_period TEXT, prior_complaints INTEGER, latest_period TEXT, latest_complaints INTEGER, absolute_change INTEGER, percentage_change REAL);
        CREATE TABLE gold_product_group_period_totals(reporting_period TEXT, product_group TEXT, complaints_opened INTEGER);
        """)
        conn.executemany("INSERT INTO silver_product_complaints VALUES(:product,:product_group,:reporting_period,:complaints_opened)", volume_long)
        conn.executemany("INSERT INTO silver_product_context VALUES(:product,:product_group,:reporting_period,:complaints_per_1000)", context_long)
        conn.executemany("INSERT INTO silver_market_outcomes VALUES(:reporting_period,:complaints_closed,:closed_within_3_days_pct,:closed_over_3_days_within_8_weeks_pct,:closed_over_8_weeks_pct,:complaints_upheld,:upheld_pct,:total_redress_gbp,:redress_upheld_gbp,:redress_not_upheld_gbp,:average_redress_upheld_gbp)", market_clean)
        conn.executemany("INSERT INTO gold_product_half_year_change VALUES(:product,:product_group,:prior_period,:prior_complaints,:latest_period,:latest_complaints,:absolute_change,:percentage_change)", product_delta)
        conn.executemany("INSERT INTO gold_product_group_period_totals VALUES(:reporting_period,:product_group,:complaints_opened)", group_summary)

    report = {
        "status": "PASS",
        "run_timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source_publication": "FCA Aggregate complaints data: 2025 H2",
        "source_snapshot": "Published values transcribed into the bundled source CSV files; see data/source/README-source.md",
        "checks": [
            {"name": "source_sha256_matches_manifest", "status": "PASS", "files_checked": len(source_checks)},
            {"name": "product_row_count", "status": "PASS", "rows": len(products)},
            {"name": "context_row_count", "status": "PASS", "rows": len(contexts)},
            {"name": "market_period_count", "status": "PASS", "rows": len(market)},
            {"name": "product_period_counts_nonnegative", "status": "PASS", "rows": len(volume_long)},
            {"name": "closure_bands_sum_to_100pct", "status": "PASS", "periods": len(market_clean)},
            {"name": "null_context_values_preserved", "status": "PASS", "null_cells": sum(r["complaints_per_1000"] is None for r in context_long)},
        ],
        "source_files": source_checks,
        "outputs": [f"data/bronze/{bronze_snapshot.name}/", "data/fabric.db", "data/silver/", "data/gold/"],
        "note": "Market/product aggregates only; this run does not contain consumer-level complaint records or a live feed."
    }
    (ROOT / "pipeline" / "latest-run.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


def fail(issues: list[str]) -> int:
    report = {"status": "FAIL", "issues": issues, "note": "Quality gates failed; no curated outputs were written."}
    (ROOT / "pipeline" / "latest-run.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2), file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(run())

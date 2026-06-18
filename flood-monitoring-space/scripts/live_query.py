import json
import requests
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent

STAC_URL = "https://catalogue.dataspace.copernicus.eu/stac/search"

FLOOD_AOI = [14.0, 49.5, 23.0, 54.5]
FLOOD_AOI_LABEL = "Central Europe (Poland / Czech Republic / Germany)"

STAC_PROVIDERS = {
    "sentinel_1": {
        "collection": "sentinel-1-grd",
        "label": "Sentinel-1 SAR",
        "cloud_independent": True
    },
    "sentinel_2": {
        "collection": "sentinel-2-l2a",
        "label": "Sentinel-2 Optical",
        "cloud_independent": False
    }
}

METADATA_ONLY_PROVIDERS = {
    "sentinel_3": {
        "label": "Sentinel-3 OLCI",
        "access_note": "Available via CDSE OData or EUMETSAT Data Store (requires auth)"
    },
    "sentinel_5p": {
        "label": "Sentinel-5P TROPOMI",
        "access_note": "Available via CDSE OData API (requires registration)"
    },
    "copernicus_ems": {
        "label": "Copernicus Emergency Management Service",
        "access_note": "On-demand activation service — https://emergency.copernicus.eu"
    },
    "copernicus_clms": {
        "label": "Copernicus Land Monitoring Service",
        "access_note": "Pre-processed archive products — https://land.copernicus.eu"
    },
    "cdse": {
        "label": "CDSE Platform",
        "access_note": "Access platform (STAC, OData, openEO) — https://dataspace.copernicus.eu"
    },
    "eumetsat": {
        "label": "EUMETSAT",
        "access_note": "Meteorological data — https://data.eumetsat.int"
    }
}


def load_catalog():
    catalog_path = BASE_DIR / "catalog" / "federated_catalog.json"
    if not catalog_path.exists():
        print("Catalog not found. Run build_catalog.py first.")
        exit(1)
    with open(catalog_path, encoding="utf-8") as f:
        return json.load(f)


def query_stac(collection, bbox, time_window, limit=10):
    payload = {
        "collections": [collection],
        "bbox": bbox,
        "datetime": time_window,
        "limit": limit
    }
    try:
        resp = requests.post(STAC_URL, json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json().get("features", []), None
    except Exception as e:
        return [], str(e)


def summarise_items(items, provider_id):
    if not items:
        return None
    cloud_values = [
        i.get("properties", {}).get("eo:cloud_cover")
        for i in items
        if i.get("properties", {}).get("eo:cloud_cover") is not None
    ]
    avg_cloud = round(sum(cloud_values) / len(cloud_values), 1) if cloud_values else None
    datetimes = [
        i.get("properties", {}).get("datetime", "")
        for i in items
    ]
    datetimes = sorted([d for d in datetimes if d])
    return {
        "provider_id": provider_id,
        "count": len(items),
        "earliest": datetimes[0] if datetimes else "N/A",
        "latest": datetimes[-1] if datetimes else "N/A",
        "avg_cloud_cover": avg_cloud,
        "example_ids": [i.get("id", "N/A") for i in items[:3]]
    }


def build_report(catalog, time_window, results, errors):
    lines = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines.append("=" * 70)
    lines.append("LIVE STAC AVAILABILITY QUERY — FEDERATED FLOOD MONITORING DATA SPACE")
    lines.append("=" * 70)
    lines.append(f"Query time:    {now}")
    lines.append(f"STAC endpoint: {STAC_URL}")
    lines.append(f"AOI:           {FLOOD_AOI_LABEL}")
    lines.append(f"Bbox:          {FLOOD_AOI}")
    lines.append(f"Time window:   {time_window}")
    lines.append("")

    all_providers = {p["provider_id"]: p for p in catalog["providers"]}

    lines.append("-" * 70)
    lines.append("LIVE STAC QUERY RESULTS (sentinel-1-grd, sentinel-2-l2a via CDSE)")
    lines.append("-" * 70)

    for pid, pinfo in STAC_PROVIDERS.items():
        summary = results.get(pid)
        error = errors.get(pid)
        meta = all_providers.get(pid, {})

        lines.append(f"\n  [{pid.upper()}]  {pinfo['label']}  (collection: {pinfo['collection']})")
        if error:
            lines.append(f"  Status:   ERROR — {error}")
        elif summary is None:
            lines.append("  Status:   NO RESULTS IN WINDOW")
        else:
            lines.append(f"  Status:   AVAILABLE")
            lines.append(f"  Products found:    {summary['count']}")
            lines.append(f"  Earliest:          {summary['earliest']}")
            lines.append(f"  Latest:            {summary['latest']}")
            if summary["avg_cloud_cover"] is not None:
                lines.append(f"  Avg cloud cover:   {summary['avg_cloud_cover']}%")
            lines.append(f"  Example IDs:")
            for eid in summary["example_ids"]:
                lines.append(f"    - {eid}")

        if meta:
            req = meta.get("operational_requirements", {})
            supports = [r for r, d in req.items() if d.get("supported")]
            lines.append(f"  Flood requirements met: {', '.join(supports)}")

    lines.append("")
    lines.append("-" * 70)
    lines.append("METADATA-ONLY PROVIDERS (external access)")
    lines.append("-" * 70)
    for pid, pinfo in METADATA_ONLY_PROVIDERS.items():
        meta = all_providers.get(pid, {})
        lines.append(f"\n  [{pid.upper()}]  {pinfo['label']}")
        lines.append(f"  Access: {pinfo['access_note']}")
        if meta:
            req = meta.get("operational_requirements", {})
            supports = [r for r, d in req.items() if d.get("supported")]
            lines.append(f"  Flood requirements met: {', '.join(supports)}")

    lines.append("")
    lines.append("-" * 70)
    lines.append("SENSOR RECOMMENDATION BY SCENARIO")
    lines.append("-" * 70)

    available_ids = [pid for pid, s in results.items() if s is not None]

    all_labels = {
        **{pid: pinfo["label"] for pid, pinfo in STAC_PROVIDERS.items()},
        **{pid: pinfo["label"] for pid, pinfo in METADATA_ONLY_PROVIDERS.items()}
    }

    scenarios = {
        "Active flood event (cloudy)":    ["sentinel_1"],
        "Active flood event (clear sky)": ["sentinel_1", "sentinel_2", "sentinel_3"],
        "Night-time monitoring":          ["sentinel_1"],
        "Post-event damage assessment":   ["sentinel_2", "sentinel_1"],
        "Continental overview":           ["sentinel_3"],
        "Upstream rainfall monitoring":   ["eumetsat"],
        "Emergency mapping activation":   ["copernicus_ems"]
    }

    for scenario, preferred in scenarios.items():
        lines.append(f"\n  {scenario}:")
        for p in preferred:
            if p in STAC_PROVIDERS:
                status = "AVAILABLE" if p in available_ids else "NO DATA IN WINDOW"
            else:
                status = "external service (see metadata)"
            label = all_labels.get(p, p)
            lines.append(f"    -> {label:40s} [{status}]")

    lines.append("")
    lines.append("=" * 70)
    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Live STAC availability query for the Flood Monitoring Data Space")
    parser.add_argument("--start", default="2024-09-01T00:00:00Z", help="Start datetime (ISO8601)")
    parser.add_argument("--end", default="2024-09-15T23:59:59Z", help="End datetime (ISO8601)")
    parser.add_argument("--limit", type=int, default=10, help="Max results per provider")
    args = parser.parse_args()

    time_window = f"{args.start}/{args.end}"
    catalog = load_catalog()

    print(f"Querying CDSE STAC API for {len(STAC_PROVIDERS)} providers...")
    print(f"AOI: {FLOOD_AOI_LABEL}")
    print(f"Window: {time_window}")
    print()

    results = {}
    errors = {}

    for pid, pinfo in STAC_PROVIDERS.items():
        print(f"  Querying {pinfo['label']}...", end=" ", flush=True)
        items, error = query_stac(pinfo["collection"], FLOOD_AOI, time_window, args.limit)
        if error:
            errors[pid] = error
            print(f"ERROR: {error}")
        else:
            results[pid] = summarise_items(items, pid)
            count = results[pid]["count"] if results[pid] else 0
            print(f"{count} products found")

    report_text = build_report(catalog, time_window, results, errors)

    reports_dir = BASE_DIR / "reports"
    reports_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_dir / f"live_query_{timestamp}.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    print()
    print(report_text)
    print(f"Report saved to: {report_path}")


if __name__ == "__main__":
    main()

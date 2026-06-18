import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent

REQUIREMENTS = [
    "flood_detection",
    "flood_extent_assessment",
    "cloudy_conditions",
    "night_operations",
    "emergency_response"
]

REQ_ABBREV = {
    "flood_detection":         "FLD_DET",
    "flood_extent_assessment": "FLD_EXT",
    "cloudy_conditions":       "CLOUDY ",
    "night_operations":        "NIGHT  ",
    "emergency_response":      "EMERG  "
}


def load_catalog():
    catalog_path = BASE_DIR / "catalog" / "federated_catalog.json"
    with open(catalog_path, encoding="utf-8") as f:
        return json.load(f)


def build_report(catalog):
    providers = catalog["providers"]
    lines = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines.append("=" * 70)
    lines.append("FEDERATED EO DATA SPACE FOR NATIONAL FLOOD MONITORING")
    lines.append("Data Spaces and Federated Data Engineering — Labs 10-12")
    lines.append("=" * 70)
    lines.append(f"Report generated:    {now}")
    lines.append(f"Catalog generated:   {catalog['generated_at']}")
    lines.append(f"Total providers:     {catalog['provider_count']}")
    lines.append("")

    lines.append("-" * 70)
    lines.append("REGISTERED PROVIDERS")
    lines.append("-" * 70)
    for p in providers:
        req_count = sum(1 for r in REQUIREMENTS if p["operational_requirements"][r]["supported"])
        lines.append(f"  [{req_count}/5] {p['provider_id']:25s} | {p['provider_label']:35s} | {p['organization']}")
    lines.append("")

    lines.append("-" * 70)
    lines.append("OPERATIONAL REQUIREMENTS COVERAGE")
    lines.append("-" * 70)
    for req in REQUIREMENTS:
        supported = [p["provider_label"] for p in providers if p["operational_requirements"][req]["supported"]]
        not_supported = [p["provider_label"] for p in providers if not p["operational_requirements"][req]["supported"]]
        lines.append(f"\n  {req}  ({len(supported)}/{len(providers)} providers support this)")
        lines.append(f"  Supported:")
        for s in supported:
            lines.append(f"    + {s}")
        if not_supported:
            lines.append(f"  Not supported:")
            for ns in not_supported:
                lines.append(f"    - {ns}")
    lines.append("")

    lines.append("-" * 70)
    lines.append("COVERAGE MATRIX")
    lines.append("-" * 70)
    col = 9
    header = f"  {'Provider':<28}" + "".join(f"{REQ_ABBREV[r]:>{col}}" for r in REQUIREMENTS) + "  TOTAL"
    lines.append(header)
    lines.append("  " + "-" * (28 + col * len(REQUIREMENTS) + 8))
    for p in providers:
        row = f"  {p['provider_label']:<28}"
        total = 0
        for req in REQUIREMENTS:
            val = "YES" if p["operational_requirements"][req]["supported"] else "NO"
            if val == "YES":
                total += 1
            row += f"{val:>{col}}"
        row += f"  {total}/5"
        lines.append(row)
    cov_row = f"  {'COVERAGE':28}"
    for req in REQUIREMENTS:
        count = sum(1 for p in providers if p["operational_requirements"][req]["supported"])
        cov_row += f"{count}/{len(providers)}".rjust(col)
    lines.append(cov_row)
    lines.append("")

    lines.append("-" * 70)
    lines.append("PROVIDER DETAILS")
    lines.append("-" * 70)
    for p in providers:
        lines.append("")
        lines.append(f"  [{p['provider_id'].upper()}]")
        lines.append(f"  Label:        {p['provider_label']}")
        lines.append(f"  Organization: {p['organization']}")
        lines.append(f"  Type:         {p['type']}")
        lines.append(f"  Sensor:       {p.get('sensor_type', 'N/A')}")
        lines.append(f"  Resolution:   {p.get('spatial_resolution', 'N/A')}")
        lines.append(f"  Revisit:      {p.get('revisit_time', 'N/A')}")
        lines.append(f"  Access:       {p['access_url']}")
        lines.append(f"  API:          {p.get('api_endpoint', 'N/A')}")
        lines.append(f"  Description:  {p['description']}")
        lines.append(f"  Strengths:    {'; '.join(p['strengths'][:3])}")
        lines.append(f"  Limitations:  {'; '.join(p['limitations'][:2])}")
        req_list = [r for r in REQUIREMENTS if p["operational_requirements"][r]["supported"]]
        lines.append(f"  Supports:     {', '.join(req_list) if req_list else 'none'}")
    lines.append("")

    lines.append("-" * 70)
    lines.append("FEDERATION SUMMARY")
    lines.append("-" * 70)
    orgs = list(set(p["organization"] for p in providers))
    types = list(set(p["type"] for p in providers))
    lines.append(f"  Total EO resources in data space: {len(providers)}")
    lines.append(f"  Originating organizations:        {len(orgs)}")
    lines.append(f"  Resource types represented:       {len(types)}")
    for t in types:
        count = sum(1 for p in providers if p["type"] == t)
        lines.append(f"    - {t}: {count}")
    lines.append("")
    for req in REQUIREMENTS:
        count = sum(1 for p in providers if p["operational_requirements"][req]["supported"])
        pct = int(100 * count / len(providers))
        lines.append(f"  {req:<35} {count}/{len(providers)} providers ({pct}% coverage)")
    lines.append("")
    fully_covered = [
        req for req in REQUIREMENTS
        if all(p["operational_requirements"][req]["supported"] for p in providers)
    ]
    lines.append(f"  Requirements with full (100%) provider coverage: {len(fully_covered)}")
    for r in fully_covered:
        lines.append(f"    * {r}")
    lines.append("=" * 70)

    return "\n".join(lines)


def main():
    reports_dir = BASE_DIR / "reports"
    reports_dir.mkdir(exist_ok=True)

    catalog = load_catalog()
    report_text = build_report(catalog)

    report_path = reports_dir / "lab10_flood_space_report.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(report_text)
    print()
    print(f"Report saved to: {report_path}")


if __name__ == "__main__":
    main()

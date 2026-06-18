import json
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

REQUIREMENTS = [
    "flood_detection",
    "flood_extent_assessment",
    "cloudy_conditions",
    "night_operations",
    "emergency_response"
]

REQ_ABBREV = {
    "flood_detection":       "FLD_DET",
    "flood_extent_assessment": "FLD_EXT",
    "cloudy_conditions":     "CLOUDY",
    "night_operations":      "NIGHT",
    "emergency_response":    "EMERG"
}


def load_catalog():
    catalog_path = BASE_DIR / "catalog" / "federated_catalog.json"
    if not catalog_path.exists():
        print("Catalog not found. Run build_catalog.py first.")
        exit(1)
    with open(catalog_path, encoding="utf-8") as f:
        return json.load(f)


def compare_two(p1, p2):
    col = 32
    print()
    print("=" * (20 + col * 2))
    print(f"COMPARISON: {p1['provider_label']} vs {p2['provider_label']}")
    print("=" * (20 + col * 2))

    fields = [
        ("Organization",   "organization"),
        ("Type",           "type"),
        ("Sensor",         "sensor_type"),
        ("Resolution",     "spatial_resolution"),
        ("Revisit",        "revisit_time"),
        ("Access URL",     "access_url"),
    ]

    print()
    print(f"{'Field':<20} {p1['provider_label']:<{col}} {p2['provider_label']:<{col}}")
    print(f"{'-'*20} {'-'*col} {'-'*col}")
    for label, key in fields:
        v1 = str(p1.get(key, "N/A"))
        v2 = str(p2.get(key, "N/A"))
        v1 = (v1[:col-3] + "...") if len(v1) > col else v1
        v2 = (v2[:col-3] + "...") if len(v2) > col else v2
        print(f"{label:<20} {v1:<{col}} {v2:<{col}}")

    print()
    print(f"{'OPERATIONAL REQUIREMENTS':<20} {p1['provider_label']:<{col}} {p2['provider_label']:<{col}}")
    print(f"{'-'*20} {'-'*col} {'-'*col}")
    for req in REQUIREMENTS:
        s1 = "YES" if p1["operational_requirements"][req]["supported"] else "NO "
        s2 = "YES" if p2["operational_requirements"][req]["supported"] else "NO "
        print(f"{req:<20} {s1:<{col}} {s2:<{col}}")

    print()
    print("STRENGTHS")
    max_rows = max(len(p1["strengths"]), len(p2["strengths"]))
    s1_list = p1["strengths"]
    s2_list = p2["strengths"]
    for i in range(max_rows):
        v1 = ("+ " + s1_list[i]) if i < len(s1_list) else ""
        v2 = ("+ " + s2_list[i]) if i < len(s2_list) else ""
        v1 = (v1[:col-3] + "...") if len(v1) > col else v1
        v2 = (v2[:col-3] + "...") if len(v2) > col else v2
        print(f"{'':20} {v1:<{col}} {v2:<{col}}")

    print()
    print("LIMITATIONS")
    l1_list = p1["limitations"]
    l2_list = p2["limitations"]
    max_rows = max(len(l1_list), len(l2_list))
    for i in range(max_rows):
        v1 = ("- " + l1_list[i]) if i < len(l1_list) else ""
        v2 = ("- " + l2_list[i]) if i < len(l2_list) else ""
        v1 = (v1[:col-3] + "...") if len(v1) > col else v1
        v2 = (v2[:col-3] + "...") if len(v2) > col else v2
        print(f"{'':20} {v1:<{col}} {v2:<{col}}")


def coverage_matrix(providers):
    col = 10
    print()
    print("COVERAGE MATRIX — ALL PROVIDERS x ALL OPERATIONAL REQUIREMENTS")
    print("=" * (30 + col * len(REQUIREMENTS)))
    print()
    header = f"  {'Provider':<28}" + "".join(f"{REQ_ABBREV[r]:>{col}}" for r in REQUIREMENTS) + f"  {'TOTAL':>6}"
    print(header)
    print("  " + "-" * (28 + col * len(REQUIREMENTS) + 8))
    for p in providers:
        row = f"  {p['provider_label']:<28}"
        total = 0
        for req in REQUIREMENTS:
            val = "YES" if p["operational_requirements"][req]["supported"] else "NO"
            if val == "YES":
                total += 1
            row += f"{val:>{col}}"
        row += f"  {total:>4}/5"
        print(row)
    print()
    print(f"  {'REQUIREMENT COVERAGE':28}", end="")
    for req in REQUIREMENTS:
        count = sum(1 for p in providers if p["operational_requirements"][req]["supported"])
        print(f"{count}/{len(providers)}".rjust(col), end="")
    print()


def all_for_requirement(providers, requirement):
    if requirement not in REQUIREMENTS:
        print(f"Unknown requirement. Valid: {REQUIREMENTS}")
        return
    print()
    print(f"ALL PROVIDERS — REQUIREMENT: {requirement}")
    print("=" * 70)
    print(f"  {'Provider':<35} {'Supported':<10} Notes")
    print(f"  {'-'*35} {'-'*10} {'-'*40}")
    for p in providers:
        req_data = p["operational_requirements"][requirement]
        status = "YES" if req_data["supported"] else "NO "
        note = req_data["notes"]
        if len(note) > 60:
            note = note[:57] + "..."
        print(f"  {p['provider_label']:<35} {status:<10} {note}")


def main():
    parser = argparse.ArgumentParser(
        description="Compare EO resources in the Federated Flood Monitoring Data Space"
    )
    parser.add_argument("providers", nargs="*", help="Two provider IDs to compare side by side")
    parser.add_argument("--requirement", help="Show all providers for one operational requirement")
    parser.add_argument("--matrix", action="store_true", help="Show full coverage matrix")
    args = parser.parse_args()

    catalog = load_catalog()
    all_providers = catalog["providers"]

    if args.matrix:
        coverage_matrix(all_providers)
    elif args.requirement:
        all_for_requirement(all_providers, args.requirement)
    elif len(args.providers) == 2:
        p1_id, p2_id = args.providers
        p1 = next((p for p in all_providers if p["provider_id"] == p1_id), None)
        p2 = next((p for p in all_providers if p["provider_id"] == p2_id), None)
        if not p1:
            print(f"Provider '{p1_id}' not found.")
            return
        if not p2:
            print(f"Provider '{p2_id}' not found.")
            return
        compare_two(p1, p2)
    else:
        print("Usage:")
        print("  python compare.py sentinel_1 sentinel_2          (side-by-side)")
        print("  python compare.py --requirement flood_detection  (all providers for one requirement)")
        print("  python compare.py --matrix                       (full coverage matrix)")
        print()
        print(f"Available providers: {[p['provider_id'] for p in all_providers]}")


if __name__ == "__main__":
    main()

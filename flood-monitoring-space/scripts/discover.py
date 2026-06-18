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


def load_catalog():
    catalog_path = BASE_DIR / "catalog" / "federated_catalog.json"
    if not catalog_path.exists():
        print("Catalog not found. Run build_catalog.py first.")
        exit(1)
    with open(catalog_path, encoding="utf-8") as f:
        return json.load(f)


def print_provider_brief(p):
    req_count = sum(1 for r in REQUIREMENTS if p["operational_requirements"][r]["supported"])
    print(f"  {p['provider_id']:25s} | {p['provider_label']:35s} | {p['organization']:40s} | {req_count}/5 requirements")


def print_provider_full(p):
    print()
    print("=" * 70)
    print(f"  Provider:     {p['provider_label']}")
    print(f"  ID:           {p['provider_id']}")
    print(f"  Organization: {p['organization']}")
    print(f"  Type:         {p['type']}")
    print(f"  Sensor:       {p.get('sensor_type', 'N/A')}")
    print(f"  Resolution:   {p.get('spatial_resolution', 'N/A')}")
    print(f"  Revisit:      {p.get('revisit_time', 'N/A')}")
    print(f"  Access URL:   {p['access_url']}")
    print(f"  API Endpoint: {p.get('api_endpoint', 'N/A')}")
    print()
    print(f"  Description: {p['description']}")
    print()
    print("  Operational Requirements:")
    for req in REQUIREMENTS:
        details = p["operational_requirements"][req]
        status = "YES" if details["supported"] else "NO "
        print(f"    [{status}] {req:<30} {details['notes']}")
    print()
    print("  Strengths:")
    for s in p["strengths"]:
        print(f"    + {s}")
    print()
    print("  Limitations:")
    for lim in p["limitations"]:
        print(f"    - {lim}")
    print()
    print(f"  Products: {', '.join(p.get('products', []))}")
    print()
    print("  Recommended for:")
    for r in p.get("recommended_for", []):
        print(f"    * {r}")


def list_all(providers):
    print()
    print("FEDERATED EO DATA SPACE FOR NATIONAL FLOOD MONITORING")
    print("=" * 70)
    print(f"Registered providers: {len(providers)}")
    print()
    print(f"  {'ID':25s} | {'Label':35s} | {'Organization':40s} | Coverage")
    print(f"  {'-'*25} | {'-'*35} | {'-'*40} | {'-'*12}")
    for p in providers:
        print_provider_brief(p)
    print()
    print(f"Available operational requirements:")
    for r in REQUIREMENTS:
        print(f"  - {r}")
    print()
    print("Usage examples:")
    print("  python discover.py --requirement flood_detection")
    print("  python discover.py --provider sentinel_1")
    print("  python discover.py --search SAR")


def filter_by_requirement(providers, requirement):
    if requirement not in REQUIREMENTS:
        print(f"Unknown requirement '{requirement}'.")
        print(f"Valid requirements: {REQUIREMENTS}")
        return
    matched = [p for p in providers if p["operational_requirements"][requirement]["supported"]]
    not_matched = [p for p in providers if not p["operational_requirements"][requirement]["supported"]]
    print()
    print(f"REQUIREMENT: {requirement}")
    print("=" * 70)
    print(f"Supported ({len(matched)}/{len(providers)} providers):")
    print()
    for p in matched:
        note = p["operational_requirements"][requirement]["notes"]
        print(f"  {p['provider_label']:<35} {note}")
    if not_matched:
        print()
        print(f"Not supported ({len(not_matched)} providers):")
        for p in not_matched:
            note = p["operational_requirements"][requirement]["notes"]
            print(f"  {p['provider_label']:<35} {note}")


def show_provider(providers, provider_id):
    matched = [p for p in providers if p["provider_id"] == provider_id]
    if not matched:
        print(f"Provider '{provider_id}' not found.")
        print(f"Available IDs: {[p['provider_id'] for p in providers]}")
        return
    print_provider_full(matched[0])


def search_text(providers, query):
    query_lower = query.lower()
    results = []
    for p in providers:
        if query_lower in json.dumps(p).lower():
            results.append(p)
    print()
    print(f"SEARCH: '{query}'  —  {len(results)} result(s) out of {len(providers)} providers")
    print("=" * 70)
    for p in results:
        print_provider_brief(p)


def main():
    parser = argparse.ArgumentParser(
        description="Discover EO resources in the Federated Flood Monitoring Data Space"
    )
    parser.add_argument("--requirement", help="Filter by operational requirement")
    parser.add_argument("--provider", help="Show full details for a specific provider ID")
    parser.add_argument("--search", help="Free-text search across all provider metadata")
    args = parser.parse_args()

    catalog = load_catalog()
    providers = catalog["providers"]

    if args.provider:
        show_provider(providers, args.provider)
    elif args.requirement:
        filter_by_requirement(providers, args.requirement)
    elif args.search:
        search_text(providers, args.search)
    else:
        list_all(providers)


if __name__ == "__main__":
    main()

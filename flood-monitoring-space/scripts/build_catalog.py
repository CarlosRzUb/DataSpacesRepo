import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent


def load_providers():
    providers_dir = BASE_DIR / "providers"
    providers = []
    for provider_dir in sorted(providers_dir.iterdir()):
        if provider_dir.is_dir():
            metadata_file = provider_dir / "metadata.json"
            if metadata_file.exists():
                with open(metadata_file, encoding="utf-8") as f:
                    providers.append(json.load(f))
    return providers


def build_catalog(providers):
    return {
        "catalog_name": "Federated EO Data Space for National Flood Monitoring",
        "generated_at": datetime.now().isoformat(),
        "provider_count": len(providers),
        "operational_requirements": [
            "flood_detection",
            "flood_extent_assessment",
            "cloudy_conditions",
            "night_operations",
            "emergency_response"
        ],
        "providers": providers
    }


def main():
    catalog_dir = BASE_DIR / "catalog"
    catalog_dir.mkdir(exist_ok=True)

    providers = load_providers()
    catalog = build_catalog(providers)

    output_path = catalog_dir / "federated_catalog.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    print(f"Federated catalog built: {len(providers)} providers registered")
    print(f"Output: {output_path}")
    print()
    for p in providers:
        req_count = sum(
            1 for r in catalog["operational_requirements"]
            if p["operational_requirements"][r]["supported"]
        )
        print(f"  [{req_count}/5] {p['provider_id']:25s} | {p['provider_label']}")


if __name__ == "__main__":
    main()

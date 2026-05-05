import requests
import json
import os

os.makedirs("results", exist_ok=True)

URL = "https://catalogue.dataspace.copernicus.eu/stac/search"

queries = [
    {
        "name": "Query 1: Optical monitoring of southern Poland",
        "payload": {
            "collections": ["sentinel-2-l2a"],
            "bbox": [19.0, 50.0, 20.0, 51.0],
            "datetime": "2024-01-01T00:00:00Z/2024-01-10T23:59:59Z",
            "limit": 20
        }
    },
    {
        "name": "Query 2: Optical monitoring of Baltic region",
        "payload": {
            "collections": ["sentinel-2-l2a"],
            "bbox": [17.0, 54.0, 19.0, 55.5],
            "datetime": "2024-01-01T00:00:00Z/2024-01-10T23:59:59Z",
            "limit": 20
        }
    },
    {
        "name": "Query 3: Radar monitoring of southern Poland",
        "payload": {
            "collections": ["ccm-sar"],
            "bbox": [19.0, 50.0, 20.0, 51.0],
            "datetime": "2024-01-01T00:00:00Z/2024-01-10T23:59:59Z",
            "limit": 20
        }
    }
]

raw_items = []
unified_catalog = []
seen_ids = set()
duplicates_removed = 0
query_counts = {}

for q in queries:
    try:
        response = requests.post(URL, json=q["payload"], timeout=30)
        if response.status_code != 200:
            print(f"Error response from {q['name']}: {response.text}")
        response.raise_for_status()
        features = response.json().get("features", [])
        query_counts[q["name"]] = len(features)

        for item in features:
            raw_items.append(item)
            item_id = item.get("id")

            if item_id in seen_ids:
                duplicates_removed += 1
                continue

            seen_ids.add(item_id)

            unified_item = {
                "id": item_id,
                "collection": item.get("collection"),
                "bbox": item.get("bbox"),
                "assets_count": len(item.get("assets", {})),
                "source_provider": "CDSE",
                "source_query": q["name"],
                "datetime": item["properties"]["datetime"] 
            }
            unified_catalog.append(unified_item)

    except Exception as e:
        print(f"Failed {q['name']}: {e}")
        query_counts[q["name"]] = 0

unified_catalog.sort(key=lambda x: x.get("datetime", ""))

earliest = unified_catalog[0]["datetime"] if unified_catalog else "N/A"
latest = unified_catalog[-1]["datetime"] if unified_catalog else "N/A"
represented_collections = list(set(item["collection"] for item in unified_catalog))

for item in unified_catalog:
    if "datetime" in item:
        del item["datetime"] 

with open("results/raw_stac_items.json", "w") as f:
    json.dump(raw_items, f, indent=2)

with open("results/federated_results.json", "w") as f:
    json.dump(unified_catalog, f, indent=2)

print("DATA: ")
for k, v in query_counts.items():
    print(f"{k}: {v} products")
print(f"Duplicates removed: {duplicates_removed}")
print(f"Total unique products: {len(unified_catalog)}")
print(f"Earliest observation: {earliest}")
print(f"Latest observation: {latest}")
print(f"Collections represented: {represented_collections}")

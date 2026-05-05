import requests

url = "https://catalogue.dataspace.copernicus.eu/stac/search"
query = {
    "collections": ["sentinel-2-l2a"],
    "limit": 5
}

try:
    response = requests.post(url, json=query, timeout=20)
    response.raise_for_status()
    data = response.json()

    for item in data.get("features", []):
        item_id = item["id"]
        acq_time = item["properties"]["datetime"]
        assets_count = len(item.get("assets", {}))

        # Extraer satélite y tile del ID
        parts = item_id.split("_")
        satellite = parts[0] if len(parts) > 0 else "N/A"
        tile = next((p for p in parts if p.startswith("T") and len(p) == 6), "N/A")

        print(f"ID: {item_id}")
        print(f"Time: {acq_time}")
        print(f"Satellite: {satellite}")
        print(f"Tile: {tile}")
        print(f"Assets: {assets_count}")
        print("-" * 30)

except Exception as e:
    print("REQUEST FAILED:", e)

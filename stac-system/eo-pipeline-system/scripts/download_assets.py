import os
import requests

STAC_URL = "https://stac.dataspace.copernicus.eu/v1/search"
QUERY = {
    "collections": ["sentinel-2-l2a"],
    "bbox": [19.0, 50.0, 20.0, 51.0],
    "datetime": "2024-01-01T00:00:00Z/2024-01-31T23:59:59Z",
    "query": {
        "eo:cloud_cover": {
            "lt": 20
        }
    },
    "limit": 1
}

OUTPUT_PATHS = {
    "thumbnail": "assets/thumbnails/thumbnail.jpg",
    "TCI_10m": "assets/visual/visual.jp2",
    "B04_10m": "assets/bands/B04.jp2",
    "B08_10m": "assets/bands/B08.jp2"
}

def is_http_url(url):
    return url.startswith("http://") or url.startswith("https://")

def download_file(url, output_path):
    if not is_http_url(url):
        print("SKIPPED NON-HTTP ASSET:", url)
        return False
    try:
        response = requests.get(url, timeout=120)
        response.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"FAILED TO DOWNLOAD {url}: {e}")
        return False

def main():
    response = requests.post(STAC_URL, json=QUERY)
    response.raise_for_status()
    data = response.json()
    
    if not data.get("features"):
        print("NO PRODUCTS FOUND")
        return

    item = data["features"][0]
    assets = item["assets"]
    
    print("AVAILABLE ASSETS:")
    for asset_name in assets:
        print(asset_name)
        
    downloaded_count = 0
    skipped_count = 0
    
    print("\nSTARTING ASSET DOWNLOAD:")
    for asset_key, out_path in OUTPUT_PATHS.items():
        if asset_key in assets:
            asset_data = assets[asset_key]
            url = asset_data.get("href")
            
            if not is_http_url(url) and "alternate" in asset_data:
                url = asset_data["alternate"].get("https", {}).get("href", url)
                
            if download_file(url, out_path):
                downloaded_count += 1
                print(f"DOWNLOADED: {asset_key} -> {out_path}")
            else:
                skipped_count += 1
        else:
            print(f"ASSET NOT FOUND IN ITEM: {asset_key}")
            skipped_count += 1

    print(f"\nDOWNLOAD REPORT:")
    print(f"Total downloaded: {downloaded_count}")
    print(f"Total skipped: {skipped_count}")

if __name__ == "__main__":
    main()

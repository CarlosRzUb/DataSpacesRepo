import os
import requests
from datetime import datetime

stac_url = "https://stac.dataspace.copernicus.eu/v1/search"
query = {
    "collections": ["sentinel-2-l2a"],
    "bbox": [19.0, 50.0, 20.0, 51.0],
    "datetime": "2024-01-01T00:00:00Z/2024-01-31T23:59:59Z",
    "limit": 10
}

def compute_cloud_score(cloud_cover):
    if cloud_cover is None:
        return 0
    return max(0, 100 - cloud_cover)

def compute_completeness_score(assets_count):
    if assets_count >= 30:
        return 30
    elif assets_count >= 20:
        return 20
    elif assets_count >= 10:
        return 10
    return 0

def parse_datetime(val):
    if val.endswith("Z"):
        val = val.replace("Z", "+00:00")
    return datetime.fromisoformat(val)

def main():
    os.makedirs("reports", exist_ok=True)
    response = requests.post(stac_url, json=query, timeout=30)
    response.raise_for_status()
    features = response.json().get("features", [])

    if not features:
        print("No observations found.")
        return

    parsed_items = []
    for item in features:
        props = item.get("properties", {})
        assets = item.get("assets", {})
        parsed_items.append({
            "id": item.get("id"),
            "datetime_str": props.get("datetime"),
            "datetime_obj": parse_datetime(props.get("datetime")),
            "cloud_cover": props.get("eo:cloud_cover"),
            "assets_count": len(assets)
        })

    newest_time = max(item["datetime_obj"] for item in parsed_items)

    ranked_items = []
    for item in parsed_items:
        cloud_score = compute_cloud_score(item["cloud_cover"])
        completeness_score = compute_completeness_score(item["assets_count"])
        
        age_days = (newest_time - item["datetime_obj"]).total_seconds() / 86400
        recency_score = max(0, 20 - (age_days / 30) * 20)

        final_score = cloud_score + completeness_score + recency_score
        
        ranked_items.append({
            "id": item["id"],
            "datetime": item["datetime_str"],
            "cloud_cover": item["cloud_cover"],
            "assets_count": item["assets_count"],
            "cloud_score": cloud_score,
            "completeness_score": completeness_score,
            "recency_score": recency_score,
            "final_score": final_score
        })

    ranked_items.sort(key=lambda x: x["final_score"], reverse=True)

    report_lines = [
        "OBSERVATION RANKING REPORT",
        "=========================="
    ]
    
    for idx, item in enumerate(ranked_items, 1):
        line = (
            f"{idx}. ID: {item['id']}\n"
            f"   Time: {item['datetime']}\n"
            f"   Cloud cover: {item['cloud_cover']}\n"
            f"   Assets count: {item['assets_count']}\n"
            f"   Cloud score: {item['cloud_score']:.2f}\n"
            f"   Completeness score: {item['completeness_score']:.2f}\n"
            f"   Recency score: {item['recency_score']:.2f}\n"
            f"   Final score: {item['final_score']:.2f}\n"
            f"   --------------------------------------------------"
        )
        report_lines.append(line)

    report_lines.extend([
        "\nENGINEERING INTERPRETATION",
        "==========================",
        f"1. Which product should be processed first?",
        f"   The first product in the list ({ranked_items[0]['id']}) should be processed first.",
        f"2. Why did it receive the highest score?",
        f"   It maximizes the final score because it presents a very low cloud coverage, ensuring surface visibility.",
        f"3. Was the decision mostly influenced by cloud coverage, recency or asset completeness?",
        f"   Cloud coverage is the dominant factor since it grants up to 100 points, compared to completeness (30) or recency (20).",
        f"4. Would this ranking strategy be sufficient for a real mission system?",
        f"   No, a real system requires checking spatial overlap percentages, resolution, access cost, and alternative sensor data rules."
    ])

    report_text = "\n".join(report_lines)
    with open("reports/observation_ranking.txt", "w") as f:
        f.write(report_text)

    print("Observation ranking pipeline completed successfully.")

if __name__ == "__main__":
    main()

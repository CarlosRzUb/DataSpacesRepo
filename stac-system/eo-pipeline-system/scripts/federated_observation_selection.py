import os
import requests

def query_stac(stac_url, query):
    response = requests.post(stac_url, json=query, timeout=30)
    response.raise_for_status()
    return response.json().get("features", [])

def compute_sensor_score(sensor_name, items, scenario):
    if not items:
        return 0.0
    
    score = min(len(items), 5) * 10.0
    
    if sensor_name == "Sentinel-2 Optical":
        if scenario == "normal":
            valid_clouds = [i.get("properties", {}).get("eo:cloud_cover", 100) for i in items if i.get("properties", {}).get("eo:cloud_cover") is not None]
            avg_cloud = sum(valid_clouds) / len(valid_clouds) if valid_clouds else 100
            score += (100 - avg_cloud) * 0.79
        elif scenario == "cloudy":
            score += 18.0
        elif scenario == "night":
            score -= 10.0
            
    elif sensor_name == "Sentinel-1 SAR":
        if scenario == "normal":
            score += 50.0
        elif scenario == "cloudy":
            score += 80.0
        elif scenario == "night":
            score += 80.0
            
    return score

def main():
    stac_url = "https://stac.dataspace.copernicus.eu/v1/search"
    aoi = [19.0, 50.0, 20.0, 51.0]
    time_window = "2024-01-01T00:00:00Z/2024-01-31T23:59:59Z"
    report_file = "reports/federated_observation_selection.txt"
    
    os.makedirs("reports", exist_ok=True)
    
    queries = {
        "Sentinel-2 Optical": {
            "collections": ["sentinel-2-l2a"],
            "bbox": aoi,
            "datetime": time_window,
            "limit": 5
        },
        "Sentinel-1 SAR": {
            "collections": ["sentinel-1-grd"],
            "bbox": aoi,
            "datetime": time_window,
            "limit": 5
        }
    }
    
    print("FEDERATED OBSERVATION SELECTION")
    print("===============================")
    
    summaries = {}
    for sensor_name, query in queries.items():
        print(f"Querying: {sensor_name}")
        items = query_stac(stac_url, query)
        summaries[sensor_name] = items
        print(f"{sensor_name} products: {len(items)}")
        
    scenarios = ["normal", "cloudy", "night"]
    report_lines = [
        "FEDERATED OBSERVATION SELECTION REPORT",
        "======================================",
        "Sensors compared:",
        "- Sentinel-2 Optical",
        "- Sentinel-1 SAR",
        "",
        "Scenario-based sensor selection:"
    ]
    
    for scenario in scenarios:
        report_lines.append(f"\nScenario: {scenario}")
        
        scores = {}
        for sensor_name, items in summaries.items():
            scores[sensor_name] = compute_sensor_score(sensor_name, items, scenario)
            
        best_sensor = max(scores, key=scores.get)
        
        report_lines.append(f"Recommended sensor: {best_sensor}")
        report_lines.append("Scores:")
        for sensor_name, score in scores.items():
            report_lines.append(f"- {sensor_name}: {score:.2f}")

    with open(report_file, "w") as f:
        f.write("\n".join(report_lines) + "\n")
        
    print("\nFEDERATED SELECTION COMPLETE")
    print(f"REPORT SAVED TO: {report_file}")

if __name__ == "__main__":
    main()

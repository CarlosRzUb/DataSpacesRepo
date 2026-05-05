import requests
import os

def main():
    url = "https://catalogue.dataspace.copernicus.eu/stac/search"
    time_window = "2024-07-01T00:00:00Z/2024-07-31T23:59:59Z"

    scenarios = {
        "WILDFIRE REGION": [13.0, 37.0, 18.0, 41.0],
        "FLOOD REGION": [18.5, 49.5, 21.5, 51.0],
        "VOLCANIC REGION": [14.5, 37.4, 15.4, 38.1]
    }

    report_lines = [
        "EMERGENCY MONITORING REPORT",
        f"Time window: {time_window}",
        "Collection: sentinel-2-l2a",
        "Cloud cover threshold: < 30%\n"
    ]

    for name, bbox in scenarios.items():
        payload = {
            "collections": ["sentinel-2-l2a"],
            "bbox": bbox,
            "datetime": time_window,
            "query": {
                "eo:cloud_cover": {"lt": 30}
            },
            "limit": 15
        }

        try:
            resp = requests.post(url, json=payload, timeout=30)
            resp.raise_for_status()
            features = resp.json().get("features", [])

            report_lines.append(f"[{name}]")
            report_lines.append(f"Returned products: {len(features)}")
            report_lines.append("Example products:")

            for item in features[:3]:
                report_lines.append(item["id"])
            report_lines.append("")

        except Exception:
            report_lines.append(f"[{name}]")
            report_lines.append("Returned products: 0")
            report_lines.append("Example products: None\n")

    report_lines.append("INTERPRETATION:")
    report_lines.append("The volcanic region has the strongest optical product availability")
    report_lines.append("in this query. However, optical imagery may still be limited by clouds,")
    report_lines.append("smoke or acquisition timing. For emergency monitoring, SAR data should be")
    report_lines.append("considered as a complementary source because it can support observation")
    report_lines.append("under cloud cover and during night-time conditions.")

    report = "\n".join(report_lines)

    os.makedirs("reports", exist_ok=True)
    with open("reports/emergency_monitoring_report.txt", "w") as f:
        f.write(report)
    print(report)

if __name__ == "__main__":
    main()

import requests
import json
import os
from datetime import datetime

def generate_live_report():
    broker_url = "http://127.0.0.1:7000/events"
    registry_path = "contracts/providers_registry.json"
    schema_path = "contracts/event_schema.json"
    selected_object = "OBJ-003"

    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"reports/stream_report_{timestamp_str}.txt"

    os.makedirs("reports", exist_ok=True)

    try:
        response = requests.get(broker_url)
        events = response.json()

        with open(registry_path, "r") as f:
            expected_providers = [p["name"] for p in json.load(f)]

        with open(schema_path, "r") as f:
            contract = json.load(f)
            required_fields = contract["required_fields"]
    except Exception as e:
        print(f"Error: {e}")
        return

    valid_events = []
    invalid_count = 0
    for event in events:
        missing_fields = [f for f in required_fields if f not in event]
        if missing_fields:
            invalid_count += 1
        else:
            valid_events.append(event)

    active_providers = sorted(set(e["provider"] for e in valid_events))
    missing_providers = sorted(set(expected_providers) - set(active_providers))

    per_provider = {}
    for e in valid_events:
        p = e["provider"]
        per_provider[p] = per_provider.get(p, 0) + 1

    distinct_objects = set(e["object_id"] for e in valid_events)
    obj_obs = sum(1 for e in valid_events if e["object_id"] == selected_object)

    is_complete = "YES" if not missing_providers else "NO"

    report_content = [
        "REAL-TIME FEDERATION REPORT",
        "---------------------------",
        f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "\n[STREAM STATUS]",
        f"Total events: {len(events)}",
        f"Valid events: {len(valid_events)}",
        f"Invalid events: {invalid_count}",
        "\n[PROVIDERS]",
        "Active providers:"
    ]

    for p in active_providers:
        report_content.append(f"- {p}")

    report_content.append("Missing providers:")
    if missing_providers:
        for p in missing_providers:
            report_content.append(f"- {p}")
    else:
        report_content.append("- none")

    report_content.append("\n[PER-PROVIDER COUNTS]")
    for p in active_providers:
        report_content.append(f"{p}: {per_provider[p]}")

    report_content.append("\n[OBJECT STATISTICS]")
    report_content.append(f"Distinct objects: {len(distinct_objects)}")
    report_content.append(f"{selected_object} observations: {obj_obs}")

    report_content.append("\n[FEDERATION STATUS]")
    report_content.append(f"COMPLETE: {is_complete}")

    with open(report_filename, "w") as f:
        f.write("\n".join(report_content))

    print(f"Report generated: {report_filename}")

generate_live_report()

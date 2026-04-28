import requests
import time
import json

BROKER_EVENTS_URL = "http://127.0.0.1:7000/events"
REGISTRY_PATH = "contracts/providers_registry.json"
SCHEMA_PATH = "contracts/event_schema.json"

TEMP_THRESHOLD = 28.0
VEL_THRESHOLD = 15000.0
ALERT_OBJECT = "OBJ-003"
WINDOW_SIZE = 5

while True:
    try:
        response = requests.get(BROKER_EVENTS_URL)
        events = response.json()

        with open(REGISTRY_PATH, "r") as f:
            expected_providers = [p["name"] for p in json.load(f)]

        with open(SCHEMA_PATH, "r") as f:
            contract = json.load(f)
            required_fields = contract["required_fields"]
    except Exception as e:
        print(f"Error loading resources: {e}")
        time.sleep(3)
        continue

    valid_count = 0
    invalid_count = 0
    duplicate_count = 0
    valid_events = []
    seen_ids = set()

    for event in events:
        missing = [field for field in required_fields if field not in event]
        if missing:
            print(f"INVALID EVENT DETECTED: Missing {missing}")
            invalid_count += 1
            continue

        event_id = (event['provider'], event['timestamp'], event['object_id'])
        if event_id in seen_ids:
            duplicate_count += 1
            continue

        seen_ids.add(event_id)
        valid_count += 1
        valid_events.append(event)

    print(f"VALID EVENTS: {valid_count}")
    print(f"INVALID EVENTS: {invalid_count}")
    print(f"DUPLICATE EVENTS: {duplicate_count}")

    active_providers = sorted(set(event["provider"] for event in valid_events))
    observed_objects = sorted(set(event["object_id"] for event in valid_events))
    missing_providers = sorted(set(expected_providers) - set(active_providers))
    is_complete = "YES" if len(missing_providers) == 0 else "NO"

    print("\nEXPECTED PROVIDERS:")
    for p in expected_providers: print(p)

    print("\nACTIVE PROVIDERS:")
    for p in active_providers: print(p)

    print("\nMISSING PROVIDERS:")
    if missing_providers:
        for p in missing_providers: print(p)
    else:
        print("none")

    print(f"\nCOMPLETE: {is_complete}")

    print("\n[STATISTICS - VALID UNIQUE EVENTS]")
    per_provider = {}
    for event in valid_events:
        p = event["provider"]
        per_provider[p] = per_provider.get(p, 0) + 1

    for p in active_providers:
        print(f"{p}: {per_provider[p]}")

    selected_count = sum(1 for event in valid_events if event["object_id"] == ALERT_OBJECT)
    print(f"DISTINCT OBJECTS: {len(observed_objects)}")
    print(f"OBSERVATIONS FOR {ALERT_OBJECT}: {selected_count}")

    window = valid_events[-WINDOW_SIZE:] if valid_events else []
    print(f"\n--- LIVE ALERTS (LAST {len(window)} EVENTS) ---")

    for event in window:
        if event['object_id'] == ALERT_OBJECT:
            print(f"ALERT: {event['object_id']} observed by {event['provider']} at {event['timestamp']}")

        if event['temperature'] > TEMP_THRESHOLD:
            print(f"WARNING: High Temperature ({event['temperature']}) from {event['provider']} for {event['object_id']}")
        if event['velocity'] > VEL_THRESHOLD:
            print(f"WARNING: High Velocity ({event['velocity']}) from {event['provider']} for {event['object_id']}")

    if valid_events:
        print(f"\nMOST RECENT VALID EVENT TIMESTAMP: {valid_events[-1]['timestamp']}")

    print("-" * 50)
    time.sleep(3)

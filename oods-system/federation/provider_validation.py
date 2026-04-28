import json
import requests

def run_validation():
    registry_path = "contracts/providers_registry.json"
    schema_path = "contracts/observation_schema.json"

    try:
        with open(registry_path, "r") as f:
            providers = json.load(f)
        with open(schema_path, "r") as f:
            contract = json.load(f)
    except FileNotFoundError:
        return

    required_fields = contract["required_fields"]

    stats = {
        "OK": 0,
        "VIOLATION": 0,
        "UNAVAILABLE": 0,
        "EMPTY DATASET": 0
    }
    problematic_providers = []

    for provider in providers:
        name = provider["name"]
        url = provider["url"]
        status = ""

        try:
            response = requests.get(f"{url}/observations", timeout=2)
            data = response.json()

            if not data:
                status = "EMPTY DATASET"
            else:
                missing = [field for field in required_fields if field not in data[0]]
                if missing:
                    status = "VIOLATION"
                else:
                    status = "OK"
        except Exception:
            status = "UNAVAILABLE"

        print(f"{name}: {status}")
        stats[status] += 1
        if status != "OK":
            problematic_providers.append(name)

    print("\nSUMMARY:")
    for key, count in stats.items():
        print(f"{key}: {count}")

    print("\nPROBLEMATIC PROVIDERS:")
    if problematic_providers:
        for p in problematic_providers:
            print(p)
    else:
        print("none")

    state = "RELIABLE" if stats["OK"] == len(providers) else "DEGRADED"
    print(f"FEDERATION STATE: {state}")

if __name__ == "__main__":
    run_validation()

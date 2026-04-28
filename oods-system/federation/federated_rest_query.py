import json
import requests

def run_object_federation():
    registry_path = "contracts/providers_registry.json"
    object_id = "OBJ-003"

    try:
        with open(registry_path, "r") as f:
            providers = json.load(f)
    except FileNotFoundError:
        print(f"Error: {registry_path} not found.")
        return

    results = []
    providers_with_data = []
    providers_no_data = []
    providers_unavailable = []

    full_registry_names = [p["name"] for p in providers]

    for provider in providers:
        name = provider["name"]
        url = provider["url"]

        try:
            response = requests.get(f"{url}/observations/{object_id}", timeout=2)
            if response.status_code == 200:
                data = response.json()
                if data:
                    providers_with_data.append(name)
                    for row in data:
                        row["provider"] = name
                        results.append(row)
                else:
                    providers_no_data.append(name)
            else:
                providers_unavailable.append(name)
        except Exception:
            providers_unavailable.append(name)

    print(f"OBJECT: {object_id}")
    print(f"TOTAL OBSERVATIONS: {len(results)}")

    print("PROVIDERS CONTAINING OBJECT:")
    if providers_with_data:
        for name in providers_with_data:
            print(name)
    else:
        print("none")

    print("MISSING PROVIDERS:")
    missing = [p for p in full_registry_names if p not in providers_with_data]
    if missing:
        for name in missing:
            status = "(no data)" if name in providers_no_data else "(unavailable)"
            print(f"{name} {status}")
    else:
        print("none")

    is_complete = "YES" if len(missing) == 0 else "NO"
    print(f"COMPLETENESS: {is_complete}")

if __name__ == "__main__":
    run_object_federation()

import json
import requests
import duckdb
from datetime import datetime
import os

def generate_report():
    registry_path = "contracts/providers_registry.json"
    schema_path = "contracts/observation_schema.json"
    object_id = "OBJ-003"
    timestamp = datetime.now().strftime("%Y%m%d_%HH%MM%SS")
    report_path = f"reports/federated_access_report_{timestamp}.txt"
    
    os.makedirs("reports", exist_ok=True)

    with open(registry_path, "r") as f:
        providers = json.load(f)
    with open(schema_path, "r") as f:
        contract = json.load(f)
    
    required_fields = contract["required_fields"]
    
    report_lines = []
    report_lines.append("FEDERATED ACCESS REPORT")
    report_lines.append("-----------------------")
    report_lines.append(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    report_lines.append("\n[REGISTERED PROVIDERS]")
    for p in providers:
        report_lines.append(f"- {p['name']}")

    availability = {}
    validation = {}
    all_observations = []
    obj_providers = []
    
    for p in providers:
        name = p['name']
        url = p['url']
        try:
            res = requests.get(f"{url}/observations", timeout=2)
            if res.status_code == 200:
                availability[name] = "AVAILABLE"
                data = res.json()
                
                missing = [f for f in required_fields if f not in (data[0] if data else [])]
                validation[name] = "OK" if not missing and data else "VIOLATION"
                
                for row in data:
                    all_observations.append(row)
                    if row['object_id'] == object_id and name not in obj_providers:
                        obj_providers.append(name)
            else:
                availability[name] = "UNAVAILABLE"
                validation[name] = "N/A"
        except:
            availability[name] = "UNAVAILABLE"
            validation[name] = "N/A"

    report_lines.append("\n[PROVIDER STATUS]")
    for name, status in availability.items():
        report_lines.append(f"{name}: {status}")

    report_lines.append("\n[CONTRACT VALIDATION]")
    for name, status in validation.items():
        report_lines.append(f"{name}: {status}")

    total_obs = len(all_observations)
    distinct_objs = len(set(row['object_id'] for row in all_observations))
    report_lines.append("\n[GLOBAL STATISTICS]")
    report_lines.append(f"Total observations: {total_obs}")
    report_lines.append(f"Distinct objects: {distinct_objs}")

    obj_obs_count = sum(1 for row in all_observations if row['object_id'] == object_id)
    report_lines.append(f"\n[OBJECT ANALYSIS: {object_id}]")
    report_lines.append("Providers containing object:")
    for op in obj_providers:
        report_lines.append(f"- {op}")
    report_lines.append(f"Total observations: {obj_obs_count}")

    # SQL Result
    try:
        sql_res = duckdb.query(f"""
            SELECT COUNT(*) FROM (
                SELECT * FROM 'http://127.0.0.1:8001/observations.csv'
                UNION ALL
                SELECT * FROM 'http://127.0.0.1:8002/observations.csv'
                UNION ALL
                SELECT * FROM 'http://127.0.0.1:8003/observations.csv'
            )
        """).fetchone()[0]
    except:
        sql_res = "ERROR"

    # GraphQL Result
    try:
        gql_query = "{ observations { provider } }"
        gql_res = len(requests.post("http://127.0.0.1:9000/graphql", json={'query': gql_query}).json()['data']['observations'])
    except:
        gql_res = "ERROR"

    report_lines.append("\n[ACCESS LAYERS]")
    report_lines.append(f"REST RESULT: {total_obs}")
    report_lines.append(f"DUCKDB RESULT: {sql_res}")
    report_lines.append(f"GRAPHQL RESULT: {gql_res}")

    is_complete = "YES" if len(obj_providers) == len(providers) else "NO"
    report_lines.append("\n[COMPLETENESS]")
    report_lines.append(f"Federation complete: {is_complete}")

    with open(report_path, "w") as f:
        f.write("\n".join(report_lines))
    
    print(f"Report generated at: {report_path}")

if __name__ == "__main__":
    generate_report()

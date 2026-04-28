import requests

def run_task():
    url_a = "http://127.0.0.1:8001"
    url_b = "http://127.0.0.1:8002"
    object_id = "OBJ-003"

    try:
        res_a_all = requests.get(f"{url_a}/observations")
        data_a_all = res_a_all.json()
        
        res_a_obj = requests.get(f"{url_a}/observations/{object_id}")
        data_a_obj = res_a_obj.json()

        res_b_obj = requests.get(f"{url_b}/observations/{object_id}")
        data_b_obj = res_b_obj.json()

        print("satellite_A:")
        print(f"NUMBER OF OBSERVATIONS: {len(data_a_all)}")
        print(f"{object_id} RESULTS: {len(data_a_obj)}")

        print("\nsatellite_B:")
        print(f"{object_id} RESULTS: {len(data_b_obj)}")

        print("\nCOMPARISON:")
        count_a = len(data_a_obj)
        count_b = len(data_b_obj)

        if count_a > 0 and count_b > 0:
            print(f"{object_id} is present in both providers.")
        elif count_a > 0:
            print(f"{object_id} is only present in satellite_A.")
        elif count_b > 0:
            print(f"{object_id} is only present in satellite_B.")
        else:
            print(f"{object_id} is not present in any provider.")

    except requests.exceptions.ConnectionError:
        print("Error: Connection refused.")

if __name__ == "__main__":
    run_task()

import os
import numpy as np
import matplotlib.pyplot as plt

def create_sample_observation(name, vegetation_level, output_dir):
    width, height = 300, 300
    red_mean = 1200
    nir_mean = 2600 if vegetation_level == "low" else (3400 if vegetation_level == "medium" else 4300)
    
    red = np.random.normal(red_mean, 250, (height, width))
    nir = np.random.normal(nir_mean, 500, (height, width))
    
    return red, nir

def compute_ndvi(red, nir):
    return (nir - red) / (nir + red + 1e-6)

def save_ndvi_map(ndvi, output_path, title):
    plt.figure(figsize=(6, 5))
    plt.imshow(ndvi, cmap="YlGn")
    plt.colorbar(label="NDVI")
    plt.title(title)
    plt.savefig(output_path)
    plt.close()

def main():
    output_dir = "results/ndvi_timeseries"
    report_file = "reports/time_series_ndvi_monitoring.txt"
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    observations = [
        {"date": "2024-04-01", "name": "observation_2024_04_01", "level": "low"},
        {"date": "2024-05-01", "name": "observation_2024_05_01", "level": "medium"},
        {"date": "2024-06-01", "name": "observation_2024_06_01", "level": "high"}
    ]

    dates = []
    mean_values = []
    report_lines = ["TIME-SERIES NDVI MONITORING REPORT", "==========="]

    for obs in observations:
        red, nir = create_sample_observation(obs["name"], obs["level"], output_dir)
        ndvi = compute_ndvi(red, nir)
        
        mean_ndvi = float(ndvi.mean())
        dates.append(obs["date"])
        mean_values.append(mean_ndvi)
        
        map_path = f"{output_dir}/{obs['name']}_ndvi_map.png"
        save_ndvi_map(ndvi, map_path, f"NDVI Map: {obs['date']}")
        
        report_lines.append(obs["date"])
        report_lines.append(f"Mean NDVI: {mean_ndvi:.2f}")

    plt.figure(figsize=(8, 5))
    months = ["Apr", "May", "Jun"]
    plt.plot(months, mean_values, marker="o", linestyle="-", color="green")
    plt.title("Mean NDVI Trend")
    plt.ylabel("Mean NDVI")
    plt.ylim(0, 0.8)
    plt.grid(True, linestyle="--", alpha=0.7)
    trend_path = f"{output_dir}/mean_ndvi_trend.png"
    plt.savefig(trend_path)
    plt.close()

    first_mean = mean_values[0]
    last_mean = mean_values[-1]
    change = last_mean - first_mean

    if change > 0.05:
        trend = "Increasing vegetation activity"
    elif change < -0.05:
        trend = "Decreasing vegetation activity"
    else:
        trend = "Stable vegetation conditions"

    report_lines.extend([
        "Vegetation trend:",
        f"First mean NDVI: {first_mean:.2f}",
        f"Last mean NDVI: {last_mean:.2f}",
        f"Change: {change:+.2f}",
        "Detected trend:",
        trend,
        "===="
    ])

    with open(report_file, "w") as f:
        f.write("\n".join(report_lines))

    print("TIME-SERIES NDVI MONITORING COMPLETE")
    print("Generated files:")
    print(f"  {output_dir}/observation_2024_04_01_ndvi_map.png")
    print(f"  {output_dir}/observation_2024_05_01_ndvi_map.png")
    print(f"  {output_dir}/observation_2024_06_01_ndvi_map.png")
    print(f"  {output_dir}/mean_ndvi_trend.png")
    print(f"  {report_file}")

if __name__ == "__main__":
    main()

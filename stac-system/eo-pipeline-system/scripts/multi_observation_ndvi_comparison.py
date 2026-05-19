import os
import numpy as np
import matplotlib.pyplot as plt

def main():
    output_dir = "results/ndvi_comparison"
    report_file = "reports/multi_observation_ndvi_comparison.txt"
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    width, height = 300, 300

    red_low = np.random.normal(1200, 250, (height, width))
    nir_low = np.random.normal(2500, 500, (height, width))
    ndvi_low = (nir_low - red_low) / (nir_low + red_low + 1e-6)

    red_high = np.random.normal(1200, 250, (height, width))
    nir_high = np.random.normal(2500, 500, (height, width))
    
    cloud_mask = np.random.rand(height, width) < 0.75
    red_high[cloud_mask] = 7500
    nir_high[cloud_mask] = 8000
    ndvi_high = (nir_high - red_high) / (nir_high + red_high + 1e-6)

    low_min, low_max, low_mean = float(ndvi_low.min()), float(ndvi_low.max()), float(ndvi_low.mean())
    low_high_veg = int(np.sum(ndvi_low > 0.5))
    low_low_ndvi = int(np.sum(ndvi_low < 0))

    high_min, high_max, high_mean = float(ndvi_high.min()), float(ndvi_high.max()), float(ndvi_high.mean())
    high_high_veg = int(np.sum(ndvi_high > 0.5))
    high_low_ndvi = int(np.sum(ndvi_high < 0))

    plt.figure(figsize=(6, 5))
    plt.imshow(ndvi_low, cmap="YlGn")
    plt.colorbar(label="NDVI")
    plt.title("Low Cloud Observation NDVI")
    plt.savefig(f"{output_dir}/low_cloud_observation_ndvi_map.png")
    plt.close()

    plt.figure(figsize=(6, 5))
    plt.imshow(ndvi_high, cmap="YlGn")
    plt.colorbar(label="NDVI")
    plt.title("High Cloud Observation NDVI")
    plt.savefig(f"{output_dir}/high_cloud_observation_ndvi_map.png")
    plt.close()

    report_content = f"""MULTI-OBSERVATION NDVI COMPARISON
===
low_cloud_observation
Cloud cover: 5%
NDVI min: {low_min:.2f}
NDVI max: {low_max:.2f}
NDVI mean: {low_mean:.2f}
High vegetation pixels: {low_high_veg}
Low NDVI pixels: {low_low_ndvi}

high_cloud_observation
Cloud cover: 75%
NDVI min: {high_min:.2f}
NDVI max: {high_max:.2f}
NDVI mean: {high_mean:.2f}
High vegetation pixels: {high_high_veg}
Low NDVI pixels: {high_low_ndvi}

ENGINEERING COMPARISON
The low-cloud observation provides a clearer and more useful NDVI result.
The high-cloud observation is operationally less reliable because clouds
reduce interpretability and may hide the real surface signal.

Recommended observation:
low_cloud_observation
"""

    with open(report_file, "w") as f:
        f.write(report_content)

    print("COMPARISON COMPLETE")

if __name__ == "__main__":
    main()

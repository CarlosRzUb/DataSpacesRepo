import os
import numpy as np
import matplotlib.pyplot as plt

ndvi_path = "results/ndvi/ndvi.npy"
output_image = "results/ndvi/ndvi_map.png"
report_file = "reports/ndvi_analysis.txt"

os.makedirs("results/ndvi", exist_ok=True)
os.makedirs("reports", exist_ok=True)

if not os.path.exists(ndvi_path):
    print(f"Error: {ndvi_path} not found.")
    exit(1)

ndvi = np.load(ndvi_path)

ndvi_min = float(ndvi.min())
ndvi_max = float(ndvi.max())
ndvi_mean = float(ndvi.mean())

high_veg_pixels = int(np.sum(ndvi > 0.5))
low_ndvi_pixels = int(np.sum(ndvi < 0))
total_pixels = int(ndvi.size)

high_veg_percent = (high_veg_pixels / total_pixels) * 100
low_ndvi_percent = (low_ndvi_pixels / total_pixels) * 100

plt.figure(figsize=(8, 6))
plt.imshow(ndvi, cmap="YlGn")
plt.colorbar(label="NDVI Index")
plt.title("NDVI Vegetation Map")
plt.savefig(output_image)
plt.close()

report_content = f"""NDVI ANALYSIS REPORT
====================
Input File: {ndvi_path}
Generated Image: {output_image}

STATISTICS:
NDVI Minimum: {ndvi_min:.4f}
NDVI Maximum: {ndvi_max:.4f}
NDVI Mean: {ndvi_mean:.4f}
High Vegetation Pixels (NDVI > 0.5): {high_veg_pixels} ({high_veg_percent:.2f}%)
Low NDVI Pixels (NDVI < 0): {low_ndvi_pixels} ({low_ndvi_percent:.2f}%)

ENGINEERING INTERPRETATION:
1. Vegetated areas correspond to pixels with high NDVI values, driven by strong NIR reflection.
2. Non-vegetated surfaces or bare soil correspond to intermediate or lower positive values.
3. Low or negative NDVI values typically represent water, deep shadows, or high-reflectance artifacts like clouds.
4. No direct cloud contamination can be confirmed in this test because the input spectral bands were synthetically generated for pipeline validation.
"""

with open(report_file, "w") as f:
    f.write(report_content)

print("NDVI VISUALIZATION")
print("==================")
print(f"NDVI MIN: {ndvi_min:.4f}")
print(f"NDVI MAX: {ndvi_max:.4f}")
print(f"NDVI MEAN: {ndvi_mean:.4f}")
print(f"HIGH VEGETATION PIXELS: {high_veg_pixels}")
print(f"LOW NDVI PIXELS: {low_ndvi_pixels}")
print(f"NDVI MAP SAVED TO: {output_image}")
print(f"ANALYSIS REPORT SAVED TO: {report_file}")

import os
import numpy as np
import rasterio

os.makedirs("results/ndvi", exist_ok=True)
os.makedirs("reports", exist_ok=True)

with rasterio.open("assets/bands/B04_10m.tif") as red_src:
    red = red_src.read(1).astype(float)

with rasterio.open("assets/bands/B08_10m.tif") as nir_src:
    nir = nir_src.read(1).astype(float)

ndvi = (nir - red) / (nir + red + 1e-6)

ndvi_min = float(ndvi.min())
ndvi_max = float(ndvi.max())
ndvi_mean = float(ndvi.mean())

high_veg_pixels = int(np.sum(ndvi > 0.5))
low_ndvi_pixels = int(np.sum(ndvi < 0))

np.save("results/ndvi/ndvi.npy", ndvi)

report_content = f"""NDVI PIPELINE REPORT
====================
NDVI MIN: {ndvi_min:.4f}
NDVI MAX: {ndvi_max:.4f}
NDVI MEAN: {ndvi_mean:.4f}
High vegetation pixels (NDVI > 0.5): {high_veg_pixels}
Low NDVI pixels (NDVI < 0): {low_ndvi_pixels}
"""

with open("reports/ndvi_report.txt", "w") as f:
    f.write(report_content)

print(report_content)

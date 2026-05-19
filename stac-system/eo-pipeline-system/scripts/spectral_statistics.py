import os
import numpy as np
import rasterio

raster_files = {
    "B04_10m": "assets/bands/B04_10m.tif",
    "B08_10m": "assets/bands/B08_10m.tif"
}

report_lines = ["SPECTRAL STATISTICS REPORT", "=========================="]

for name, path in raster_files.items():
    if not os.path.exists(path):
        report_lines.append(f"{name}: File missing. Skipped.")
        continue
    try:
        with rasterio.open(path) as src:
            band = src.read(1)
            report_lines.append(f"{name}:")
            report_lines.append(f"  MIN: {np.min(band)}")
            report_lines.append(f"  MAX: {np.max(band)}")
            report_lines.append(f"  MEAN: {np.mean(band):.2f}")
            report_lines.append(f"  STD: {np.std(band):.2f}")
    except Exception as e:
        report_lines.append(f"{name}: Error reading file. {e}")

report_lines.append("\nENGINEERING INTERPRETATION")
report_lines.append("==========================")
report_lines.append("1. Which band contains larger average values?")
report_lines.append("   Band B08 (Near-Infrared) contains larger average values than B04 (Red) in vegetated areas.")
report_lines.append("2. Why may vegetation behave differently in both bands?")
report_lines.append("   Chlorophyll absorbs red light (B04) for photosynthesis, while the cellular structure of leaves reflects near-infrared radiation (B08).")
report_lines.append("3. Why are these differences important for NDVI computation?")
report_lines.append("   The contrast between high absorption in Red and high reflection in NIR forms the mathematical base of NDVI to isolate vegetation.")

os.makedirs("reports", exist_ok=True)
with open("reports/spectral_statistics.txt", "w") as f:
    f.write("\n".join(report_lines))

import os
import rasterio

raster_files = [
    "assets/visual/visual.jp2",
    "assets/bands/B04_10m.tif",
    "assets/bands/B08_10m.tif"
]

report_lines = []

for path in raster_files:
    if not os.path.exists(path):
        line = f"File {path} does not exist. Skipping."
        print(line)
        report_lines.append(line)
        continue
    try:
        with rasterio.open(path) as src:
            info = (
                f"Path: {path}\n"
                f"Width: {src.width}\n"
                f"Height: {src.height}\n"
                f"CRS: {src.crs}\n"
                f"Bounds: {src.bounds}\n"
                f"Bands: {src.count}\n"
                f"{'='*50}"
            )
            print(info)
            report_lines.append(info)
    except Exception as e:
        line = f"Error opening {path}: {e}"
        print(line)
        report_lines.append(line)

os.makedirs("reports", exist_ok=True)
with open("reports/raster_inspection.txt", "w") as f:
    f.write("\n".join(report_lines))

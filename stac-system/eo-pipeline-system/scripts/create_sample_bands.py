import os
import numpy as np
import rasterio
from rasterio.transform import from_origin

os.makedirs("assets/bands", exist_ok=True)

width = 300
height = 300

transform = from_origin(19.0, 51.0, 10, 10)

red = np.random.normal(1200, 250, (height, width)).astype("float32")
nir = np.random.normal(2500, 500, (height, width)).astype("float32")

profile = {
    "driver": "GTiff",
    "height": height,
    "width": width,
    "count": 1,
    "dtype": "float32",
    "crs": "EPSG:4326",
    "transform": transform
}

with rasterio.open("assets/bands/B04_10m.tif", "w", **profile) as dst:
    dst.write(red, 1)

with rasterio.open("assets/bands/B08_10m.tif", "w", **profile) as dst:
    dst.write(nir, 1)

print("Sample bands created successfully.")

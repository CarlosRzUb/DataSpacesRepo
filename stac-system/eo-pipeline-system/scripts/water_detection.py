import os
import numpy as np
import matplotlib.pyplot as plt

def main():
    ndvi_path = "results/ndvi/ndvi.npy"
    mask_npy_output = "results/ndvi/water_mask.npy"
    mask_png_output = "results/ndvi/water_mask.png"
    report_file = "reports/water_detection.txt"
    
    print("WATER DETECTION")
    print("Loading NDVI...")
    
    if not os.path.exists(ndvi_path):
        print(f"Error: {ndvi_path} not found. Run previous tasks first.")
        return

    ndvi = np.load(ndvi_path)
    
    print("Generating binary mask...")
    water_mask = ndvi < 0
    
    water_pixels = int(np.sum(water_mask))
    total_pixels = int(ndvi.size)
    non_water_pixels = total_pixels - water_pixels
    water_percentage = (water_pixels / total_pixels) * 100
    
    print(f"Water candidate pixels: {water_pixels}")
    print(f"Non-water pixels: {non_water_pixels}")
    
    np.save(mask_npy_output, water_mask)
    
    plt.figure(figsize=(10, 8))
    plt.imshow(water_mask, cmap="Blues")
    plt.colorbar(label="Water Mask (True/False)")
    plt.title("Surface Water Candidate Mask")
    plt.savefig(mask_png_output)
    plt.close()
    
    report_content = f"""WATER DETECTION REPORT
===
Detection rule:
NDVI < 0

Pixel statistics:
Water candidate pixels: {water_pixels}
Non-water pixels: {non_water_pixels}
Water candidate percentage: {water_percentage:.2f}%

Interpretation:
Small number of low-NDVI areas detected.
Potential explanations:
water surfaces
shadows
urban regions
"""
    
    os.makedirs("reports", exist_ok=True)
    with open(report_file, "w") as f:
        f.write(report_content)
        
    print("\nFILES GENERATED:")
    print(mask_npy_output)
    print(mask_png_output)
    print(report_file)

if __name__ == "__main__":
    main()

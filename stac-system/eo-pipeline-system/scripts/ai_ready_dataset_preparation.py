import os
import json
import shutil

def determine_quality(cloud_cover, mean_ndvi):
    if cloud_cover <= 10 and mean_ndvi >= 0.5:
        return "excellent", "AI_READY"
    elif cloud_cover <= 30 and mean_ndvi >= 0.3:
        return "good", "AI_READY"
    elif cloud_cover <= 70 and mean_ndvi >= 0.1:
        return "limited", "NEEDS_REVIEW"
    return "poor", "REJECTED"

def main():
    images_dir = "dataset/images"
    metadata_dir = "dataset/metadata"
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(metadata_dir, exist_ok=True)

    synthetic_observations = [
        {"id": "OBS_001", "cloud_cover": 5, "mean_ndvi": 0.62, "sensor": "Sentinel-2"},
        {"id": "OBS_002", "cloud_cover": 18, "mean_ndvi": 0.44, "sensor": "Sentinel-2"},
        {"id": "OBS_003", "cloud_cover": 68, "mean_ndvi": 0.21, "sensor": "Sentinel-2"}
    ]

    file_mappings = {
        "OBS_001": [
            ("results/ndvi/ndvi_map.png", "dataset/images/OBS_001_ndvi_map.png"),
            ("results/ndvi/water_mask.png", "dataset/images/OBS_001_water_mask.png")
        ],
        "OBS_002": [
            ("results/ndvi_comparison/low_cloud_observation_ndvi_map.png", "dataset/images/OBS_002_ndvi_map.png")
        ],
        "OBS_003": [
            ("results/ndvi_comparison/high_cloud_observation_ndvi_map.png", "dataset/images/OBS_003_ndvi_map.png")
        ]
    }

    print("AI-READY EO DATASET PREPARATION")
    print("===============================")

    for obs_id, files in file_mappings.items():
        for src, dst in files:
            if os.path.exists(src):
                shutil.copy(src, dst)
                print(f"COPIED: {dst}")
            else:
                print(f"MISSING: {src}")

    print()

    quality_counts = {"excellent": 0, "good": 0, "limited": 0, "poor": 0}

    for obs in synthetic_observations:
        quality, suitability = determine_quality(obs["cloud_cover"], obs["mean_ndvi"])
        
        if quality in quality_counts:
            quality_counts[quality] += 1
            
        selected_assets = [dst for src, dst in file_mappings.get(obs["id"], []) if os.path.exists(src)]

        metadata = {
            "observation_id": obs["id"],
            "sensor": obs["sensor"],
            "cloud_cover": obs["cloud_cover"],
            "mean_ndvi": obs["mean_ndvi"],
            "quality": quality,
            "suitability": suitability,
            "selected_assets": selected_assets,
            "labels": {
                "vegetation_monitoring": suitability,
                "ai_training": suitability,
                "cloud_conditions": "LOW" if obs["cloud_cover"] <= 30 else "HIGH"
            }
        }

        meta_path = f"{metadata_dir}/{obs['id']}.json"
        with open(meta_path, "w") as f:
            json.dump(metadata, f, indent=4)
        print(f"METADATA CREATED: {meta_path}")

    print("\nDATASET SUMMARY")
    print(f"Dataset size: {len(synthetic_observations)}")
    print(f"Excellent: {quality_counts['excellent']}")
    print(f"Good: {quality_counts['good']}")
    print(f"Limited: {quality_counts['limited']}")

    summary = {
        "dataset_size": len(synthetic_observations),
        "images_directory": images_dir,
        "metadata_directory": metadata_dir,
        "quality_distribution": {
            "excellent": quality_counts["excellent"],
            "good": quality_counts["good"],
            "limited": quality_counts["limited"]
        }
    }

    with open(f"{metadata_dir}/dataset_summary.json", "w") as f:
        json.dump(summary, f, indent=4)

    print("\nGENERATED STRUCTURE:")
    print("dataset/")
    print("  images/")
    print("  metadata/")
    print("AI-READY DATASET COMPLETE")

if __name__ == "__main__":
    main()

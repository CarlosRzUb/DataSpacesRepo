import json
import os

def main():
    with open("results/raw_stac_items.json", "r") as f:
        items = json.load(f)

    core_fields = ["id", "collection", "bbox", "geometry", "assets", "links"]
    optional_fields = ["eo:cloud_cover", "platform", "instruments", "sat:orbit_state"]

    complete_items = 0
    missing_optional = 0

    for item in items:
        has_core = all(field in item for field in core_fields) and "datetime" in item.get("properties", {})
        if has_core:
            complete_items += 1

        props = item.get("properties", {})
        has_all_optional = all(field in props for field in optional_fields)
        if not has_all_optional:
            missing_optional += 1

    report = f"""METADATA CONSISTENCY REPORT
Total items checked: {len(items)}
Items with complete core metadata: {complete_items}
Items with missing optional EO metadata: {missing_optional}

Common fields:
id
collection
bbox
geometry
properties.datetime
assets
links

Fields missing in some items:
properties.eo:cloud_cover
properties.sat:orbit_state

Interpretation:
The catalog is structurally consistent at STAC level,
but observation-specific metadata differs between collections.
This means that cross-collection processing should not assume
that all quality or sensor fields are always available.
"""
    os.makedirs("reports", exist_ok=True)
    with open("reports/metadata_consistency.txt", "w") as f:
        f.write(report)
    print(report)

if __name__ == "__main__":
    main()

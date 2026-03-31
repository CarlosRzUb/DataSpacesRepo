#!/bin/bash
for meta in metadata_catalog/*.json
do
    PATH_DATA=$(grep "data_path" "$meta" | cut -d '"' -f4)
    if [ ! -f "$PATH_DATA" ]; then
        echo "Inconsistent: $meta (File not found: $PATH_DATA)"
    elif [ ! -s "$PATH_DATA" ]; then
        echo "Inconsistent: $meta (File is empty: $PATH_DATA)"
    fi
done

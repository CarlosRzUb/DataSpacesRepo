#!/bin/bash
ID=$1
for file in metadata_catalog/*
do
    DATA_LOCATION=$(grep "data_path" "$file" | cut -d '"' -f4)
    if [ -f "$DATA_LOCATION" ]; then
        grep "$ID" "$DATA_LOCATION"
    fi
done

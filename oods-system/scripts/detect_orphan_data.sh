#!/bin/bash
for ds in providers/*/observations.csv
do
    COUNT=$(grep -rc "$ds" metadata_catalog/ | awk -F: '{sum+=$2} END {print sum}')
    if [ "$COUNT" -eq 0 ]; then
        echo "Orphan data: $ds"
    fi
done

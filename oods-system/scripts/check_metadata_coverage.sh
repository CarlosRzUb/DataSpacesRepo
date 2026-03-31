#!/bin/bash
MISSING=$(for ds in providers/*/observations.csv; do
    MATCH=$(grep -l "$ds" metadata_catalog/*.json 2>/dev/null)
    if [ -z "$MATCH" ]; then
        echo "Missing metadata for: $ds"
    fi
done)

if [ -z "$MISSING" ]; then
    echo "All datasets are described in metadata. No issues found."
else
    echo "$MISSING"
fi

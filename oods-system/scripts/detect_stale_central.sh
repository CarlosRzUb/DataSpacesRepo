#!/bin/bash
for ds in providers/*/observations.csv
do
    NAME=$(basename "$(dirname "$ds")")
    CENTRAL="central_repository/${NAME}_observations.csv"
    if [ ! -f "$CENTRAL" ] || ! cmp -s "$ds" "$CENTRAL"; then
        echo "Stale or missing: $NAME"
    fi
done

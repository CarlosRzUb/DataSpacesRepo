#!/bin/bash

ID=${1:-"OBJ-003"}

DIST_RES=$(./scripts/search_distributed.sh "$ID" | tail -n 1 | cut -d' ' -f2)
FED_RES=$(./scripts/search_federated.sh "$ID" 2>/dev/null | grep -c "$ID")

echo "Distributed results: $DIST_RES"
echo "Federated results: $FED_RES"

if [ "$DIST_RES" -eq "$FED_RES" ]; then
    echo "Results are consistent: yes"
else
    echo "Results are consistent: no"
fi

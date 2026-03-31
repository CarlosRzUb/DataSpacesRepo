#!/bin/bash
ID=${1:-"OBJ-003"}
DIST=$(./scripts/search_distributed.sh "$ID" | tail -n 1 | cut -d' ' -f2)
FED=$(./scripts/search_federated.sh "$ID" | grep -c "$ID")
echo "Distributed: $DIST, Federated: $FED"
if [ "$FED" -lt "$DIST" ]; then
    echo "Complete: no"
else
    echo "Complete: yes"
fi

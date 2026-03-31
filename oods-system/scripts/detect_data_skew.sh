#!/bin/bash
COUNTS=$(wc -l providers/*/observations.csv | grep -v "total")
echo "$COUNTS"
MAX_VAL=$(echo "$COUNTS" | awk '{print $1}' | sort -nr | head -n1)
MIN_VAL=$(echo "$COUNTS" | awk '{print $1}' | sort -n | head -n1)
DIFF=$((MAX_VAL - MIN_VAL))
echo "Largest: $(echo "$COUNTS" | sort -nr | head -n1)"
echo "Smallest: $(echo "$COUNTS" | sort -n | head -n1)"
echo "Difference: $DIFF"

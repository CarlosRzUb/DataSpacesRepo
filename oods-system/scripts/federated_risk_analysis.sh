#!/bin/bash
FULL=$(duckdb -noheader -list -c "SELECT COUNT(*) FROM read_csv_auto('providers/*/observations.csv');")
FED=$(duckdb -noheader -list -c "SELECT COUNT(*) FROM read_csv_auto(['providers/satellite_A/observations.csv', 'providers/satellite_B/observations.csv']);")
MISSING=$((FULL - FED))
LOSS=$(duckdb -noheader -list -c "SELECT round(($MISSING.0 / $FULL.0) * 100, 1);")

echo "FULL: $FULL"
echo "FEDERATED: $FED"
echo "MISSING: $MISSING"
echo "LOSS: $LOSS%"

#!/bin/bash
FULL=$(duckdb -noheader -list -c "SELECT COUNT(*) FROM read_csv_auto('providers/*/observations.csv');")
FED=$(duckdb -noheader -list -c "SELECT COUNT(*) FROM read_csv_auto(['providers/satellite_A/observations.csv', 'providers/satellite_B/observations.csv']);")

if [ "$FULL" -eq "$FED" ]; then
    echo "FEDERATED RESULT: COMPLETE"
else
    echo "FEDERATED RESULT: INCOMPLETE"
    echo "MISSING PROVIDERS: ground_station"
fi

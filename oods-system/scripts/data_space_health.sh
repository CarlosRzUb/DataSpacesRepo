#!/bin/bash
SCORE=$(duckdb -noheader -list -c "SELECT COUNT(*) FROM (SELECT object_id FROM read_csv_auto('providers/*/observations.csv', filename=true) GROUP BY object_id HAVING COUNT(DISTINCT filename) = 3);")
TOTAL_OBJ=$(duckdb -noheader -list -c "SELECT COUNT(DISTINCT object_id) FROM read_csv_auto('providers/*/observations.csv');")
FULL=$(duckdb -noheader -list -c "SELECT COUNT(*) FROM read_csv_auto('providers/*/observations.csv');")
FED=$(duckdb -noheader -list -c "SELECT COUNT(*) FROM read_csv_auto(['providers/satellite_A/observations.csv', 'providers/satellite_B/observations.csv']);")

if [ "$SCORE" -eq "$TOTAL_OBJ" ] && [ "$FULL" -eq "$FED" ]; then
    echo "DATA SPACE HEALTH: GOOD"
elif [ "$FULL" -ne "$FED" ]; then
    echo "DATA SPACE HEALTH: WARNING"
    echo "Reason: incomplete coverage and federated loss detected"
else
    echo "DATA SPACE HEALTH: CRITICAL"
fi

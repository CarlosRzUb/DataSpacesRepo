#!/bin/bash
DRIFT=$(duckdb -noheader -list -c "
SELECT 'ground_station has extra column: ' || column_name 
FROM (DESCRIBE SELECT * FROM 'providers/ground_station/observations.csv')
WHERE column_name NOT IN (SELECT column_name FROM (DESCRIBE SELECT * FROM 'providers/satellite_A/observations.csv'));")

if [ -z "$DRIFT" ]; then
    echo "SCHEMA STATUS: CONSISTENT"
else
    echo "SCHEMA DRIFT DETECTED:"
    echo "$DRIFT"
fi

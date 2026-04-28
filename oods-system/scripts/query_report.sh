#!/bin/bash

OBJECT_ID=${1:-"OBJ-003"}
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
REPORT_FILE="./reports/query_report_$TIMESTAMP.txt"
GEN_DATE=$(date +"%Y-%m-%d %H:%M:%S")

mkdir -p ../reports

echo "DATA SPACE QUERY REPORT" > "$REPORT_FILE"
echo "-----------------------" >> "$REPORT_FILE"
echo "Generated at: $GEN_DATE" >> "$REPORT_FILE"

echo -e "\n[GLOBAL STATISTICS]" >> "$REPORT_FILE"

TOTAL_OBS=$(duckdb -noheader -list -c "SELECT COUNT(*) FROM read_csv_auto('providers/*/observations.csv');")
echo "Total observations: $TOTAL_OBS" >> "$REPORT_FILE"

DISTINCT_OBJ=$(duckdb -noheader -list -c "SELECT COUNT(DISTINCT object_id) FROM read_csv_auto('providers/*/observations.csv');")
echo "Distinct objects: $DISTINCT_OBJ" >> "$REPORT_FILE"

echo -e "\n[OBJECT ANALYSIS: $OBJECT_ID]" >> "$REPORT_FILE"
echo "Providers containing object:" >> "$REPORT_FILE"

duckdb -noheader -list -c "
    SELECT DISTINCT replace(replace(filename, 'providers/', ''), '/observations.csv', '') 
    FROM read_csv_auto('providers/*/observations.csv', filename=true) 
    WHERE object_id = '$OBJECT_ID';" | sed 's/^/- /' >> "$REPORT_FILE"

OBJ_COUNT=$(duckdb -noheader -list -c "SELECT COUNT(*) FROM read_csv_auto('providers/*/observations.csv') WHERE object_id = '$OBJECT_ID';")
echo "Total observations: $OBJ_COUNT" >> "$REPORT_FILE"

echo -e "\n[FEDERATED QUERY COMPARISON]" >> "$REPORT_FILE"
echo "FULL RESULT: $OBJ_COUNT" >> "$REPORT_FILE"

FED_COUNT=$(duckdb -noheader -list -c "
    SELECT COUNT(*) 
    FROM read_csv_auto(['providers/satellite_A/observations.csv', 'providers/satellite_B/observations.csv']) 
    WHERE object_id = '$OBJECT_ID';")
echo "FEDERATED RESULT: $FED_COUNT" >> "$REPORT_FILE"

if [ "$OBJ_COUNT" -eq "$FED_COUNT" ]; then
    echo "COMPLETE: YES" >> "$REPORT_FILE"
else
    echo "COMPLETE: NO" >> "$REPORT_FILE"
fi

echo -e "\n[SCHEMA VALIDATION]" >> "$REPORT_FILE"

DIFF_SCHEMA=$(duckdb -noheader -list -c "
    (DESCRIBE SELECT * FROM 'providers/satellite_A/observations.csv')
    EXCEPT
    (DESCRIBE SELECT * FROM 'providers/ground_station/observations.csv');")

if [ -z "$DIFF_SCHEMA" ]; then
    echo "Schema consistency: CONSISTENT" >> "$REPORT_FILE"
else
    echo "Schema consistency: INCONSISTENT" >> "$REPORT_FILE"
fi

echo -e "\nThis report summarizes key aspects of the data space and provides a consolidated view of data availability and quality." >> "$REPORT_FILE"

echo "Report generated: $REPORT_FILE"

#!/bin/bash

REPORT_FILE="reports/data_space_report.txt"
QUERY_ID="OBJ-003"

TOTAL_DATASETS=$(ls providers/*/observations.csv | wc -l)
TOTAL_RECORDS=$(cat providers/*/observations.csv | grep -v "timestamp" | wc -l)
OBJ_COUNT=$(./scripts/search_distributed.sh "$QUERY_ID" | tail -n 1 | cut -d' ' -f2)
CONSISTENCY=$(./scripts/compare_queries.sh "$QUERY_ID" | grep "consistent" | cut -d' ' -f4)

mkdir -p reports

echo "DATA SPACE REPORT" > "$REPORT_FILE"
echo "Total datasets: $TOTAL_DATASETS" >> "$REPORT_FILE"
echo "Total records: $TOTAL_RECORDS" >> "$REPORT_FILE"
echo "Objects found for query $QUERY_ID: $OBJ_COUNT" >> "$REPORT_FILE"
echo "Consistency check: $CONSISTENCY" >> "$REPORT_FILE"

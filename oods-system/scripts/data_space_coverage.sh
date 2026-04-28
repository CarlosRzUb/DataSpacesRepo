#!/bin/bash
TOTAL_OBJ=$(duckdb -noheader -list -c "SELECT COUNT(DISTINCT object_id) FROM read_csv_auto('providers/*/observations.csv');")
FULL_COV=$(duckdb -noheader -list -c "SELECT COUNT(*) FROM (SELECT object_id FROM read_csv_auto('providers/*/observations.csv', filename=true) GROUP BY object_id HAVING COUNT(DISTINCT filename) = 3);")
PARTIAL=$((TOTAL_OBJ - FULL_COV))
SCORE=$(duckdb -noheader -list -c "SELECT round(($FULL_COV.0 / $TOTAL_OBJ.0) * 100, 0);")

echo "TOTAL OBJECTS: $TOTAL_OBJ"
echo "FULL COVERAGE: $FULL_COV"
echo "PARTIAL: $PARTIAL"
echo "COVERAGE SCORE: $SCORE%"

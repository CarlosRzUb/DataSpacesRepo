#!/bin/bash
TOTAL=$(duckdb -noheader -list -c "SELECT COUNT(*) FROM read_csv_auto('providers/*/observations.csv');")
duckdb -noheader -list -c "
SELECT 
    replace(replace(filename, 'providers/', ''), '/observations.csv', '') || ': ' || 
    count(*) || ' (' || round((count(*) * 100.0 / $TOTAL), 0) || '%)'
FROM read_csv_auto('providers/*/observations.csv', filename=true)
GROUP BY filename
ORDER BY count(*) DESC;"
DOMINANT=$(duckdb -noheader -list -c "SELECT replace(replace(filename, 'providers/', ''), '/observations.csv', '') FROM read_csv_auto('providers/*/observations.csv', filename=true) GROUP BY filename ORDER BY count(*) DESC LIMIT 1;")
echo "DOMINANT PROVIDER: $DOMINANT"

#!/bin/bash
THRESHOLD=0.5
duckdb -noheader -list -c "
WITH stats AS (
    SELECT 
        object_id,
        list(replace(replace(filename, 'providers/', ''), '/observations.csv', '') || ': ' || temperature) AS vals,
        max(temperature) - min(temperature) AS diff
    FROM read_csv_auto('providers/*/observations.csv', filename=true)
    GROUP BY object_id
    HAVING count(DISTINCT filename) > 1 AND diff > $THRESHOLD
)
SELECT 
    object_id || ' inconsistency detected (temperature):' || chr(10) || array_to_string(vals, chr(10))
FROM stats;"

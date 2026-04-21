#!/bin/bash
duckdb -noheader -list -c "
WITH object_providers AS (
    SELECT object_id, 
           replace(replace(filename, 'providers/', ''), '/observations.csv', '') AS provider
    FROM read_csv_auto('providers/*/observations.csv', filename=true)
),
all_providers AS (
    SELECT 'satellite_A' AS p UNION SELECT 'satellite_B' UNION SELECT 'ground_station'
)
SELECT 
    op.object_id || ' missing in: ' || string_agg(ap.p, ', ')
FROM (SELECT DISTINCT object_id FROM object_providers) op
CROSS JOIN all_providers ap
LEFT JOIN object_providers match ON op.object_id = match.object_id AND ap.p = match.provider
WHERE match.provider IS NULL
GROUP BY op.object_id;"

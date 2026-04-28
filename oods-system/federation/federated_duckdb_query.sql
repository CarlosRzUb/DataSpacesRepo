SELECT 
    COUNT(*) AS "TOTAL OBSERVATIONS",
    COUNT(*) FILTER (WHERE object_id = 'OBJ-003') AS "OBJ-003 OBSERVATIONS"
FROM (
    SELECT * FROM 'http://127.0.0.1:8001/observations.csv'
    UNION ALL
    SELECT * FROM 'http://127.0.0.1:8002/observations.csv'
    UNION ALL
    SELECT * FROM 'http://127.0.0.1:8003/observations.csv'
);

SELECT 
    provider, 
    COUNT(*) AS count
FROM (
    SELECT 'satellite_A' AS provider, * FROM 'http://127.0.0.1:8001/observations.csv'
    UNION ALL
    SELECT 'satellite_B' AS provider, * FROM 'http://127.0.0.1:8002/observations.csv'
    UNION ALL
    SELECT 'ground_station' AS provider, * FROM 'http://127.0.0.1:8003/observations.csv'
)
GROUP BY provider
ORDER BY count DESC;

SELECT provider, timestamp, object_id, temperature, velocity
FROM (
    SELECT 'satellite_A' AS provider, * FROM 'http://127.0.0.1:8001/observations.csv'
    UNION ALL
    SELECT 'satellite_B' AS provider, * FROM 'http://127.0.0.1:8002/observations.csv'
    UNION ALL
    SELECT 'ground_station' AS provider, * FROM 'http://127.0.0.1:8003/observations.csv'
)
WHERE object_id = 'OBJ-003';

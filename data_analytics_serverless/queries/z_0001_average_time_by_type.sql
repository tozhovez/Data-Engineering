WITH
difference AS(
    SELECT
        vehicle_id,
        vehicle_type,
        LEAD(timestamp/1000) OVER(PARTITION BY days, vehicle_id, vehicle_type ORDER BY timestamp) - timestamp/1000 AS seconds_to_next_measurement
    FROM {ATHENA_DB}.{SENSOR_DATA}
    WHERE sensor_value IS NOT NULL
),
avg_difference AS(
    SELECT
        vehicle_id,
        vehicle_type,
        avg(seconds_to_next_measurement) AS avg_difference_time_btween_measurements
    FROM difference
    -- where seconds_to_next_measurement is not null
    GROUP BY  vehicle_id, vehicle_type
)

SELECT
    vehicle_type,
    avg(avg_difference_time_btween_measurements) AS average_time
FROM avg_difference
GROUP BY  vehicle_type
ORDER BY 1

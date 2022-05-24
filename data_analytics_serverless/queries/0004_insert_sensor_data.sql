INSERT INTO {ATHENA_DB}.{SENSOR_DATA}(
    VEHICLE_ID,
    TIMESTAMP,
    sensor_value,
    -- year, month, day,
    days,
    VEHICLE_TYPE
)
SELECT
c.VEHICLE_ID,
c.TIMESTAMP,
c.sensor_value,
-- CAST(year(from_unixtime(c.timestamp/1000)) as INT) as year,
-- CAST(month(from_unixtime(c.timestamp/1000)) as INT) as month,
-- CAST(day(from_unixtime(c.timestamp/1000)) as INT) as day,
CAST(date(from_unixtime(a.timestamp/1000)) AS date) AS days,
d.VEHICLE_TYPE
FROM (
      SELECT DISTINCT
            a.VEHICLE_ID,
            a.TIMESTAMP,
            a.sensor_value
      FROM {ATHENA_DB}.{RAW_SENSOR_DATA} a
      LEFT JOIN {ATHENA_DB}.{SENSOR_DATA} b
      ON (a.VEHICLE_ID=b.VEHICLE_ID AND a.TIMESTAMP=b.TIMESTAMP AND a.sensor_value=b.sensor_value)
      WHERE b.VEHICLE_ID IS NULL
     ) c
INNER JOIN {ATHENA_DB}.{VEHICLES_DATA} d
ON (c.VEHICLE_ID=d.VEHICLE_ID)
;

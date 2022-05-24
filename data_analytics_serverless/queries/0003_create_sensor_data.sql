CREATE TABLE IF NOT EXISTS {ATHENA_DB}.{SENSOR_DATA}
WITH(
-- partitioned_by=ARRAY['year','month','day', 'VEHICLE_TYPE'],
partitioned_by=ARRAY['days', 'VEHICLE_TYPE'],
format='PARQUET',
write_compression='SNAPPY',
external_location='s3://{S3_BUCKET}/{SENSOR_DATA}/'
) AS
SELECT DISTINCT
a.vehicle_id,
a.timestamp,
a.sensor_value,
CAST(date(from_unixtime(a.timestamp/1000)) as date) as days,
--CAST(year(from_unixtime(a.timestamp/1000)) as INT) as year,
--CAST(month(from_unixtime(a.timestamp/1000)) as INT) as month,
--CAST(day(from_unixtime(a.timestamp/1000)) as INT) as day,
b.VEHICLE_TYPE
FROM {ATHENA_DB}.{RAW_SENSOR_DATA} a
INNER JOIN {ATHENA_DB}.{VEHICLES_DATA} b
on (a.vehicle_id = b.vehicle_id)
-- WHERE b.VEHICLE_TYPE BETWEEN {VEHICLE_TYPE_MIN} AND {VEHICLE_TYPE_MAX}
;

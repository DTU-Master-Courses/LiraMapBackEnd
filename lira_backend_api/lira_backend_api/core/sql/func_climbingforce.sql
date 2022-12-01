-- Main Dev: Wangrandk
-- Supporting Devs: HUIYULEO, Tswagerman
with useful as(
select
	lat,
	lon,
	message,
	row_number() over (partition by date_trunc('second', "TS_or_Distance") order by "TS_or_Distance" desc)
           as row_number
	 FROM public."Measurements"
	where
	"FK_Trip" = '+trip_id+'
	 and
	"T" = 'acc.xyz'
),
--only take one row per. second
useful_second as
(
select *
from useful
where row_number = 1
),

agg as(
SELECT
	message::json->>'@vid' as vid,
	SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',1) as ts_date,
    SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',2)  as ts_time,
-- 	round(avg(cast(message::json->>'acc.xyz.z' as decimal(3,2))), 2) as az,
-- 	round(avg(cast(message::json->>'acc.xyz.y' as decimal(3,2))), 2) as ay,
-- 	round(avg(cast(message::json->>'acc.xyz.x' as decimal(3,2))), 2) as ax,
-- 	avg(lat) as lat,
-- 	avg(lon) as lon
	round(cast(message::json->>'acc.xyz.z' as decimal(3,2)), 2) as az,
	round(cast(message::json->>'acc.xyz.y' as decimal(3,2)), 2) as ay,
	round(cast(message::json->>'acc.xyz.x' as decimal(3,2)), 2) as ax,
	(lat) as lat,
	(lon) as lon
	from useful_second
	),
--calculate outliers
agg_outlier AS
(
select
	*,
-- 	lag(lat,1) over (order by ts_date, ts_time) as previous_lat,
	(lat -lag(lat,1) over (order by ts_date, ts_time)) as diff_previous_lat
	from agg
)
--remove lat lon outliers (threashold: 0.0003) and calculate climbing force
select
vid,
ts_date,
ts_time,
az,
ay,
ax,
lat,
lon,
1584*9.80655 * sin(round(sqrt(power(ax,2) + power(ay,2) + power(az,2)),4)/1000) as ClimbingForce
-- 	sqrt(power(ax,2) + power(ay,2) + power(az,2)) as slop
from agg_outlier
where abs(diff_previous_lat) < 0.0003

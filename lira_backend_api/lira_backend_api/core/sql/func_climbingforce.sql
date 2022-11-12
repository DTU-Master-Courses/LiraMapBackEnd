
with useful as(
select 
	lat,
	lon,
	message
	 FROM public."Measurements"
	where 
	"FK_Trip" = '+trip_id+'
	 and 
	"T" = 'acc.xyz'
	limit 10000
),
agg as(
SELECT	
	message::json->>'@vid' as vid,
	SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',1) as ts_date,
    SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',2)  as ts_time,
	round(avg(cast(message::json->>'acc.xyz.z' as decimal(3,2))), 2) as az,
	round(avg(cast(message::json->>'acc.xyz.y' as decimal(3,2))), 2) as ay,
	round(avg(cast(message::json->>'acc.xyz.x' as decimal(3,2))), 2) as ax,
	avg(lat) as lat, 
	avg(lon) as lon
	from useful
	 	
	group by 
	message::json->>'@vid',
	SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',1), 
    SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',2)	
-- 	LIMIT 100
	)
	
	select 
	*,
	1584*9.80655 * sin(round(sqrt(power(ax,2) + power(ay,2) + power(az,2)),4)/1000) as ClimbingForce
-- 	sqrt(power(ax,2) + power(ay,2) + power(az,2)) as slop
	from agg
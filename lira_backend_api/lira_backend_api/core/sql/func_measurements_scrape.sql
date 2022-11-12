with useful as(
select 
	lat,
	lon,
	message
	 FROM public."Measurements"
	where 
	"FK_Trip" = '2857262b-71db-49df-8db6-a042987bf0eb'
	 and
	("T" = 'obd.spd'
     or 
    "T" = 'obd.spd_veh'
     or 
	"T" = 'acc.xyz')
	and 
	(
	(cast(message::json->>'obd.spd_veh.value' as decimal(6,3)) > 0
	--or cast(message::json->>'obd.spd.value' as decimal(6,3)) > 0
	)
	or 
	cast(message::json->>'acc.xyz.x' as decimal(3,2)) > 0
	)
),
agg as(
SELECT	
	SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',1) as ts_date,
    SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',2)  as ts_time,
	round(avg(cast(message::json->>'acc.xyz.z' as decimal(3,2))), 2) as az,
	round(avg(cast(message::json->>'acc.xyz.y' as decimal(3,2))), 2) as ay,
	round(avg(cast(message::json->>'acc.xyz.x' as decimal(3,2))), 2) as ax,
    round(avg(cast(message::json->>'obd.spd_veh.value' as decimal(6,3))), 2) as speed,
	--round(avg(cast(message::json->>'obd.spd.value' as decimal(6,3))), 2) as speed,
    avg(lat) as lat, 
	avg(lon) as lon
	from useful
	 	
	group by 
	SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',1), 
    SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',2)	
	)
	
	select 
	*,
	sqrt(pow(ax,2) + pow(ay,2)) as magnitude
-- 	sqrt(power(ax,2) + power(ay,2) + power(az,2)) as slop
	from agg
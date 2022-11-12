 SELECT
	"Measurements"."FK_Trip" as tripid,
	SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',1) as ts_date,
    SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',2)  as ts_time,
	-- message::json->>'@t' as rmp_tag,
	avg(public."Measurements".lat) as lat, 
	avg(public."Measurements".lon) as lon,
	avg(cast(message::json->>'obd.rpm_fl.value' as decimal(6,3))) as rpm_fl,
    avg(cast(message::json->>'obd.rpm_rl.value' as decimal(6,3))) as rpm_rl
	FROM public."Measurements"
	where 
	"FK_Trip" =  '+trip_id+' -- '2857262b-71db-49df-8db6-a042987bf0eb' --
	and (message::json->>'obd.rpm_rl.value' is not NULL
	or message::json->>'obd.rpm_fl.value' is not NULL)
	and (cast(message::json->>'obd.rpm_rl.value' as decimal(6,3)) > 0
	or cast(message::json->>'obd.rpm_fl.value' as decimal(6,3)) > 0)
	and public."Measurements".lat is not null
	and public."Measurements".lon is not null
	and ( "T" = 'obd.rpm_rl' or "T" = 'obd.rpm_fl')
	group by
	tripid,
	SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',1), 
    SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',2)
	-- ORDER BY "Measurements"."Created_Date"
	LIMIT 1000; 
 
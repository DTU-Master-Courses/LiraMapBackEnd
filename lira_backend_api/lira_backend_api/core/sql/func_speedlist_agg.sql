 SELECT
	SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',1) as ts_date,
    SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',2)  as ts_time,
	message::json->>'@vid' as vid,

    avg(cast(message::json->>'obd.spd_veh.value' as decimal(6,3))) as speed,
	avg(public."Measurements".lat) as lat,
	avg(public."Measurements".lon) as lon
	FROM public."Measurements"
	where
	"FK_Trip" = '+trip_id+' -- '2857262b-71db-49df-8db6-a042987bf0eb' --
	-- and EXTRACT (YEAR FROM "TS_or_Distance") > 2020
    and message::json->>'obd.spd_veh.value' is not NULL
	and cast(message::json->>'obd.spd_veh.value' as decimal(6,3)) > 0
	and public."Measurements".lat is not null
	and public."Measurements".lon is not null
	and ( "T" = 'obd.spd' or "T" = 'obd.spd_veh')
	group by
	SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',1),
    SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',2) ,

	message::json->>'@vid'
	-- LIMIT 500;

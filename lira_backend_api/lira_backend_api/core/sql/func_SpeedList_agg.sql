
create OR REPLACE FUNCTION  public.func_SpeedList_agg(trip_id uuid)
RETURNS TABLE (ts_date TEXT , ts_time TEXT, vid TEXT, speed NUMERIC(6,3), lat FLOAT,lon FLOAT)
as $$
BEGIN
    RETURN QUERY SELECT	
    --to_date(SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',1), 'yyyy-mm-dd') as ts_date,
    --cast(SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',2) as time) as ts_time,
	SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',1) as ts_date,
    SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',2)  as ts_time,
	message::json->>'@vid' as vid,
	
    avg(cast(message::json->>'obd.spd_veh.value' as decimal(6,3))) as speed,
	avg(public."Measurements".lat) as lat, 
	avg(public."Measurements".lon) as lon
	FROM public."Measurements"
	where 
	"FK_Trip" = trip_id -- '2857262b-71db-49df-8db6-a042987bf0eb' --
	and message::json->>'obd.spd_veh.value' is not NULL
	and cast(message::json->>'obd.spd_veh.value' as decimal(6,3)) > 0
	and public."Measurements".lat is not null
	and public."Measurements".lon is not null
	and ( "T" = 'obd.spd' or "T" = 'obd.spd_veh')
	group by 
	SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',1), 
    SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',2) ,
	message::json->>'@vid'
	LIMIT 500; 
end;$$ LANGUAGE plpgsql;

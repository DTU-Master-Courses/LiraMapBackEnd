create OR REPLACE FUNCTION  public.func_SpeedList(trip_id uuid)
RETURNS TABLE (ts TEXT , vid TEXT, uid TEXT, rec TEXT, speed NUMERIC(6,3), lat REAL,lon REAL)
as $$
BEGIN
    RETURN QUERY SELECT	
	message::json->>'@ts' as ts,
	message::json->>'@vid' as vid,
	message::json->>'@uid' as uid,
    message::json->>'@rec' as rec,
    cast(message::json->>'obd.spd_veh.value' as decimal(6,3)) as speed,
	public."Measurements".lat as lat, 
	public."Measurements".lon as lon
	FROM public."Measurements"
	where 
	"FK_Trip" = trip_id
	and message::json->>'obd.spd_veh.value' is not NULL
	and cast(message::json->>'obd.spd_veh.value' as decimal(6,3)) > 0
	and public."Measurements".lat is not null
	and public."Measurements".lon is not null
	and ( "T" = 'obd.spd' or "T" = 'obd.spd_veh')
	LIMIT 1000;                                                    -- Return the cursor to the caller
end;$$ LANGUAGE plpgsql;

--drop FUNCTION SpeedList(uuid);


	
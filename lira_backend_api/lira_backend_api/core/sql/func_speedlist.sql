SELECT	
	message::json->>'@ts' as ts,
	message::json->>'@vid' as vid,
	message::json->>'@uid' as uid,
    message::json->>'@rec' as rec,
    cast(message::json->>'obd.spd_veh.value' as decimal(6,3)) as speed,
    "Measurements".lon as lon,
	"Measurements".lat as lat 
	FROM "Measurements"
	where 
	"FK_Trip" = '+trip_id+'
	and message::json->>'obd.spd_veh.value' is not NULL
	and cast(message::json->>'obd.spd_veh.value' as decimal(6,3)) > 0
	and "Measurements".lat is not null
	and "Measurements".lon is not null
	and ( "T" = 'obd.spd' or "T" = 'obd.spd_veh')
	LIMIT 1000 


	
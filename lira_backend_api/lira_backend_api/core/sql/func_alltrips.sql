-- Main Dev: Wangrandk
-- Supporting Devs: HUIYULEO, Tswagerman
with useful as(
select
	"TripId" as id,
	"TaskId" AS task_id,
	date_trunc('second', "StartTimeUtc") as start_time_utc,
	date_trunc('second', "EndTimeUtc") as end_time_utc,
	"StartPositionLat" as start_position_lat,
	"StartPositionLng"  as start_position_lng,
	"StartPositionDisplay"::json->>'city' as start_position_city,
	"StartPositionDisplay"::json->>'house_number' as start_position_house_number,
	"StartPositionDisplay"::json->>'county' as start_position_county,
	"StartPositionDisplay"::json->>'state' as start_position_state,
	"StartPositionDisplay"::json->>'postcode' as start_position_postcode,
	"EndPositionLat" as end_position_lat,
	"EndPositionLng"  AS end_position_lng,
	"EndPositionDisplay"::json->>'city' as end_position_city,
	"EndPositionDisplay"::json->>'house_number' as end_position_house_number,
	"EndPositionDisplay"::json->>'county' as end_position_county,
	"EndPositionDisplay"::json->>'state' as end_position_state,
	"EndPositionDisplay"::json->>'postcode' as end_position_postcode,
	date_trunc('second', "Duration") AS duration,
	round(cast("DistanceKm" as decimal(8,4)), 4) AS distance_km,
	"FK_Device" as fk_device,
	"Created_Date" as created_date,
	"Updated_Date" as updated_date,
	"Fully_Imported" as fully_imported
	 FROM public."Trips"
	limit 490
-- 	where
-- 	"TripId" = '2857262b-71db-49df-8db6-a042987bf0eb'-- '+trip_id+'
)
select *
from useful

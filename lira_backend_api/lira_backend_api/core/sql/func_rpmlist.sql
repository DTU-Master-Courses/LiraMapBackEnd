-- Main Dev: HUIYULEO
-- Supporting Devs: Wangrandk, Tswagerman
SELECT
	"Measurements"."FK_Trip" as tripid,
	message::json->>'@ts' as created_date,
--     message::json->>'@t' as rpm_tag,
    "Measurements".lon as lon,
	"Measurements".lat as lat,
	cast(message::json->>'obd.rpm_fl.value' as decimal(6,3)) as rpm_fl,
    cast(message::json->>'obd.rpm_rl.value' as decimal(6,3)) as rpm_rl
	FROM "Measurements"
	where
	"FK_Trip" = '+trip_id+' -- '2857262b-71db-49df-8db6-a042987bf0eb' --
	and (message::json->>'obd.rpm_rl.value' is not NULL
	or message::json->>'obd.rpm_fl.value' is not NULL)
	and (cast(message::json->>'obd.rpm_rl.value' as decimal(6,3)) > 0
	or cast(message::json->>'obd.rpm_fl.value' as decimal(6,3)) > 0)
	and "Measurements".lat is not null
	and "Measurements".lon is not null
	and ( "T" = 'obd.rpm_rl' or "T" = 'obd.rpm_fl')
	ORDER BY "Measurements"."Created_Date"
	LIMIT 1000

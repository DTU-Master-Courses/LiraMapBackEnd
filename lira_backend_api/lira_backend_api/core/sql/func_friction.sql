-- Main Dev: Wangrandk
-- Supporting Devs: HUIYULEO, Tswagerman
with useful as(
select
	"Measurements"."FK_Trip" as tripid,
	lat,
	lon,
	message
	FROM public."Measurements"
	where
	"FK_Trip" = '+trip_id+' -- '2857262b-71db-49df-8db6-a042987bf0eb' --
	and (message::json->>'obd.rpm_rl.value' is not NULL
	or message::json->>'obd.rpm_fl.value' is not NULL)
	and (cast(message::json->>'obd.rpm_rl.value' as decimal(6,3)) > 0
	or cast(message::json->>'obd.rpm_fl.value' as decimal(6,3)) > 0)
	and public."Measurements".lat is not null
	and public."Measurements".lon is not null
	and ( "T" = 'obd.rpm_rl' or "T" = 'obd.rpm_fl')
	ORDER BY "Measurements"."Created_Date"
	limit 10000
),
aggr as(
SELECT
	tripid,
	SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',1) as ts_date,
    SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',2)  as ts_time,
	avg(lat) as lat,
	avg(lon) as lon,
	avg(cast(message::json->>'obd.rpm_fl.value' as decimal(6,3))) as rpm_fl,
	avg(cast(message::json->>'obd.rpm_rl.value' as decimal(6,3))) as rpm_rl
	from useful
	group by
	tripid,
	SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',1),
    SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',2)
	)

	select
	*,
	0.31*rpm_rl as v_func,
	LOG(ABS((3*0.31)/((rpm_fl*0.31)-0.31*rpm_rl))+ 1) as friction
	from aggr


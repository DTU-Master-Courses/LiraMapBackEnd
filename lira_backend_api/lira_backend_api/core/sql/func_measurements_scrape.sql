with useful as(
select 
	lat,
	lon,
	message
	 FROM public."Measurements"
	where 
	"FK_Trip" ='+trip_id+'
	 and
	(
    "T" = 'obd.spd_veh'
     or
	"T" = 'obd.acc_yaw'
	 or 
	"T" = 'obd.acc_long'
	 or
	"T" = 'obd.brk_trq_req_elec'
	 or
	"T" = 'obd.trac_cons'
	 or
	"T" = 'obd.whl_trq_est'
	)
	and 
	(
	cast(message::json->>'obd.spd_veh.value' as decimal(6,3)) > 0
	or 
	cast(message::json->>'obd.acc_yaw.value' as decimal(10,3)) > 0
	or
	cast(message::json->>'obd.acc_long.value' as decimal(10,3)) > 0
	or
	cast(message::json->>'obd.brk_trq_req_elec.value' as decimal(10,3)) > 0
	or
	cast(message::json->>'obd.trac_cons.value' as decimal(10,3)) > 0
	or
	cast(message::json->>'obd.whl_trq_est.value' as decimal(10,3)) > 0
	)
	and 
	SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',2) not like '%+%'
	limit 100000
),
agg as(
SELECT	
	SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',1) as ts_date,
    SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',2)  as ts_time,
	--Coalesce to return 0 when value equals NULL
    COALESCE(round(avg(cast(message::json->>'obd.spd_veh.value' as decimal(6,3))), 2), 0 ) as speed,
	round(avg(cast(message::json->>'obd.acc_long.value' as decimal(10,3))), 2) as acc_long,
	round(avg(cast(message::json->>'obd.acc_yaw.value' as decimal(10,3))), 2) as acc_yaw,
	round(avg(cast(message::json->>'obd.brk_trq_req_elec' as decimal(10,3))), 2) as brk_trq_req_elec,
	round(avg(cast(message::json->>'obd.trac_cons.value' as decimal(10,3))), 2) as trac_cons,
    round(avg(cast(message::json->>'whl_trq_est.value' as decimal(10,3))), 2) as whl_trq_est,
	avg(lat) as lat, 
	avg(lon) as lon
	from useful
	 	
	group by 
	SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',1), 
    SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',2)	
	)
	
	select 
	*
	from agg
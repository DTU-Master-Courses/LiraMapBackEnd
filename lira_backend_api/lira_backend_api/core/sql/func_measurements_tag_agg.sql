SELECT
	"Measurements"."FK_Trip" as tripid,
	SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',1) as ts_date,
    SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',2)  as ts_time,
    "Measurements"."T",
	round(avg(cast(message::json->>'+tag+.value' as numeric)), 2) as value
	FROM public."Measurements"
	where
	"FK_Trip" =  '+trip_id+' -- '2857262b-71db-49df-8db6-a042987bf0eb' --
	and (message::json->>'+tag+.value' is not NULL)
	and "T" = '+tag+'
	group by
	tripid,
    "Measurements"."T",
	SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',1),
    SPLIT_PART(SPLIT_PART(message::json->>'@ts','.',1),'T',2)

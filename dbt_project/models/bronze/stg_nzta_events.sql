WITH deduplicated AS (
    SELECT 
        event_id,
        location,
        event_type,
        status,
        impact_score,
        ingested_at,
        -- This creates a 'rank' for every row per event_id, starting at 1 for the newest
        ROW_NUMBER() OVER (
            PARTITION BY event_id 
            ORDER BY ingested_at DESC
        ) as row_num
    FROM public.nzta_events_raw
)

SELECT 
    event_id,
    location,
    event_type,
    status,
    impact_score,
    ingested_at
FROM deduplicated
WHERE row_num = 1  -- Only keep the single newest version of each ID
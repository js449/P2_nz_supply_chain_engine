{{ config(materialized='table') }}

SELECT 
    event_id,
    location,
    event_type,
    status,
    impact_score,
    CASE 
        WHEN impact_score >= 8.0 THEN 'CRITICAL'
        WHEN impact_score >= 5.0 THEN 'MAJOR'
        ELSE 'MINOR'
    END as urgency_level,
    ingested_at
FROM {{ ref('stg_nzta_events') }}
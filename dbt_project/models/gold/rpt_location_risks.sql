{{ config(materialized='table') }}

SELECT 
    location,
    COUNT(event_id) as total_events,
    -- We only want to count the high-priority ones
    COUNT(CASE WHEN urgency_level = 'CRITICAL' THEN 1 END) as critical_events,
    -- Calculate a risk percentage
    ROUND(
        (COUNT(CASE WHEN urgency_level = 'CRITICAL' THEN 1 END)::DECIMAL / 
        NULLIF(COUNT(event_id), 0)) * 100, 
        2
    ) as risk_percentage
FROM {{ ref('fct_road_events') }}
GROUP BY 1
ORDER BY critical_events DESC
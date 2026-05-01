{{ config(materialized='table') }}

WITH base_metrics AS (
    SELECT 
        location,
        event_type,
        impact_score,
        -- Business Logic: Convert score to hours (Requirement: Delay Trends)
        (impact_score * 2.5) as estimated_delay_hours,
        -- Business Logic: Convert hours to NZD (Requirement: Cost Impact)
        (impact_score * 2.5 * 500) as estimated_cost_nzd,
        urgency_level
    FROM {{ ref('fct_road_events') }}
)

SELECT 
    location,
    COUNT(*) as total_incidents,
    ROUND(SUM(estimated_delay_hours)::numeric, 1) as total_delay_hours,
    ROUND(SUM(estimated_cost_nzd)::numeric, 2) as total_economic_impact_nzd,
    MAX(urgency_level) as highest_urgency_noted
FROM base_metrics
GROUP BY 1
ORDER BY total_economic_impact_nzd DESC
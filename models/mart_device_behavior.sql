{{ config(materialized='table') }}
with device as (

    select * from {{ref('stg_user_device_info')}}
),
engagement as (

    select * from {{ref('fct_user_engagement')}}    
)

select 
    device.primary_device,
    round(avg(engagement.binge_watch_sessions), 1) as avg_binge_watch_sessions,
    round(avg(engagement.recommendation_click_rate), 1) as avg_recommendation_click_rate,
    round(avg(engagement.avg_watch_time_minutes), 1) as avg_watch_time_minutes
from device
join engagement on device.user_id = engagement.user_id
group by device.primary_device
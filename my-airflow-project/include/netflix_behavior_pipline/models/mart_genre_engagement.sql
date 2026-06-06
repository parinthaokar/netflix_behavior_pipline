{{ config(materialized='table') }}

with engagement as (

    select * from {{ref('fct_user_engagement')}}
)

select favorite_genre, count(user_id) as Total_fans, Round(avg(avg_watch_time_minutes),1) as Average_watch_time, Round(avg(completion_rate),1) as Average_Completion_Rate
from engagement
group by favorite_genre
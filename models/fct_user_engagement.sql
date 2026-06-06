with raw_behavior as (
    select * from {{ source('olist_raw', 'USER_WATCHING_BEHAVIOR') }}
)

select
    user_id,
    favorite_genre,
    avg_watch_time_minutes,
    watch_sessions_per_week,
    binge_watch_sessions,
    completion_rate,
    rating_given,
    content_interactions,
    recommendation_click_rate,
    days_since_last_login
from raw_behavior
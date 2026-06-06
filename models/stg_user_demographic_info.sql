with user_info as (
    select *
    from {{source('olist_raw', 'USER_WATCHING_BEHAVIOR')}}
)

select user_id, age, gender, country
from user_info
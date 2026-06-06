with subscription_info as (
    select *
    from {{source('olist_raw', 'USER_WATCHING_BEHAVIOR')}}
)

select user_id, account_age_months, subscription_type, monthly_fee,payment_method,churned
from subscription_info
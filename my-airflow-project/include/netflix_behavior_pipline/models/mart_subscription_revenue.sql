{{ config(materialized='table') }}

with subscription as (

    select * from {{ref('stg_user_subscription_info')}}
)

select subscription_type, count(user_id) as total_count , SUM(MONTHLY_FEE) as total_revenue
from subscription
group by subscription_type
with device_info as (
    select *
    from {{source('olist_raw', 'USER_WATCHING_BEHAVIOR')}}
)

select user_id, primary_device, devices_used
from device_info
SELECT
    call_id,
    customer_id,
    ticket_id,
    agent_id,
    caller,
    call_type,
    call_status,
    start_time,
    end_time,
    created_at,
    updated_at
FROM
    vuanem_warehouse.care_soft_call_logs cscl
WHERE
    group_id = '11823'

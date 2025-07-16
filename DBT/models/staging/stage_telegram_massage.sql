with source as (
    select * from {{ source('raw', 'telegram_messages') }}
)

select
    message_id,
    channel,
    date,
    text,
    has_media,
    media_type,
    media_path
from source

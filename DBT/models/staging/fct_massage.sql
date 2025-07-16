select
    message_id,
    channel as channel_name,
    date,
    has_media,
    media_type,
    length(text) as message_length
from {{ ref('stg_telegram_messages') }}

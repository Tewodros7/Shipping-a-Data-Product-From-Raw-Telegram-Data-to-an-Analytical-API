from sqlalchemy import create_engine, text
import pandas as pd
import os
import json
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

create_table_sql = """
CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.telegram_messages (
    message_id BIGINT PRIMARY KEY,
    channel TEXT,
    date TIMESTAMP,
    text TEXT,
    has_media BOOLEAN,
    media_type TEXT,
    media_path TEXT
);
"""

with engine.connect() as conn:
    conn.execute(text(create_table_sql))
    conn.commit()

DATA_LAKE_DIR = "data/raw/telegram_messages"

def load_json_lines(file_path, channel_name):
    messages = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                record = json.loads(line)
                record['channel'] = channel_name
                messages.append(record)
            except json.JSONDecodeError:
                continue
    return messages

def insert_to_postgres(data):
    if not data:
        return

    df = pd.DataFrame(data)
    df = df[["message_id", "channel", "date", "text", "has_media", "media_type", "media_path"]]

    try:
        df.to_sql("telegram_messages", con=engine, schema="raw", if_exists="append", index=False, method="multi")
        print(f"✅ Inserted {len(df)} rows.")
    except Exception as e:
        print(f"❌ Failed to insert batch: {e}")

for channel in os.listdir(DATA_LAKE_DIR):
    channel_path = os.path.join(DATA_LAKE_DIR, channel)
    if not os.path.isdir(channel_path):
        continue

    print(f"📂 Processing channel: {channel}")

    for file in tqdm(os.listdir(channel_path)):
        if not file.endswith(".json"):
            continue

        full_path = os.path.join(channel_path, file)
        records = load_json_lines(full_path, channel)
        insert_to_postgres(records)

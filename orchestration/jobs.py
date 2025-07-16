from dagster import job
from orchestration.ops.scraping import scrape_messages
from orchestration.ops.load_to_db import load_messages_to_db
from orchestration.ops.detect_yolo import run_yolo_detection
from orchestration.ops.run_dbt import run_dbt

@job
def telegram_data_pipeline():
    raw = scrape_messages()
    loaded = load_messages_to_db(start=raw)  # 👈 Pass output to next
    detected = run_yolo_detection(start=loaded)
    transformed = run_dbt(start=detected)

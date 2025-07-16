from dagster import Definitions
from orchestration.jobs import telegram_data_pipeline

defs = Definitions(
    jobs=[telegram_data_pipeline]
)

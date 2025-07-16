from dagster import ScheduleDefinition
from jobs import telegram_data_pipeline

daily_schedule = ScheduleDefinition(
    job=telegram_data_pipeline,
    cron_schedule="0 6 * * *",  # Every day at 6 AM
)

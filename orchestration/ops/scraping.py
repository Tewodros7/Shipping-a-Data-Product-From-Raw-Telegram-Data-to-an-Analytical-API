from dagster import op
import subprocess
import sys

@op
def scrape_messages():
    subprocess.run([sys.executable, "scripts/telegram_scraper.py"], check=True)

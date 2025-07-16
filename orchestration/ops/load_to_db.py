from dagster import op
import sys

@op
def load_messages_to_db(start):  # 👈 Accept dummy input for sequencing
    import subprocess
    subprocess.run([sys.executable, "scripts/load_raw_data_to_db.py"], check=True)

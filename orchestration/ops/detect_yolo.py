from dagster import op
import sys

@op
def run_yolo_detection(start):
    import subprocess
    subprocess.run([sys.executable, "scripts/yolo_detect.py"], check=True)

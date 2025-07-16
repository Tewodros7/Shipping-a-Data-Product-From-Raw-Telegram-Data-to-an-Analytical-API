# scripts/yolo_detect.py

from ultralytics import YOLO
import os
import cv2
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import logging

# === Config ===
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

# === Load YOLOv8 model (can use custom if needed) ===
model = YOLO("yolov8n.pt")  # Nano version, pre-trained COCO model

# === Paths ===
DATA_ROOT = "data/raw/telegram_messages"

# === Output rows ===
detections = []

logger.info("🔍 Starting YOLOv8 detection...")

for channel in os.listdir(DATA_ROOT):
    image_dir = os.path.join(DATA_ROOT, channel, "images")
    if not os.path.isdir(image_dir):
        continue

    logger.info(f"📂 Scanning {channel}...")

    for img_name in os.listdir(image_dir):
        if not img_name.lower().endswith(".jpg"):
            continue

        message_id = int(img_name.split(".")[0])
        image_path = os.path.join(image_dir, img_name)

        try:
            results = model(image_path)
            for result in results:
                for box in result.boxes:
                    cls_id = int(box.cls[0])
                    confidence = float(box.conf[0])
                    class_name = model.names[cls_id]

                    detections.append({
                        "message_id": message_id,
                        "channel": channel,
                        "detected_class": class_name,
                        "confidence": confidence
                    })

            logger.info(f"✅ Detected objects for {message_id}")
        except Exception as e:
            logger.warning(f"⚠️ Failed on {img_name}: {str(e)}")

logger.info(f"📝 Inserting {len(detections)} detections into database...")

df = pd.DataFrame(detections)

# === Create table and insert ===
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS raw.fct_image_detections (
            message_id BIGINT,
            channel TEXT,
            detected_class TEXT,
            confidence FLOAT
        );
    """))
    conn.commit()

    df.to_sql("fct_image_detections", engine, schema="raw", if_exists="append", index=False, method="multi")

logger.info("✅ Done.")

#  Shipping a Data Product: From Raw Telegram Data to an Analytical API

This repository contains an end-to-end data pipeline project developed as part of **10 Academy's Artificial Intelligence Mastery (KAIM) Week 7 Challenge**. The project extracts and analyzes messages and images from Ethiopian medical-related Telegram channels, transforming them into actionable insights via an analytical API.

---

## 📌 Project Overview

- **Objective:** Build a robust data platform to answer business questions about Ethiopian medical products using public Telegram channel data.
- **Stack:** Python, PostgreSQL, Docker, Telethon, dbt, YOLOv8, FastAPI, Dagster
- **Key Features:**
  - Telegram scraping (messages + images)
  - Star schema modeling with dbt
  - Object detection on images (YOLOv8)
  - API exposing analytical insights
  - Full orchestration with Dagster

---

## 🧱 Architecture Diagram

![Pipeline Diagram](./screenshots/pipeline-diagram.png)
![Star Schema](./screenshots/star-schema.png)

---

## 🗃️ Project Structure

```bash
kaim-week7/
├── data/
│   └── raw/
│       └── telegram_messages/YYYY-MM-DD/channel_name.json
├── dbt_project/
│   ├── models/
│   │   ├── staging/
│   │   ├── marts/
│   │   └── schema.yml
├── images/
│   └── raw/
├── api/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── database.py
├── orchestration/
│   └── dagster_job.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
└── README.md
````

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/DagmMesfin/shipping-data-product-week7.git
cd shipping-data-product-week7
```

### 2. Set Up Environment Variables

Create a `.env` file:

```env
TELEGRAM_API_ID=your_telegram_api_id
TELEGRAM_API_HASH=your_telegram_api_hash
DATABASE_URL=postgresql://postgres:postgres@db:5432/kaimdb
```

> ✅ Make sure `.env` is added to `.gitignore`.

### 3. Run Docker Environment

```bash
docker-compose up --build
```

This will:

* Spin up a PostgreSQL database
* Build your Python environment

---

## 🚀 Running Each Component

### A. Telegram Data Scraping

```bash
python scripts/scrape_telegram.py
```

Scrapes messages and images from public channels and stores them in `data/raw/`.

---

### B. Load Raw JSON to PostgreSQL

```bash
python scripts/load_raw_to_db.py
```

Loads raw data from JSON into a raw table in PostgreSQL.

---

### C. dbt Transformations

```bash
cd dbt_project
dbt run
dbt test
```

Builds the staging and mart models using a star schema.

---

### D. YOLOv8 Object Detection

```bash
python scripts/yolo_detect.py
```

Detects objects in scraped images and stores results in `fct_image_detections`.

---

### E. Launch FastAPI Server

```bash
uvicorn api.main:app --reload
```

#### 📊 Key Endpoints

* `GET /api/reports/top-products?limit=10`
* `GET /api/channels/{channel}/activity`
* `GET /api/search/messages?query=paracetamol`

Screenshots:
![Top Products](./screenshots/top-products.png)
![Channel Activity](./screenshots/channel-activity.png)

---

### F. Dagster Orchestration

Launch Dagster UI:

```bash
dagster dev
```

Run the full pipeline from scraping to enrichment via Dagster job.

---

## 🧠 Business Questions Answered

* What are the top 10 most frequently mentioned medical products?
* How does availability/pricing differ across Telegram channels?
* Which channels have the most images and what kind of content?
* What are the posting trends over time?

---

## 📚 Learning Highlights

* End-to-end ELT data architecture (raw → staging → marts)
* Star schema dimensional modeling
* Integrating unstructured image data into structured warehouses
* Analytical API development and data validation
* Data pipeline orchestration using Dagster

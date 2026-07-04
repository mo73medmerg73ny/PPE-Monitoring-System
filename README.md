# PPE Monitoring System 🦺

A real-time Personal Protective Equipment (PPE) monitoring system built with YOLOv8, FastAPI, and Streamlit. Detects safety violations on construction sites and logs them automatically.

## Features

- Real-time detection of workers missing hardhats or safety vests
- Violation logging with timestamp and snapshot image
- REST API for accessing violation history
- Streamlit dashboard for video analysis and live monitoring
- PostgreSQL database for persistent storage
- Fully containerized with Docker

## Tech Stack

- **YOLOv8** — object detection and tracking
- **FastAPI** — REST API and WebSocket streaming
- **Streamlit** — dashboard and UI
- **PostgreSQL** — violation storage
- **Docker** — containerization

## Detected Classes

| Class | Description |
|---|---|
| Person | Worker detected |
| Hardhat | Helmet worn ✅ |
| No-Hardhat | Helmet missing ❌ |
| Safety Vest | Vest worn ✅ |
| No-Safety Vest | Vest missing ❌ |

## Project Structure

```
ppe_monitor/
├── core/
│   ├── detector.py       # YOLO inference + ByteTrack
│   └── violation.py      # PPE logic + violation detection
├── api/
│   └── routes/
│       └── violations.py # Violation endpoints
├── db/
│   └── models.py         # PostgreSQL models + queries
├── app/
│   └── streamlit_app.py  # Dashboard
├── main.py               # FastAPI app
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Getting Started

### With Docker

```bash
git clone https://github.com/your-username/ppe-monitor
cd ppe-monitor
docker-compose up --build
```

API: http://localhost:8000  
Dashboard: http://localhost:8501

### Without Docker

```bash
pip install -r requirements.txt
uvicorn main:app --reload
streamlit run app/streamlit_app.py
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/analyze/video` | Analyze uploaded video |
| WS | `/analyze/live` | Real-time camera stream |
| GET | `/violations/` | All violations |
| GET | `/violations/{person_id}` | Violations by person |
| GET | `/violations/date/{date}` | Violations by date |

## How It Works

1. Each frame is processed by YOLOv8 to detect persons and PPE
2. ByteTrack assigns a stable ID to each person across frames
3. IoU matching links each person to nearby helmets and vests
4. A violation is logged only after 5 continuous seconds of non-compliance
5. Each violation is saved with a snapshot image and stored in PostgreSQL

## Model

Trained on the [Construction Site Safety dataset](https://www.kaggle.com/datasets/snehilsanyal/construction-site-safety-image-dataset-roboflow) with YOLOv8m — 10 classes, 50 epochs.

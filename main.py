import os
import cv2
import time
import tempfile
import numpy as np
from fastapi import FastAPI, UploadFile, WebSocket, File
from api.routes.violation import router as violation_router
from core.detector import PPEDetector
from core.violation import separate_detections, check_ppe, log_violation
from db.models import db_init, insert_violation


db_init()

detector = PPEDetector()

app = FastAPI(
    title='PPE Monitoring System',
    description='Real-time PPE detection',
    version='1.0.0'
)

app.include_router(violation_router)

@app.get('/', summary="Health Check", description='Check if The API is Running')
def home():
    return {"message" : "Heloo World"}


async def read_video(file):
    video_bytes = await file.read()

    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tm:
        tm.write(video_bytes)
        video_path = tm.name

    cap = cv2.VideoCapture(video_path)
    return cap, video_path

@app.post('/analyze/video')
async def analyze_video(file: UploadFile = File(...)):
    cap, video_path = await read_video(file)
    
    timers = {}
    all_violations = []

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        detections = detector.detect(frame)
        person, hardhats, vests = separate_detections(detections)
        results = check_ppe(person, hardhats, vests)
        violations = log_violation(results, timers, frame)
        all_violations.extend(violations)

        for v in violations:
            insert_violation(v['person_id'], v['violation_type'],  v['timestamp'], v['image_path'])

    cap.release()
    os.remove(video_path)

    return {"message": "Video analyzed", "violations": len(all_violations)}


@app.websocket('/analyze/live')
async def analyze_live(websocket : WebSocket):
    await websocket.accept()

    cap = cv2.VideoCapture(0)

    timers = {}
    all_violations = []

    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            break

        detections = detector.detect(frame)
        person, hardhats, vests = separate_detections(detections)
        results = check_ppe(person, hardhats, vests)
        violations = log_violation(results, timers, frame)
        all_violations.extend(violations)

        for v in violations:
            insert_violation(v['person_id'], v['violation_type'], v['timestamp'] , v['image_path'])

        await websocket.send_json({
        "message": "Video analyzed",
        "violations": len(all_violations)
        })

    cap.release()

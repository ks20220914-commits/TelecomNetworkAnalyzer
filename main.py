from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

# ==================== قاعدة البيانات ====================

DB_NAME = "telecom.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            network_type TEXT,
            cell_id TEXT,
            rsrp REAL,
            rsrq REAL,
            sinr REAL,
            latitude REAL,
            longitude REAL,
            download_mbps REAL,
            upload_mbps REAL,
            latency_ms REAL
        )
    """)
    conn.commit()
    conn.close()

def save_measurement(data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO measurements (
            timestamp, network_type, cell_id, rsrp, rsrq, sinr,
            latitude, longitude, download_mbps, upload_mbps, latency_ms
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.timestamp,
        data.network_type,
        data.cell_id,
        data.rsrp,
        data.rsrq,
        data.sinr,
        data.latitude,
        data.longitude,
        data.download_mbps,
        data.upload_mbps,
        data.latency_ms
    ))
    conn.commit()
    conn.close()

def get_all_measurements():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM measurements ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

# ==================== نموذج البيانات ====================

class Measurement(BaseModel):
    timestamp: str
    network_type: str = "LTE"
    cell_id: str = "101"
    rsrp: float = -85
    rsrq: float = -10
    sinr: float = 18
    latitude: float = 30.0444
    longitude: float = 31.2357
    download_mbps: float = 45.2
    upload_mbps: float = 12.4
    latency_ms: float = 32

# ==================== FastAPI ====================

app = FastAPI(title="Telecom Network Analyzer API")

# نشغل قاعدة البيانات
init_db()

@app.get("/")
def home():
    return {"message": "📡 Telecom API is running!", "status": "online"}

@app.post("/measurements")
def add_measurement(data: Measurement):
    save_measurement(data)
    return {"status": "success", "message": "Measurement saved!", "data": data.dict()}

@app.get("/measurements")
def get_measurements():
    rows = get_all_measurements()
    return {"count": len(rows), "data": rows}
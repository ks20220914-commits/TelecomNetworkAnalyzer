<div align="center">

<img src="screenshots/logo.png" alt="Telecom Network Analyzer Logo" width="150"/>

# 📡 Telecom Network Analyzer

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3.0+-blue.svg)
![Plotly](https://img.shields.io/badge/Plotly-5.0+-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**A Complete Mobile Network Performance Analysis Platform**

[Features](#-features) • [Architecture](#-system-architecture) • [Installation](#-installation) • [Usage](#-usage) • [Dashboard](#-dashboard-screenshots) • [Contributing](#-contributing)

</div>

---

## 📖 Overview

**Telecom Network Analyzer** is a complete end-to-end platform for collecting, storing, and analyzing mobile network performance data. The system consists of:

- **📱 Data Collection**: Mobile app (G-NetTrack) for collecting real network measurements
- **🐍 Backend API**: FastAPI for receiving and storing data
- **🗄️ Database**: SQLite for persistent storage
- **📊 Dashboard**: Streamlit for visualization and analysis

> 🔥 **Goal**: Provide telecom professionals and network engineers with a complete tool for network performance monitoring and analysis.

---

## 🚀 Features

### 📊 Core Analytics
- **Signal Quality Analysis**: Classify RSRP and SINR into Excellent, Good, Fair, Poor
- **Speed Analysis**: Monitor Download/Upload speeds and Latency
- **Network Health Score**: Calculate overall network health (0-100)
- **Problem Detection**: Automatically identify weak signal, high latency, and low speed issues

### 📈 Interactive Visualizations
- RSRP/SINR trends over time
- Signal quality distribution charts
- Download/Upload speed comparison
- Latency monitoring with thresholds
- Geographic coverage map

### 🗃️ Data Management
- CSV file upload support
- G-NetTrack TXT file support (auto-conversion)
- Cell-level performance analysis
- Export analysis results as CSV
- Sample data included for testing
- SQLite database for persistent storage

### 🔌 API Integration
- RESTful API with FastAPI
- POST /measurements - Add new measurements
- GET /measurements - Retrieve all measurements
- Automatic database storage

### 🎯 Cell Performance
- Per-cell statistics (samples, avg RSRP/SINR/speed/latency)
- Problem count per cell
- Identify best and worst performing cells

---

## 🏗️ System Architecture

📱 G-NetTrack App (Mobile)

↓ 

(TXT/CSV Export)

📤 File Upload

↓

📊 Streamlit Dashboard

↓

(Data Processing)

🐍 TelecomAnalyzer (Python)

↓

(Analysis Results)

📊 Interactive Charts & Map

----- OR -----

📱 Mobile App / Postman

↓

(HTTP POST)

🐍 FastAPI Backend
↓

(Save)

🗄️ SQLite Database
↓

(Read)

📊 Streamlit Dashboard


---

## 🛠️ Technologies

| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Core programming language |
| **Streamlit** | Interactive web dashboard |
| **FastAPI** | RESTful API backend |
| **SQLite** | Lightweight database |
| **Pandas** | Data processing and analysis |
| **Plotly** | Interactive charts and visualizations |

---

## 📁 Project Structure

TelecomNetworkAnalyzer/

├── app.py              # Main Streamlit dashboard

├── analyzer.py         # Analysis engine (backend logic

├── main.py             # FastAPI backend

├── db_helper.py        # Database helper functions

├── sample_data.csv     # Sample measurement data

├── requirements.txt    # Python dependencies

├── screenshots/        # Dashboard screenshots

│   └── logo.png        # Project logo

└── README.md          # Documentation

`

---

## 📊 Input Data Format

The application accepts CSV files with the following columns:

| Column | Type | Description |
|--------|------|-------------|
| timestamp | datetime | Measurement time |
| cell_id | int | Cell tower identifier |
| latitude | float | GPS latitude |
| longitude | float | GPS longitude |
| rsrp | float | Reference Signal Received Power (dBm) |
| rsrq | float | Reference Signal Received Quality (dB) |
| sinr | float | Signal-to-Interference-plus-Noise Ratio (dB) |
| download_mbps | float | Download speed in Mbps |
| upload_mbps | float | Upload speed in Mbps |
| latency_ms | float | Network latency in milliseconds |

### 📱 G-NetTrack Support
The dashboard automatically converts G-NetTrack TXT exports to the required format.

---

## 💻 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone the repository

git clone https://github.com/yourusername/TelecomNetworkAnalyzer.git
cd TelecomNetworkAnalyzer

### Step 2: Install dependencies

pip install -r requirements.txt
Or install manually:

pip install pandas streamlit plotly fastapi uvicorn
### Step 3: Run the Dashboard

streamlit run app.py
### Step 4: Run the API Server (Optional)

python -m uvicorn main:app --reload
### Step 5: Open in browser

· Dashboard: http://localhost:8501

· API: http://localhost:8000

· API Docs: http://localhost:8000/docs

---

🎯 Usage Guide

1️⃣ Collect Data (Mobile)

· Install G-NetTrack Lite from Google Play
· Grant location and phone permissions
· Start logging measurements
· Export as TXT file

2️⃣ Upload Data

· Click Upload CSV or TXT in the sidebar
· Select your file (CSV or G-NetTrack TXT)
· Or use the included sample_data.csv for testing

3️⃣ Analyze Results

The dashboard automatically displays:

· Network Overview cards (Health Score, RSRP, SINR, Problems)
· Signal quality distribution charts
· Time series trends for RSRP, SINR, Speed, and Latency

4️⃣ Explore Cell Performance

· View statistics for each cell tower
· Identify problematic cells with high issue counts

5️⃣ Export Results

· Click Download CSV to save the analysis results

6️⃣ API Usage (Optional)

Send measurements via HTTP POST:

curl -X POST http://localhost:8000/measurements \



    -H"Content-Type: application/json" \
  
    -d'{
  
    "timestamp": "2026-09-04 15:30:00",
    
    "network_type": "5G",
    
    "cell_id": "205",
    
    "rsrp": -72,
    
    "rsrq": -8,
    
    "sinr": 25,
    
    "latitude": 30.0500,
    
    "longitude": 31.2400,
    
    "download_mbps": 120.5,
    
    "upload_mbps": 35.2,
    
    "latency_ms": 15
    }'
  
  
---

📸 Dashboard Screenshots

"""in the screenshots file"""

<div align="center">

Network Overview

<img src="screenshots/overview.png" alt="Network Overview" width="800"/>

Signal Quality Charts

<img src="screenshots/signal_quality.png" alt="Signal Quality" width="800"/>

RSRP Trend

<img src="screenshots/rsrp_trend.png" alt="RSRP Trend" width="800"/>

SINR Trend

<img src="screenshots/sinr_trend.png" alt="SINR Trend" width="800"/>

Speed Analysis

<img src="screenshots/speed_analysis.png" alt="Speed Analysis" width="800"/>

Latency Analysis

<img src="screenshots/latency_analysis.png" alt="Latency Analysis" width="800"/>

Cell Performance Table

<img src="screenshots/cell_performance.png" alt="Cell Performance" width="800"/>

Detected Problems

<img src="screenshots/problems.png" alt="Detected Problems" width="800"/>

Location Map

<img src="screenshots/map.png" alt="Location Map" width="800"/>

</div>

---

📊 Sample Output

After analyzing data, the dashboard provides:

Network Health Score: 80/100
Average RSRP: -92.5 dBm
Average SINR: 14.1 dB
Total Problems Detected: 6


Best Cell: Cell 105 (Avg RSRP: -77.33, Avg SINR: 22.67)


Worst Cell: Cell 104 (Avg RSRP: -111.67, Avg SINR: 4.33)

---

🔌 API Endpoints

Method Endpoint Description
GET / API status
POST /measurements Add new measurement
GET /measurements Get all measurements
GET /docs Swagger UI documentation

---

🤝 Contributing

Contributions are welcome! Here's how you can help:
1. Fork the repository
2. Create a feature branch (git checkout -b feature/AmazingFeature)
3. Commit your changes (git commit -m 'Add AmazingFeature')
4. Push to the branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

---

📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

👨‍💻 Author

Kyrillos Saeed

https://linkedin.com/in/kyrillos-saeed


---

🙏 Acknowledgments

· Streamlit for the amazing web framework
· FastAPI for the powerful API framework
· Pandas for powerful data processing
· Plotly for interactive visualizations
· G-NetTrack for mobile data collection

---

⭐ Show Your Support

If you found this project helpful, please give it a ⭐ on GitHub!

---

<div align="center">
Made with ❤️ by Kyrillos Saeed
</div>
`

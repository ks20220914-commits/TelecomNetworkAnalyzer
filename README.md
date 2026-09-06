<div align="center">

<img src="screenshots/logo.png" alt="Telecom Network Analyzer Logo" width="150"/>

# 📡 Telecom Network Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3.0+-blue.svg)
![Plotly](https://img.shields.io/badge/Plotly-5.0+-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Version](https://img.shields.io/badge/Version-3.0-orange.svg)

**A Complete End-to-End Mobile Network Performance Analysis & Intelligence Platform**

[Features](#-features) • [Architecture](#-system-architecture) • [Installation](#-installation) • [Usage](#-usage) • [Screenshots](#-screenshots) • [Contributing](#-contributing)

</div>

---

## 📖 Overview

**Telecom Network Intelligence Platform** is a comprehensive, end-to-end solution for collecting, storing, analyzing, and visualizing mobile network performance data. Built with a focus on **Telecom Engineering** and **Data Science**, this platform transforms raw network measurements into actionable insights.

> 🔥 **Mission**: Empower telecom professionals and network engineers with a complete tool for network performance monitoring, analysis, and optimization.

---

## 🚀 Features

### 📊 Core Analytics (12 Features)
- **Signal Quality Analysis**: Classify RSRP and SINR into Excellent, Good, Fair, Poor
- **Speed Analysis**: Monitor Download/Upload speeds and Latency
- **Network Health Score**: Calculate overall network health (0-100)
- **Problem Detection**: Automatically identify weak signal, high latency, and low speed issues
- **Cell Performance**: Per-cell statistics and problem analysis
- **Interactive Charts**: RSRP/SINR trends, quality distribution, speed comparison
- **Geographic Map**: Location-based coverage visualization
- **CSV Upload & Export**: Easy data import/export
- **Sample Data**: Included for testing

### 🔬 Advanced Analytics (14 Features)
- **Coverage Heatmap**: Visualize signal strength and quality on interactive maps
- **User Experience Score**: Calculate UX Score (0-100) based on network quality
- **Handover Analysis**: Detect and analyze cell transitions
- **Time-Series Forecasting**: Predict future RSRP, SINR, and Latency
- **Anomaly Detection**: Identify unusual measurements using IQR and Z-Score methods
- **Root Cause Analysis**: Diagnose the root causes of network problems
- **Machine Learning Prediction**: Random Forest model to predict network problems
- **PDF Reports**: Generate professional PDF reports
- **Coverage Gaps**: Detect and analyze coverage gaps
- **Capacity Planning**: Analyze network load and identify bottlenecks
- **Real-time Dashboard**: Live monitoring with auto-refresh
- **G-NetTrack Support**: Direct import of mobile measurement data
- **FastAPI Backend**: RESTful API for data collection
- **SQLite Database**: Persistent data storage

### 🎨 Premium Features (10 Features)
- **Export to Excel**: Multi-sheet Excel reports
- **Dark/Light Mode**: Toggle between themes
- **Data Comparison**: Compare two periods or two cells
- **Network Simulation**: What-if analysis for network improvements
- **User Authentication**: Secure login with user roles
- **Custom Alerts**: Set custom thresholds for network monitoring
- **Data Import from URL**: Import CSV from any URL
- **Mobile Responsive**: Optimized for all screen sizes
- **Advanced Analytics Dashboard**: Comprehensive analytics in one place
- **Data Quality Report**: Analyze data quality (missing, duplicates, outliers)

---

## 🏗️ System Architecture

┌────          ──────────────────────────────                     ───────────────────────────────────────┐


│                            Telecom Network Intelligence                                                │                                                                          │


│
┌───────               ────────────────────────────────        ──────────────────────────┐               │

│ 

│                                   DATA COLLECTION                                    │                 │

│

│

┌──────────┐           ┌──────────┐          ┌──────────┐        ┌──────────┐            │               │

│    

│


│       CSV File │        │G-NetTrack│        │URL Import│          │ FastAPI  │          │             │

│


│     └──────────┘     └──────────┘      └──────────┘      └──────────┘               │                 │

│


└─────────────────────────────────────────────────────────────────┘    │

│                                    ↓                                    │

│  ┌─────────────────────────────────────────────────────────────────┐    │


│  │                        DATA PROCESSING                          │    │



│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │    │

│  │  │ Cleaning │  │ Analysis │  │   ML     │  │Forecastng│         │    │

│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │    │

│  └─────────────────────────────────────────────────────────────────┘    │

│                                    ↓                                    │

│  ┌─────────────────────────────────────────────────────────────────┐    │

│  │                       VISUALIZATION                             │    │

│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │    │

│  │  │ Dashboard│  │  Charts  │  │   Map    │  │ Reports  │         │    │

│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │    │

│  └─────────────────────────────────────────────────────────────────┘    │

│                                    ↓                                    │

│  ┌─────────────────────────────────────────────────────────────────┐    │

│  │                      INTELLIGENCE                               │    │

│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │    │

│  │  │ Anomaly  │  │Root Cause│  │ Capacity │  │   Alerts │         │    │

│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │    │

│  └─────────────────────────────────────────────────────────────────┘    │

└─────────────────────────────────────────────────────────────────────────┘


---

## 🛠️ Technologies

| Category | Technology | Purpose |
|----------|------------|---------|
| **Language** | Python 3.8+ | Core programming |
| **Web Framework** | Streamlit | Interactive dashboard |
| **Backend** | FastAPI | RESTful API |
| **Database** | SQLite | Lightweight storage |
| **Data Processing** | Pandas, NumPy | Data analysis |
| **Visualization** | Plotly, Folium | Interactive charts & maps |
| **Machine Learning** | Scikit-learn | Random Forest, ML |
| **Reporting** | ReportLab | PDF generation |
| **Excel** | OpenPyXL | Excel export |
| **Authentication** | Hashlib, JSON | User management |

---

## 📁 Project Structure

TelecomNetworkAnalyzer/

├── app.py                 # Main Streamlit Dashboard (36 features)

├── analyzer.py            # Analysis Engine (24 analytics functions)

├── main.py               # FastAPI Backend Server

├── db_helper.py          # SQLite Database Helper

├── telecom.db            # SQLite Database File

├── sample_data.csv       # Sample Measurement Data

├── users.json            # User Authentication Data

├── requirements.txt      # Python Dependencies

├── README.md            # Documentation

├── LICENSE              # MIT License

└── screenshots/         # Dashboard Screenshots

├── logo.png         # Project Logo

├── overview.png     # Network Overview

├── signal_quality.png

├── rsrp_trend.png

├── sinr_trend.png

├── speed_analysis.png

├── latency_analysis.png

├── cell_performance.png

├── problems.png

├── map.png

└── advanced_analytics.png




---

## 📊 Input Data Format

The platform accepts CSV/TXT files with the following columns:

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

### 📱 Supported Formats
- ✅ Standard CSV files
- ✅ G-NetTrack TXT exports (auto-conversion)
- ✅ URL-based CSV imports
- ✅ FastAPI POST requests

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
Step 3: Run the Dashboard

streamlit run app.py
### Step 4: Run the API Server (Optional)

python -m uvicorn main:app --reload
### Step 5: Open in browser

· Dashboard: http://localhost:8501
· API: http://localhost:8000
· API Docs: http://localhost:8000/docs

---

🎯 Usage Guide

1️⃣ Collect Data

· Mobile App: Use G-NetTrack Lite to collect network measurements
· Manual: Prepare CSV file with required columns
· API: Send data via HTTP POST to FastAPI

2️⃣ Upload Data

· Upload CSV: Click "Upload CSV or TXT" in sidebar
· Import URL: Enter CSV URL in sidebar
· Use Sample: Built-in sample_data.csv

3️⃣ Analyze

The dashboard automatically displays:

· Network Overview (Health Score, KPIs)
· Signal Quality Charts
· Time Series Trends
· Cell Performance Table
· Detected Problems
· Coverage Heatmap
· Advanced Analytics

4️⃣ Explore Advanced Features

· Filter Data: Use sidebar filters (date, cell, quality, etc.)
· Compare Data: Compare periods or cells
· Run Simulation: Test what-if scenarios
· Generate Reports: PDF, Excel, CSV
· Check Alerts: Custom threshold monitoring

5️⃣ Export Results

· 📥 Download CSV
· 📥 Download Excel
· 📥 Download PDF Report
· 📥 Download Quality Report

---

📸 Screenshots

<div align="center">

🏠 Network Overview

"""in the screenshots file"""

<img src="screenshots/overview.png" alt="Network Overview" width="800"/>

📊 Signal Quality Charts

<img src="screenshots/signal_quality.png" alt="Signal Quality" width="800"/>

📈 RSRP & SINR Trends

<img src="screenshots/rsrp_trend.png" alt="RSRP Trend" width="800"/>
<img src="screenshots/sinr_trend.png" alt="SINR Trend" width="800"/>

🚀 Speed & Latency Analysis

<img src="screenshots/speed_analysis.png" alt="Speed Analysis" width="800"/>
<img src="screenshots/latency_analysis.png" alt="Latency Analysis" width="800"/>

📋 Cell Performance & Problems

<img src="screenshots/cell_performance.png" alt="Cell Performance" width="800"/>
<img src="screenshots/problems.png" alt="Detected Problems" width="800"/>

🗺️ Coverage Heatmap

<img src="screenshots/map.png" alt="Coverage Map" width="800"/>

📊 Advanced Analytics

<img src="screenshots/advanced_analytics.png" alt="Advanced Analytics" width="800"/>

</div>

---

🔌 API Endpoints

Method Endpoint Description
GET / API status
POST /measurements Add new measurement
GET /measurements Get all measurements
GET /docs Swagger UI documentation

---

📊 Feature Count

Category Features
Core Analytics 12
Advanced Analytics 14
Premium Features 10
Total 36

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

· Telecom Engineer | Data Science Enthusiast
· Building tools that bridge Telecom Engineering and Data Science
https://ks20220914-commits.github.io/Kyrillos-Saeed.github.io/

https://www.linkedin.com/in/kyrillos-saeed

---

🙏 Acknowledgments

· Streamlit - Amazing web framework
· FastAPI - Powerful API framework
· Pandas - Data processing powerhouse
· Plotly - Interactive visualizations
· Scikit-learn - Machine learning
· G-NetTrack - Mobile data collection

---

⭐ Show Your Support

If you found this project helpful, please give it a ⭐ on GitHub!

---

<div align="center">

Built with ❤️ by Kyrillos Saeed

Telecom Engineering + Data Science = Intelligence

</div>
`

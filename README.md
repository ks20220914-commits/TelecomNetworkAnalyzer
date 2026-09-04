<div align="center">

<img src="screenshots/logo.png" alt="Telecom Network Analyzer Logo" width="150"/>

# 📡 Telecom Network Analyzer

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-green.svg)
![Plotly](https://img.shields.io/badge/Plotly-5.0+-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**A Professional Mobile Network Performance Analysis & Monitoring Dashboard**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Dashboard](#-dashboard-screenshots) • [Contributing](#-contributing)

</div>

---

## 📖 Overview

**Telecom Network Analyzer** is a comprehensive Python-based tool for analyzing mobile network performance metrics including RSRP, RSRQ, SINR, latency, and data speeds. The application provides an interactive dashboard with real-time visualizations, problem detection, and network health scoring.

> 🔥 **Goal**: Help network engineers and telecom professionals identify coverage issues and optimize network performance through data-driven insights.

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
- Cell-level performance analysis
- Export analysis results as CSV
- Sample data included for testing

### 🎯 Cell Performance
- Per-cell statistics (samples, avg RSRP/SINR/speed/latency)
- Problem count per cell
- Identify best and worst performing cells

---

## 🛠️ Technologies

| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Core programming language |
| **Streamlit** | Interactive web dashboard |
| **Pandas** | Data processing and analysis |
| **Plotly** | Interactive charts and visualizations |

---

## 📁 Project Structure

TelecomNetworkAnalyzer/
├── app.py              # Main dashboard application
├── analyzer.py         # Analysis engine (backend logic)
├── sample_data.csv     # Sample measurement data
├── requirements.txt    # Python dependencies
├── screenshots/        # Dashboard screenshots
│   └── logo.png        # Project logo
└── README.md          # Documentation


---

## 📊 Input Data Format

The application expects CSV files with the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `timestamp` | datetime | Measurement time |
| `cell_id` | int | Cell tower identifier |
| `latitude` | float | GPS latitude |
| `longitude` | float | GPS longitude |
| `rsrp` | float | Reference Signal Received Power (dBm) |
| `rsrq` | float | Reference Signal Received Quality (dB) |
| `sinr` | float | Signal-to-Interference-plus-Noise Ratio (dB) |
| `download_mbps` | float | Download speed in Mbps |
| `upload_mbps` | float | Upload speed in Mbps |
| `latency_ms` | float | Network latency in milliseconds |

---

## 💻 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone the repository

bash
git clone https://github.com/yourusername/TelecomNetworkAnalyzer.git
cd TelecomNetworkAnalyzer

Step 2: Install dependencies

bash
pip install -r requirements.txt

Or install manually:

bash
pip install pandas streamlit plotly

Step 3: Run the application

bash
streamlit run app.py
`

Step 4: Open in browser

The dashboard will open automatically at http://localhost:8501

---

🎯 Usage Guide

1️⃣ Upload Data

· Click the Upload CSV button in the sidebar
· Select your CSV file with the required columns
· Or use the included sample_data.csv for testing

2️⃣ Analyze Results

The dashboard automatically displays:

· Network Overview cards (Health Score, RSRP, SINR, Problems)
· Signal quality distribution charts
· Time series trends for RSRP, SINR, Speed, and Latency

3️⃣ Explore Cell Performance

· View statistics for each cell tower
· Identify problematic cells with high issue counts

4️⃣ Export Results

· Click Download CSV to save the analysis results

---

📸 Dashboard Screenshots

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

https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white
https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white

---

🙏 Acknowledgments

· Streamlit for the amazing web framework
· Pandas for powerful data processing
· Plotly for interactive visualizations

---

⭐ Show Your Support

If you found this project helpful, please give it a ⭐ on GitHub!

---

<div align="center">
Made with ❤️ by Kyrillos Saeed
</div>
`
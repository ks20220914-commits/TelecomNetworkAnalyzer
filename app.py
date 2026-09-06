import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from analyzer import TelecomAnalyzer
from db_helper import get_data_as_dataframe
import requests


# في بداية الملف، أضف:
try:
    import reportlab
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="📡 Telecom Analyzer",
    page_icon="📡",
    layout="wide"
)

# ==================== MOBILE RESPONSIVE ====================
st.markdown("""
<style>
    /* تحسين للشاشات الصغيرة */
    @media (max-width: 768px) {
        /* تصغير حجم الخط للعنواين */
        h1 {
            font-size: 24px !important;
        }
        h2 {
            font-size: 20px !important;
        }
        h3 {
            font-size: 16px !important;
        }
        
        /* جعل البطاقات في صف واحد */
        .stColumns {
            flex-direction: column !important;
        }
        
        /* تصغير حجم المتركس */
        .stMetric {
            padding: 8px !important;
        }
        .stMetric label {
            font-size: 12px !important;
        }
        .stMetric div {
            font-size: 20px !important;
        }
        
        /* جعل الجداول قابلة للتمرير */
        .stDataFrame {
            overflow-x: auto !important;
        }
        .stDataFrame table {
            font-size: 10px !important;
        }
        
        /* تصغير حجم الخريطة */
        .stMap {
            height: 300px !important;
        }
        
        /* تصغير حجم الفلاتر */
        .stSidebar {
            width: 250px !important;
        }
        .stSidebar .stSelectbox, 
        .stSidebar .stMultiselect,
        .stSidebar .stDateInput {
            font-size: 12px !important;
        }
        
        /* تحسين الرسوم البيانية */
        .stPlotlyChart {
            height: 300px !important;
        }
        .stPlotlyChart .plotly {
            height: 280px !important;
        }
        
        /* تصغير حجم الأزرار */
        .stButton button {
            font-size: 12px !important;
            padding: 6px 12px !important;
        }
        
        /* تحسين تبويبات */
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px !important;
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 12px !important;
            padding: 4px 8px !important;
        }
    }
    
    /* تحسين للشاشات المتوسطة */
    @media (min-width: 769px) and (max-width: 1024px) {
        .stColumns {
            flex-wrap: wrap !important;
        }
        .stColumns > div {
            flex: 1 1 45% !important;
        }
    }
    
    /* تحسينات عامة */
    .stApp {
        max-width: 100% !important;
        overflow-x: hidden !important;
    }
    
    /* جعل الصور والخريطة تتناسب مع الشاشة */
    .stImage img, .stMap {
        max-width: 100% !important;
        height: auto !important;
    }
    
    /* تحسين التمرير */
    .stSidebar .stSidebarContent {
        overflow-y: auto !important;
    }
    
    /* تحسين الداتا فريم */
    .dataframe {
        font-size: 12px !important;
    }
    .dataframe td, .dataframe th {
        padding: 4px 6px !important;
    }
</style>
""", unsafe_allow_html=True)







# ==================== AUTHENTICATION ====================
# ==================== AUTHENTICATION ====================
import hashlib
import json
import os

# ملف تخزين المستخدمين
USERS_FILE = "users.json"

# تحميل المستخدمين من ملف
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

# حفظ المستخدمين في ملف
def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

# تشفير كلمة المرور
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# تحميل المستخدمين
USERS = load_users()

# التأكد من وجود الأدمن
if "admin" not in USERS:
    USERS["admin"] = {
        "password": hash_password("admin123"),
        "role": "admin",
        "name": "Administrator"
    }
    save_users(USERS)

# تهيئة session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'user_role' not in st.session_state:
    st.session_state.user_role = ""

# ==================== تسجيل الدخول ====================
def login():
    username = st.session_state.login_username
    password = st.session_state.login_password
    
    if username in USERS and USERS[username]["password"] == hash_password(password):
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.user_role = USERS[username]["role"]
        st.rerun()
    else:
        st.error("❌ Invalid username or password")

# ==================== تسجيل حساب جديد ====================
def register():
    new_username = st.session_state.register_username
    new_password = st.session_state.register_password
    new_name = st.session_state.register_name
    
    if new_username in USERS:
        st.error("❌ Username already exists")
        return
    
    if len(new_password) < 4:
        st.error("❌ Password must be at least 4 characters")
        return
    
    USERS[new_username] = {
        "password": hash_password(new_password),
        "role": "user",
        "name": new_name
    }
    save_users(USERS)
    st.success(f"✅ Account created! Welcome {new_name}")
    st.rerun()

# ==================== تسجيل الخروج ====================
def logout():
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.user_role = ""
    st.rerun()

# ==================== صفحة الدخول ====================
if not st.session_state.authenticated:
    st.markdown("""
    <style>
    .login-container {
        max-width: 450px;
        margin: 50px auto;
        padding: 30px;
        border-radius: 12px;
        background: white;
        box-shadow: 0 0 30px rgba(0,0,0,0.1);
    }
    .login-title {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .login-subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 25px;
    }
    </style>
    <div class="login-container">
        <div class="login-title">📡 Telecom Analyzer</div>
        <div class="login-subtitle">Network Performance Dashboard</div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
    
    with tab1:
        st.text_input("👤 Username", key="login_username", placeholder="Enter your username")
        st.text_input("🔑 Password", type="password", key="login_password", placeholder="Enter your password")
        
        if st.button("🔓 Login", use_container_width=True):
            login()
    
    with tab2:
        st.text_input("👤 Choose Username", key="register_username", placeholder="Choose a username")
        st.text_input("🔑 Choose Password (min 4 chars)", type="password", key="register_password", placeholder="Choose a password")
        st.text_input("📛 Your Name", key="register_name", placeholder="Enter your full name")
        
        if st.button("📝 Create Account", use_container_width=True):
            register()
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()
 # ==================== معلومات المستخدم ====================
st.sidebar.markdown(f"👤 {USERS[st.session_state.username]['name']} (@{st.session_state.username})")
if st.session_state.user_role == "admin":
    st.sidebar.markdown("🔑 Admin Access")
else:
    st.sidebar.markdown("👀 User Access")

if st.sidebar.button("🚪 Logout", use_container_width=True):
    logout()
st.sidebar.markdown("---")





# ==================== THEME ====================
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

def toggle_theme():
    st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'

# زر التبديل في الـ Sidebar
theme_button = st.sidebar.button(
    "🌙" if st.session_state.theme == 'light' else "☀️",
    help="Toggle Dark/Light Mode",
    use_container_width=True
)
if theme_button:
    toggle_theme()
    st.rerun()

# تطبيق الثيم
if st.session_state.theme == 'dark':
    st.markdown("""
    <style>
    .stApp {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    .stSidebar {
        background-color: #2d2d2d;
    }
    .stMetric label {
        color: #ffffff !important;
    }
    .stMetric div {
        color: #ffffff !important;
    }
    .stDataFrame {
        background-color: #2d2d2d;
    }
    .stMarkdown {
        color: #ffffff !important;
    }
    .stSubheader {
        color: #ffffff !important;
    }
    .stAlert {
        background-color: #2d2d2d !important;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff;
        color: #000000;
    }
    .stSidebar {
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)


# ==================== CONVERT G-NETTRACK DATA ====================
def convert_gnetrack_data(df):
    """تحويل بيانات G-NetTrack للشكل المطلوب"""
    try:
        df = df.rename(columns={
            "Timestamp": "timestamp",
            "Latitude": "latitude",
            "Longitude": "longitude",
            "Level": "rsrp"
        })
        
        df["cell_id"] = 1
        df["rsrq"] = -10
        df["sinr"] = 15
        df["download_mbps"] = 30
        df["upload_mbps"] = 10
        df["latency_ms"] = 40
        
        df_final = df[["timestamp", "cell_id", "latitude", "longitude", 
                       "rsrp", "rsrq", "sinr", "download_mbps", 
                       "upload_mbps", "latency_ms"]]
        
        return df_final
    except Exception as e:
        st.error(f"❌ Conversion failed: {e}")
        return df

# ==================== COVERAGE HEATMAP ====================
def create_coverage_map_rsrp(data):
    """خريطة حرارية حسب RSRP"""
    try:
        center_lat = data['latitude'].mean()
        center_lon = data['longitude'].mean()
        m = folium.Map(location=[center_lat, center_lon], zoom_start=14)
        
        for _, row in data.iterrows():
            rsrp = row['rsrp']
            if rsrp >= -80:
                color = 'green'
                quality = 'Excellent'
            elif rsrp >= -90:
                color = 'lightgreen'
                quality = 'Good'
            elif rsrp >= -100:
                color = 'orange'
                quality = 'Fair'
            else:
                color = 'red'
                quality = 'Poor'
            
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=8,
                popup=f"""
                <b>Cell ID:</b> {row['cell_id']}<br>
                <b>RSRP:</b> {row['rsrp']} dBm<br>
                <b>Quality:</b> {quality}<br>
                <b>SINR:</b> {row['sinr']} dB
                """,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7
            ).add_to(m)
        
        # Legend
        legend_html = '''
        <div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000; background: white; padding: 10px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.3);">
            <p><strong>📊 RSRP Quality</strong></p>
            <p><span style="color:green;">●</span> Excellent (≥ -80 dBm)</p>
            <p><span style="color:lightgreen;">●</span> Good (-90 to -80)</p>
            <p><span style="color:orange;">●</span> Fair (-100 to -90)</p>
            <p><span style="color:red;">●</span> Poor (≤ -100 dBm)</p>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(legend_html))
        
        return m
    except Exception as e:
        st.error(f"❌ Error creating RSRP map: {e}")
        return None

def create_coverage_map_sinr(data):
    """خريطة حرارية حسب SINR"""
    try:
        center_lat = data['latitude'].mean()
        center_lon = data['longitude'].mean()
        m = folium.Map(location=[center_lat, center_lon], zoom_start=14)
        
        for _, row in data.iterrows():
            sinr = row['sinr']
            if sinr >= 20:
                color = 'green'
                quality = 'Excellent'
            elif sinr >= 13:
                color = 'lightgreen'
                quality = 'Good'
            elif sinr >= 5:
                color = 'orange'
                quality = 'Fair'
            else:
                color = 'red'
                quality = 'Poor'
            
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=8,
                popup=f"""
                <b>Cell ID:</b> {row['cell_id']}<br>
                <b>SINR:</b> {row['sinr']} dB<br>
                <b>Quality:</b> {quality}<br>
                <b>RSRP:</b> {row['rsrp']} dBm
                """,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7
            ).add_to(m)
        
        # Legend
        legend_html = '''
        <div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000; background: white; padding: 10px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.3);">
            <p><strong>📊 SINR Quality</strong></p>
            <p><span style="color:green;">●</span> Excellent (≥ 20 dB)</p>
            <p><span style="color:lightgreen;">●</span> Good (13-20 dB)</p>
            <p><span style="color:orange;">●</span> Fair (5-13 dB)</p>
            <p><span style="color:red;">●</span> Poor (≤ 5 dB)</p>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(legend_html))
        
        return m
    except Exception as e:
        st.error(f"❌ Error creating SINR map: {e}")
        return None

# ==================== HEADER ====================
st.title("📡 Telecom Network Analyzer")
st.markdown("---")

# ==================== LOAD DATA ====================
uploaded_file = st.file_uploader("📤 Upload CSV or TXT", type=["csv", "txt"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.txt'):
            data = pd.read_csv(uploaded_file, sep='\t')
            
            if 'Operatorname' in data.columns:
                data = convert_gnetrack_data(data)
                st.info("✅ Converted G-NetTrack data successfully")
            else:
                st.warning("⚠️ Unknown TXT format, please use CSV")
                data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_csv(uploaded_file)
            st.info("✅ CSV file loaded successfully")
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
        st.stop()
else:
    try:
        data = get_data_as_dataframe()
        if len(data) > 0:
            st.info(f"✅ Loaded {len(data)} measurements from database (telecom.db)")
        else:
            st.warning("⚠️ No data in database. Using sample data.")
            data = pd.read_csv("sample_data.csv")
    except Exception as e:
        st.warning(f"⚠️ Could not read from database: {e}")
        st.info("📁 Using sample_data.csv")
        data = pd.read_csv("sample_data.csv")

# ==================== ANALYZER ====================
analyzer = TelecomAnalyzer(data)
prepared_data = analyzer.prepare_data()
stats = analyzer.get_stats()
health = analyzer.health_score()

# ==================== ANALYZER ====================
analyzer = TelecomAnalyzer(data)
prepared_data = analyzer.prepare_data()
stats = analyzer.get_stats()
health = analyzer.health_score()

# ==================== UX SCORE ====================
prepared_data = analyzer.add_ux_score()  
ux_stats = analyzer.get_ux_statistics()

# ==================== HANDOVER ANALYSIS ====================
handovers = analyzer.detect_handovers()
handover_stats = analyzer.get_handover_statistics(handovers)
handover_pairs = analyzer.get_handover_pairs(handovers)

# ==================== TIME-SERIES FORECASTING ====================
# تنبؤ RSRP
future_dates_rsrp, forecast_rsrp, confidence_rsrp = analyzer.get_forecast('rsrp', steps=6)

# تنبؤ SINR
future_dates_sinr, forecast_sinr, confidence_sinr = analyzer.get_forecast('sinr', steps=6)

# تنبؤ Latency
future_dates_latency, forecast_latency, confidence_latency = analyzer.get_forecast('latency_ms', steps=6)

# تحليل الاتجاه
trend_rsrp = analyzer.get_trend_analysis('rsrp')
trend_sinr = analyzer.get_trend_analysis('sinr')
trend_latency = analyzer.get_trend_analysis('latency_ms')

# ==================== ANOMALY DETECTION ====================
# كشف الشذوذ
anomalies, anomaly_counts = analyzer.detect_all_anomalies()
prepared_data = analyzer.add_anomaly_score()
anomaly_stats = analyzer.get_anomaly_statistics()

# ==================== ROOT CAUSE ANALYSIS ====================
prepared_data = analyzer.add_root_cause_analysis()
rc_stats = analyzer.get_root_cause_statistics()

# ==================== ML PREDICTION ====================
ml_result = analyzer.train_ml_model()

if ml_result is not None and isinstance(ml_result, dict) and ml_result.get("model") is not None:
    model = ml_result["model"]
    accuracy = ml_result["accuracy"]
    feature_importance = ml_result["feature_importance"]
    X_test = ml_result["X_test"]
    y_test = ml_result["y_test"]
    n_samples = ml_result["n_samples"]
    
    # توقع كل البيانات
    prepared_data = analyzer.predict_all_problems(model)
    ml_stats = analyzer.get_ml_statistics(model, X_test, y_test)
    st.success(f"✅ ML Model trained on {n_samples} samples with accuracy: {accuracy:.1f}%")
else:
    ml_stats = None

# ==================== COVERAGE GAPS ====================
coverage_gaps = analyzer.detect_coverage_gaps()
gap_stats = analyzer.get_coverage_gap_statistics(coverage_gaps)
gap_recommendations = analyzer.get_coverage_recommendations(coverage_gaps)

# ==================== CAPACITY PLANNING ====================
capacity_data = analyzer.analyze_capacity()
capacity_recommendations = analyzer.get_capacity_recommendations(capacity_data) if capacity_data else []

# ==================== REAL-TIME DASHBOARD ====================
realtime_stats = analyzer.get_realtime_stats()
cells_status = analyzer.get_cells_status()










# تحسين الـ sidebar للموبايل
st.sidebar.markdown("""
<style>
    @media (max-width: 768px) {
        .stSidebar {
            width: 200px !important;
        }
        .stSidebar .stSelectbox label,
        .stSidebar .stMultiselect label,
        .stSidebar .stDateInput label {
            font-size: 11px !important;
        }
        .stSidebar .stMetric {
            padding: 4px !important;
        }
        .stSidebar .stMetric label {
            font-size: 10px !important;
        }
        .stSidebar .stMetric div {
            font-size: 14px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ==================== FILTERS =========================

st.sidebar.header("🔍 Filters")

# ==================== 1. Date Range Filter ====================
if 'timestamp' in prepared_data.columns:
    prepared_data['timestamp'] = pd.to_datetime(prepared_data['timestamp'])
    min_date = prepared_data['timestamp'].min()
    max_date = prepared_data['timestamp'].max()
    
    date_range = st.sidebar.date_input(
        "📅 Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        prepared_data = prepared_data[
            (prepared_data['timestamp'].dt.date >= start_date) &
            (prepared_data['timestamp'].dt.date <= end_date)
        ]

# ==================== 2. Cell ID Filter ====================
cells = sorted(prepared_data['cell_id'].unique())
selected_cells = st.sidebar.multiselect(
    "📡 Select Cells",
    cells,
    default=cells
)
prepared_data = prepared_data[prepared_data['cell_id'].isin(selected_cells)]

# ==================== 3. Signal Quality Filter (RSRP) ====================
signal_options = ['All', 'Excellent', 'Good', 'Fair', 'Poor']
selected_signal = st.sidebar.selectbox(
    "📶 Signal Quality (RSRP)",
    signal_options
)
if selected_signal != 'All':
    prepared_data = prepared_data[prepared_data['signal_quality'] == selected_signal]

# ==================== 4. SINR Quality Filter ====================
sinr_options = ['All', 'Excellent', 'Good', 'Fair', 'Poor']
selected_sinr = st.sidebar.selectbox(
    "📶 SINR Quality",
    sinr_options
)
if selected_sinr != 'All':
    prepared_data = prepared_data[prepared_data['sinr_quality'] == selected_sinr]

# ==================== 5. Problem Filter ====================
problem_filter = st.sidebar.selectbox(
    "⚠️ Problem Status",
    ["All", "Only Problems", "Only Healthy"]
)
if problem_filter == "Only Problems":
    prepared_data = prepared_data[prepared_data['problem'] == True]
elif problem_filter == "Only Healthy":
    prepared_data = prepared_data[prepared_data['problem'] == False]

# ==================== 6. Download Speed Filter ====================
st.sidebar.markdown("---")
st.sidebar.write("⬇️ Download Speed")
col1, col2 = st.sidebar.columns(2)
with col1:
    min_download = st.number_input(
        "Min",
        value=0.0,
        min_value=0.0,
        step=1.0,
        key="min_download"
    )
with col2:
    max_download = st.number_input(
        "Max",
        value=100.0,
        min_value=0.0,
        step=1.0,
        key="max_download"
    )
if min_download > 0 or max_download < 100:
    prepared_data = prepared_data[
        (prepared_data['download_mbps'] >= min_download) &
        (prepared_data['download_mbps'] <= max_download)
    ]

# ==================== 7. Upload Speed Filter ====================
st.sidebar.write("⬆️ Upload Speed")
col1, col2 = st.sidebar.columns(2)
with col1:
    min_upload = st.number_input(
        "Min",
        value=0.0,
        min_value=0.0,
        step=1.0,
        key="min_upload"
    )
with col2:
    max_upload = st.number_input(
        "Max",
        value=50.0,
        min_value=0.0,
        step=1.0,
        key="max_upload"
    )
if min_upload > 0 or max_upload < 50:
    prepared_data = prepared_data[
        (prepared_data['upload_mbps'] >= min_upload) &
        (prepared_data['upload_mbps'] <= max_upload)
    ]

# ==================== 8. Latency Filter ====================
st.sidebar.write("⏱️ Latency")
col1, col2 = st.sidebar.columns(2)
with col1:
    min_latency = st.number_input(
        "Min (ms)",
        value=0.0,
        min_value=0.0,
        step=5.0,
        key="min_latency"
    )
with col2:
    max_latency = st.number_input(
        "Max (ms)",
        value=200.0,
        min_value=0.0,
        step=5.0,
        key="max_latency"
    )
if min_latency > 0 or max_latency < 200:
    prepared_data = prepared_data[
        (prepared_data['latency_ms'] >= min_latency) &
        (prepared_data['latency_ms'] <= max_latency)
    ]
# ==================== 9. Time of Day Filter ====================
time_options = ['All', '🌅 Morning (6-12)', '☀️ Afternoon (12-18)', '🌆 Evening (18-24)', '🌙 Night (0-6)']
selected_time = st.sidebar.selectbox(
    "🕐 Time of Day",
    time_options
)
if selected_time != 'All':
    hour = prepared_data['timestamp'].dt.hour
    if selected_time == '🌅 Morning (6-12)':
        prepared_data = prepared_data[(hour >= 6) & (hour < 12)]
    elif selected_time == '☀️ Afternoon (12-18)':
        prepared_data = prepared_data[(hour >= 12) & (hour < 18)]
    elif selected_time == '🌆 Evening (18-24)':
        prepared_data = prepared_data[(hour >= 18) & (hour < 24)]
    elif selected_time == '🌙 Night (0-6)':
        prepared_data = prepared_data[(hour >= 0) & (hour < 6)]

# ==================== 10. Day of Week Filter ====================
day_options = ['All', 'Weekday (Mon-Fri)', 'Weekend (Sat-Sun)']
selected_day = st.sidebar.selectbox(
    "📅 Day of Week",
    day_options
)
if selected_day != 'All':
    day_of_week = prepared_data['timestamp'].dt.dayofweek
    if selected_day == 'Weekday (Mon-Fri)':
        prepared_data = prepared_data[day_of_week < 5]
    else:  # Weekend
        prepared_data = prepared_data[day_of_week >= 5]

# ==================== 11. Anomaly Filter ====================
if 'is_anomaly' in prepared_data.columns:
    anomaly_options = ['All', '🚨 Only Anomalies', '✅ Only Normal']
    selected_anomaly = st.sidebar.selectbox(
        "🚨 Anomaly Status",
        anomaly_options
    )
    if selected_anomaly == '🚨 Only Anomalies':
        prepared_data = prepared_data[prepared_data['is_anomaly'] == True]
    elif selected_anomaly == '✅ Only Normal':
        prepared_data = prepared_data[prepared_data['is_anomaly'] == False]

# ==================== 12. UX Score Filter ====================
if 'ux_category' in prepared_data.columns:
    ux_options = ['All', 'Excellent 🟢', 'Good 🟡', 'Fair 🟠', 'Poor 🔴']
    selected_ux = st.sidebar.selectbox(
        "⭐ UX Score",
        ux_options
    )
    if selected_ux != 'All':
        prepared_data = prepared_data[prepared_data['ux_category'] == selected_ux]

# ==================== 13. Severity Filter ====================
if 'severity' in prepared_data.columns:
    severity_options = ['All', '🔴 High', '🟡 Medium', '🟢 Low']
    selected_severity = st.sidebar.selectbox(
        "⚠️ Severity",
        severity_options
    )
    if selected_severity != 'All':
        prepared_data = prepared_data[prepared_data['severity'] == selected_severity]

# ==================== 14. Handover Filter ====================
if 'handover' in prepared_data.columns:
    handover_options = ['All', '🔄 Only Handovers', '🚫 No Handovers']
    selected_handover = st.sidebar.selectbox(
        "🔄 Handover Status",
        handover_options
    )
    if selected_handover == '🔄 Only Handovers':
        prepared_data = prepared_data[prepared_data['handover'] == True]
    elif selected_handover == '🚫 No Handovers':
        prepared_data = prepared_data[prepared_data['handover'] == False]

# ==================== 15. Coverage Gap Filter ====================
if 'is_gap' in prepared_data.columns:
    gap_options = ['All', '📍 Only Coverage Gaps', '✅ No Gaps']
    selected_gap = st.sidebar.selectbox(
        "📍 Coverage Gap",
        gap_options
    )
    if selected_gap == '📍 Only Coverage Gaps':
        prepared_data = prepared_data[prepared_data['is_gap'] == True]
    elif selected_gap == '✅ No Gaps':
        prepared_data = prepared_data[prepared_data['is_gap'] == False]

# ==================== 16. ML Prediction Filter ====================
if 'ml_result' in prepared_data.columns:
    ml_options = ['All', '⚠️ ML Predicts Problem', '✅ ML Predicts Healthy']
    selected_ml = st.sidebar.selectbox(
        "🤖 ML Prediction",
        ml_options
    )
    if selected_ml == '⚠️ ML Predicts Problem':
        prepared_data = prepared_data[prepared_data['ml_result'] == '⚠️ Problem']
    elif selected_ml == '✅ ML Predicts Healthy':
        prepared_data = prepared_data[prepared_data['ml_result'] == '✅ Healthy']

# ==================== 17. Reset All Filters ====================
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
    st.rerun()

# ==================== 18. Export Filtered Data ====================
st.sidebar.markdown("---")
if st.sidebar.button("📥 Export Filtered Data", use_container_width=True):
    csv = prepared_data.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"filtered_data.csv",
        mime="text/csv"
    )

# ==================== 19. Show Data Count ====================
st.sidebar.markdown("---")
st.sidebar.metric("📊 Total Records", len(prepared_data))

# ==================== DATA IMPORT FROM URL ====================
st.sidebar.markdown("---")
st.sidebar.subheader("🌐 Import from URL")

url_input = st.sidebar.text_input(
    "Enter CSV URL",
    placeholder="https://example.com/data.csv",
    key="url_input"
)

if st.sidebar.button("📥 Import from URL", use_container_width=True):
    if url_input:
        try:
            import requests
            from io import StringIO
            
            with st.spinner(f"Downloading data from {url_input}..."):
                response = requests.get(url_input, timeout=30)
                response.raise_for_status()
                
                # قراءة البيانات
                data = pd.read_csv(StringIO(response.text))
                
                if len(data) > 0:
                    st.session_state.imported_data = data
                    st.sidebar.success(f"✅ Loaded {len(data)} rows from URL!")
                    st.rerun()
                else:
                    st.sidebar.error("❌ No data found in the URL")
                    
        except requests.exceptions.Timeout:
            st.sidebar.error("❌ Connection timeout. Please check the URL.")
        except requests.exceptions.HTTPError as e:
            st.sidebar.error(f"❌ HTTP Error: {e}")
        except Exception as e:
            st.sidebar.error(f"❌ Error: {e}")
    else:
        st.sidebar.warning("⚠️ Please enter a valid URL")

# استخدام البيانات المستوردة
if 'imported_data' in st.session_state and st.session_state.imported_data is not None:
    data = st.session_state.imported_data
    st.info(f"✅ Using data imported from URL ({len(data)} rows)")








# ==================== COLUMNS RESPONSIVE ====================
if st.session_state.get('_is_mobile', False):
    col1, col2, col3, col4 = st.columns(2)
else:
    col1, col2, col3, col4 = st.columns(4)


# ==================== KPI CARDS ====================

st.subheader("📊 Network Overview")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🏥 Health Score", f"{health}/100")
with col2:
    st.metric("📡 Avg RSRP", f"{stats['avg_rsrp']:.1f} dBm")
with col3:
    st.metric("📶 Avg SINR", f"{stats['avg_sinr']:.1f} dB")
with col4:
    st.metric("⚠️ Problems", f"{stats['problems']}")

col5, col6, col7 = st.columns(3)
with col5:
    st.metric("⬇️ Download", f"{stats['avg_download']:.1f} Mbps")
with col6:
    st.metric("⬆️ Upload", f"{stats['avg_upload']:.1f} Mbps")
with col7:
    st.metric("⏱️ Latency", f"{stats['avg_latency']:.1f} ms")

st.markdown("---")

# ==================== ADVANCED ANALYTICS DASHBOARD ====================
with st.expander("📊 Advanced Analytics Dashboard", expanded=False):
    st.subheader("📈 Advanced Network Analytics")
    
    # تبويبات للتحليلات المتقدمة
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Statistics", "📈 Trends", "📉 Distributions", "📋 Summary"])
    
    with tab1:
        st.write("📊 Detailed Statistics")
        
        # إحصائيات متقدمة
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("Signal Statistics")
            signal_stats = {
                "RSRP Mean": f"{prepared_data['rsrp'].mean():.2f} dBm",
                "RSRP Median": f"{prepared_data['rsrp'].median():.2f} dBm",
                "RSRP Std": f"{prepared_data['rsrp'].std():.2f} dBm",
                "RSRP Min": f"{prepared_data['rsrp'].min():.2f} dBm",
                "RSRP Max": f"{prepared_data['rsrp'].max():.2f} dBm",
                "SINR Mean": f"{prepared_data['sinr'].mean():.2f} dB",
                "SINR Median": f"{prepared_data['sinr'].median():.2f} dB",
                "SINR Std": f"{prepared_data['sinr'].std():.2f} dB",
            }
            for key, value in signal_stats.items():
                st.write(f"• {key}: {value}")
        
        with col2:
            st.write("Performance Statistics")
            perf_stats = {
                "Download Mean": f"{prepared_data['download_mbps'].mean():.2f} Mbps",
                "Download Median": f"{prepared_data['download_mbps'].median():.2f} Mbps",
                "Download Std": f"{prepared_data['download_mbps'].std():.2f} Mbps",
                "Upload Mean": f"{prepared_data['upload_mbps'].mean():.2f} Mbps",
                "Upload Median": f"{prepared_data['upload_mbps'].median():.2f} Mbps",
                "Latency Mean": f"{prepared_data['latency_ms'].mean():.2f} ms",
                "Latency Median": f"{prepared_data['latency_ms'].median():.2f} ms",
                "Latency Std": f"{prepared_data['latency_ms'].std():.2f} ms",
            }
            for key, value in perf_stats.items():
                st.write(f"• {key}: {value}")
    
    with tab2:
        st.write("📈 Trend Analysis")
        
        # رسم الاتجاهات
        fig_col1, fig_col2 = st.columns(2)
        
        with fig_col1:
            # RSRP Trend with rolling average
            prepared_data['rsrp_rolling'] = prepared_data['rsrp'].rolling(window=3).mean()
            fig = px.line(
                prepared_data,
                x='timestamp',
                y=['rsrp', 'rsrp_rolling'],
                title='RSRP Trend (with 3-point rolling average)',
                labels={'value': 'RSRP (dBm)', 'timestamp': 'Time'}
            )
            st.plotly_chart(fig, use_container_width=True, key="advanced_rsrp_trend")
        
        with fig_col2:
            # SINR Trend with rolling average
            prepared_data['sinr_rolling'] = prepared_data['sinr'].rolling(window=3).mean()
            fig = px.line(
                prepared_data,
                x='timestamp',
                y=['sinr', 'sinr_rolling'],
                title='SINR Trend (with 3-point rolling average)',
                labels={'value': 'SINR (dB)', 'timestamp': 'Time'}
            )
            st.plotly_chart(fig, use_container_width=True, key="advanced_sinr_trend")
    
    with tab3:
        st.write("📉 Distributions")
        
        fig_col1, fig_col2 = st.columns(2)
        
        with fig_col1:
            # RSRP Distribution with KDE
            fig = px.histogram(
                prepared_data,
                x='rsrp',
                nbins=20,
                title='RSRP Distribution',
                labels={'rsrp': 'RSRP (dBm)'},
                color_discrete_sequence=['blue']
            )
            fig.add_vline(x=prepared_data['rsrp'].mean(), line_dash="dash", line_color="red", annotation_text="Mean")
            fig.add_vline(x=prepared_data['rsrp'].median(), line_dash="dash", line_color="green", annotation_text="Median")
            st.plotly_chart(fig, use_container_width=True, key="advanced_rsrp_dist")
        
        with fig_col2:
            # SINR Distribution with KDE
            fig = px.histogram(
                prepared_data,
                x='sinr',
                nbins=20,
                title='SINR Distribution',
                labels={'sinr': 'SINR (dB)'},
                color_discrete_sequence=['green']
            )
            fig.add_vline(x=prepared_data['sinr'].mean(), line_dash="dash", line_color="red", annotation_text="Mean")
            fig.add_vline(x=prepared_data['sinr'].median(), line_dash="dash", line_color="orange", annotation_text="Median")
            st.plotly_chart(fig, use_container_width=True, key="advanced_sinr_dist")
    
    with tab4:
        st.write("📋 Summary Report")
        
        # إنشاء ملخص شامل
        summary_data = {
            "Metric": [
                "Total Samples",
                "Health Score",
                "Total Problems",
                "Problem Percentage",
                "Average RSRP",
                "Average SINR",
                "Average Download",
                "Average Upload",
                "Average Latency",
                "Best Cell (RSRP)",
                "Worst Cell (RSRP)",
                "Best Cell (SINR)",
                "Worst Cell (SINR)"
            ],
            "Value": [
                len(prepared_data),
                f"{analyzer.health_score():.1f}/100",
                prepared_data['problem'].sum(),
                f"{(prepared_data['problem'].sum() / len(prepared_data) * 100):.1f}%",
                f"{prepared_data['rsrp'].mean():.2f} dBm",
                f"{prepared_data['sinr'].mean():.2f} dB",
                f"{prepared_data['download_mbps'].mean():.2f} Mbps",
                f"{prepared_data['upload_mbps'].mean():.2f} Mbps",
                f"{prepared_data['latency_ms'].mean():.2f} ms",
                f"Cell {prepared_data.groupby('cell_id')['rsrp'].mean().idxmax()} ({prepared_data.groupby('cell_id')['rsrp'].mean().max():.2f} dBm)",
                f"Cell {prepared_data.groupby('cell_id')['rsrp'].mean().idxmin()} ({prepared_data.groupby('cell_id')['rsrp'].mean().min():.2f} dBm)",
                f"Cell {prepared_data.groupby('cell_id')['sinr'].mean().idxmax()} ({prepared_data.groupby('cell_id')['sinr'].mean().max():.2f} dB)",
                f"Cell {prepared_data.groupby('cell_id')['sinr'].mean().idxmin()} ({prepared_data.groupby('cell_id')['sinr'].mean().min():.2f} dB)"
            ]
        }
        
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, use_container_width=True)
        
        # Export summary
        if st.button("📥 Export Summary as CSV", key="export_summary"):
            csv = summary_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Summary CSV",
                data=csv,
                file_name="advanced_summary.csv",
                mime="text/csv"
            )



# ==================== UX SCORE CARDS ====================
st.subheader("👤 User Experience Score")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("⭐ Avg UX Score", f"{ux_stats['avg_ux']:.1f}/100")
with col2:
    st.metric("🟢 Excellent", ux_stats['excellent_count'])
with col3:
    st.metric("🟡 Good", ux_stats['good_count'])
with col4:
    st.metric("🟠 Fair + 🔴 Poor", ux_stats['fair_count'] + ux_stats['poor_count'])

st.markdown("---")

# ==================== UX SCORE CHART ====================
st.subheader("📊 UX Score Distribution")

# Bar chart for UX categories
ux_dist = prepared_data['ux_category'].value_counts().reset_index()
ux_dist.columns = ["Category", "Count"]

# ترتيب التصنيفات
category_order = ["Excellent 🟢", "Good 🟡", "Fair 🟠", "Poor 🔴"]
ux_dist['Category'] = pd.Categorical(ux_dist['Category'], categories=category_order, ordered=True)
ux_dist = ux_dist.sort_values('Category')

fig = px.bar(
    ux_dist,
    x="Category",
    y="Count",
    color="Category",
    title="UX Score Distribution",
    color_discrete_map={
        "Excellent 🟢": "green",
        "Good 🟡": "gold",
        "Fair 🟠": "orange",
        "Poor 🔴": "red"
    }
)
st.plotly_chart(fig, width='stretch', key="ux_distribution")

# ==================== UX SCORE OVER TIME ====================
st.subheader("📈 UX Score Over Time")
fig = px.line(
    prepared_data,
    x="timestamp",
    y="ux_score",
    color="cell_id",
    markers=True,
    title="UX Score Trend"
)
fig.add_hline(y=80, line_dash="dash", annotation_text="✅ Excellent Threshold")
fig.add_hline(y=60, line_dash="dash", annotation_text="⚠️ Good Threshold")
st.plotly_chart(fig, width='stretch', key="ux_trend")

st.markdown("---")

# ==================== SIGNAL QUALITY CHARTS ====================
col1, col2 = st.columns(2)
with col1:
    st.subheader("📊 Signal Quality")
    signal_dist = prepared_data["signal_quality"].value_counts().reset_index()
    signal_dist.columns = ["Quality", "Count"]
    fig = px.bar(signal_dist, x="Quality", y="Count", color="Quality")
    st.plotly_chart(fig, width='stretch', key="signal_quality")

with col2:
    st.subheader("📊 SINR Quality")
    sinr_dist = prepared_data["sinr_quality"].value_counts().reset_index()
    sinr_dist.columns = ["Quality", "Count"]
    fig = px.bar(sinr_dist, x="Quality", y="Count", color="Quality")
    st.plotly_chart(fig, width='stretch', key="sinr_quality")

# ==================== RSRP OVER TIME ====================
st.subheader("📡 RSRP Over Time")
fig = px.line(
    prepared_data,
    x="timestamp",
    y="rsrp",
    color="cell_id",
    markers=True,
    title="RSRP Trend"
)
fig.add_hline(y=-100, line_dash="dash", annotation_text="⚠️ Poor Signal")
st.plotly_chart(fig, width='stretch', key="rsrp_trend")

# ==================== SINR OVER TIME ====================
st.subheader("📶 SINR Over Time")
fig = px.line(
    prepared_data,
    x="timestamp",
    y="sinr",
    color="cell_id",
    markers=True,
    title="SINR Trend"
)
fig.add_hline(y=5, line_dash="dash", annotation_text="⚠️ Poor SINR")
st.plotly_chart(fig, width='stretch', key="sinr_trend")

# ==================== SPEED ANALYSIS ====================
st.subheader("🚀 Download & Upload Speed")
speed_data = prepared_data.melt(
    id_vars=["timestamp"],
    value_vars=["download_mbps", "upload_mbps"],
    var_name="Type",
    value_name="Mbps"
)
fig = px.line(
    speed_data,
    x="timestamp",
    y="Mbps",
    color="Type",
    markers=True,
    title="Download / Upload Performance"
)
st.plotly_chart(fig, width='stretch', key="speed_trend")

# ==================== LATENCY OVER TIME ====================
st.subheader("⏱️ Latency Over Time")
fig = px.line(
    prepared_data,
    x="timestamp",
    y="latency_ms",
    color="cell_id",
    markers=True,
    title="Latency Trend"
)
fig.add_hline(y=100, line_dash="dash", annotation_text="⚠️ High Latency")
st.plotly_chart(fig, width='stretch', key="latency_trend")

# ==================== CELL PERFORMANCE ====================
st.subheader("📋 Cell Performance")
cell_stats = prepared_data.groupby("cell_id").agg(
    samples=("cell_id", "count"),
    avg_rsrp=("rsrp", "mean"),
    avg_sinr=("sinr", "mean"),
    avg_download=("download_mbps", "mean"),
    avg_latency=("latency_ms", "mean"),
    problems=("problem", "sum")
).reset_index()

st.dataframe(cell_stats.round(2), use_container_width=True)

# ==================== DETECTED PROBLEMS ====================
st.subheader("⚠️ Detected Problems")
problems = prepared_data[prepared_data["problem"]]

if len(problems) == 0:
    st.success("✅ No network problems detected!")
else:
    st.warning(f"⚠️ {len(problems)} problematic samples found")
    st.dataframe(
        problems[["timestamp", "cell_id", "rsrp", "sinr", "download_mbps", "latency_ms"]].round(2),
        use_container_width=True
    )

# ==================== HANDOVER ANALYSIS ====================
st.subheader("🔄 Cell Handover Analysis")

if handovers is not None and len(handovers) > 0:
    st.success(f"✅ {handover_stats['total_handovers']} handovers detected")
    
    # Handover Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🔄 Total Handovers", handover_stats['total_handovers'])
    with col2:
        st.metric("📡 Cells Involved", handover_stats['unique_cells'])
    with col3:
        avg_quality = handover_stats['quality_distribution']
        best_quality = max(avg_quality, key=avg_quality.get) if avg_quality else "N/A"
        st.metric("⭐ Best Quality", best_quality)
    
    # Quality Distribution
    col4, col5 = st.columns(2)
    with col4:
        st.write("Handover Quality Distribution")
        if handover_stats['quality_distribution']:
            quality_df = pd.DataFrame({
                'Quality': list(handover_stats['quality_distribution'].keys()),
                'Count': list(handover_stats['quality_distribution'].values())
            })
            fig = px.pie(quality_df, values='Count', names='Quality', title='Handover Quality')
            st.plotly_chart(fig, width='stretch', key="handover_quality_pie")
        else:
            st.info("No quality data available")
    
    with col5:
        st.write("Handover Pairs")
        st.dataframe(handover_pairs.round(2), width='stretch')
    
    # Handover Timeline
    st.subheader("📈 Handover Timeline")
    fig = px.scatter(
        handovers,
        x='timestamp',
        y='handover_quality',
        color='from_cell',
        hover_data=['to_cell', 'rsrp', 'sinr'],
        title='Handover Events Over Time'
    )
    st.plotly_chart(fig, width='stretch', key="handover_timeline")
    
else:
    st.info("ℹ️ No handovers detected. Need at least 2 different cells.")

# ==================== TIME-SERIES FORECASTING ====================
st.subheader("🔮 Network Performance Forecasting")

if forecast_rsrp is not None:
    st.success("✅ Forecast generated successfully")
    
    # Trend Analysis Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if trend_rsrp:
            st.metric("📡 RSRP Trend", trend_rsrp['trend'], delta=f"{trend_rsrp['change']:.1f} dBm")
    
    with col2:
        if trend_sinr:
            st.metric("📶 SINR Trend", trend_sinr['trend'], delta=f"{trend_sinr['change']:.1f} dB")
    
    with col3:
        if trend_latency:
            st.metric("⏱️ Latency Trend", trend_latency['trend'], delta=f"{trend_latency['change']:.1f} ms")
    
    st.markdown("---")
    
    # Forecast Charts
    tab1, tab2, tab3 = st.tabs(["📡 RSRP Forecast", "📶 SINR Forecast", "⏱️ Latency Forecast"])
    
    with tab1:
        st.write("RSRP Forecast - Next 30 Minutes")
        
        # بيانات تاريخية للـ RSRP
        ts_rsrp = analyzer.prepare_time_series('rsrp')
        historical_rsrp = ts_rsrp['rsrp'].tail(10)
        
        # إنشاء DataFrame للرسم
        forecast_df = pd.DataFrame({
            'timestamp': future_dates_rsrp,
            'value': forecast_rsrp,
            'type': 'Forecast'
        })
        
        historical_df = pd.DataFrame({
            'timestamp': historical_rsrp.index,
            'value': historical_rsrp.values,
            'type': 'Historical'
        })
        
        combined_df = pd.concat([historical_df, forecast_df])
        
        fig = px.line(
            combined_df,
            x='timestamp',
            y='value',
            color='type',
            markers=True,
            title='RSRP Forecast'
        )
        
        # إضافة مجال الثقة
        if confidence_rsrp:
            fig.add_scatter(
                x=future_dates_rsrp,
                y=[c[0] for c in confidence_rsrp],
                mode='lines',
                name='Lower Bound',
                line=dict(dash='dash', color='red')
            )
            fig.add_scatter(
                x=future_dates_rsrp,
                y=[c[1] for c in confidence_rsrp],
                mode='lines',
                name='Upper Bound',
                line=dict(dash='dash', color='green')
            )
        
        st.plotly_chart(fig, width='stretch', key="rsrp_forecast")
        
        # عرض التوقعات كجدول
        forecast_table = pd.DataFrame({
            'Time': [d.strftime('%H:%M') for d in future_dates_rsrp],
            'Forecast RSRP (dBm)': forecast_rsrp,
            'Lower Bound': [c[0] for c in confidence_rsrp] if confidence_rsrp else ['N/A']*len(forecast_rsrp),
            'Upper Bound': [c[1] for c in confidence_rsrp] if confidence_rsrp else ['N/A']*len(forecast_rsrp)
        })
        st.dataframe(forecast_table, width='stretch')
    
    with tab2:
        if forecast_sinr is not None:
            ts_sinr = analyzer.prepare_time_series('sinr')
            historical_sinr = ts_sinr['sinr'].tail(10)
            
            forecast_df = pd.DataFrame({
                'timestamp': future_dates_sinr,
                'value': forecast_sinr,
                'type': 'Forecast'
            })
            
            historical_df = pd.DataFrame({
                'timestamp': historical_sinr.index,
                'value': historical_sinr.values,
                'type': 'Historical'
            })
            
            combined_df = pd.concat([historical_df, forecast_df])
            
            fig = px.line(
                combined_df,
                x='timestamp',
                y='value',
                color='type',
                markers=True,
                title='SINR Forecast'
            )
            
            if confidence_sinr:
                fig.add_scatter(
                    x=future_dates_sinr,
                    y=[c[0] for c in confidence_sinr],
                    mode='lines',
                    name='Lower Bound',
                    line=dict(dash='dash', color='red')
                )
                fig.add_scatter(
                    x=future_dates_sinr,
                    y=[c[1] for c in confidence_sinr],
                    mode='lines',
                    name='Upper Bound',
                    line=dict(dash='dash', color='green')
                )
            
            st.plotly_chart(fig, width='stretch', key="sinr_forecast")
            
            forecast_table = pd.DataFrame({
                'Time': [d.strftime('%H:%M') for d in future_dates_sinr],
                'Forecast SINR (dB)': forecast_sinr,
                'Lower Bound': [c[0] for c in confidence_sinr] if confidence_sinr else ['N/A']*len(forecast_sinr),
                'Upper Bound': [c[1] for c in confidence_sinr] if confidence_sinr else ['N/A']*len(forecast_sinr)
            })
            st.dataframe(forecast_table, width='stretch')
        else:
            st.info("ℹ️ Not enough SINR data for forecasting")
    
    with tab3:
        if forecast_latency is not None:
            ts_latency = analyzer.prepare_time_series('latency_ms')
            historical_latency = ts_latency['latency_ms'].tail(10)
            
            forecast_df = pd.DataFrame({
                'timestamp': future_dates_latency,
                'value': forecast_latency,
                'type': 'Forecast'
            })
            
            historical_df = pd.DataFrame({
                'timestamp': historical_latency.index,
                'value': historical_latency.values,
                'type': 'Historical'
            })
            
            combined_df = pd.concat([historical_df, forecast_df])
            
            fig = px.line(
                combined_df,
                x='timestamp',
                y='value',
                color='type',
                markers=True,
                title='Latency Forecast'
            )
            
            if confidence_latency:
                fig.add_scatter(
                    x=future_dates_latency,
                    y=[c[0] for c in confidence_latency],
                    mode='lines',
                    name='Lower Bound',
                    line=dict(dash='dash', color='red')
                )
                fig.add_scatter(
                    x=future_dates_latency,
                    y=[c[1] for c in confidence_latency],
                    mode='lines',
                    name='Upper Bound',
                    line=dict(dash='dash', color='green')
                )
            
            st.plotly_chart(fig, width='stretch', key="latency_forecast")
            
            forecast_table = pd.DataFrame({
                'Time': [d.strftime('%H:%M') for d in future_dates_latency],
                'Forecast Latency (ms)': forecast_latency,
                'Lower Bound': [c[0] for c in confidence_latency] if confidence_latency else ['N/A']*len(forecast_latency),
                'Upper Bound': [c[1] for c in confidence_latency] if confidence_latency else ['N/A']*len(forecast_latency)
            })
            st.dataframe(forecast_table, width='stretch')
        else:
            st.info("ℹ️ Not enough Latency data for forecasting")
else:
    st.warning("⚠️ Not enough data for forecasting (need at least 3 data points)")

# ==================== ANOMALY DETECTION ====================
st.subheader("🚨 Anomaly Detection")

if anomaly_stats['total_anomalies'] > 0:
    st.warning(f"🚨 {anomaly_stats['total_anomalies']} anomalies detected ({anomaly_stats['anomaly_percentage']}% of data)")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🚨 Total Anomalies", anomaly_stats['total_anomalies'])
    with col2:
        st.metric("📊 Avg Score", f"{anomaly_stats['avg_anomaly_score']:.1f}")
    with col3:
        st.metric("📈 Max Score", f"{anomaly_stats['max_anomaly_score']:.1f}")
    with col4:
        st.metric("📊 Percentage", f"{anomaly_stats['anomaly_percentage']}%")
    
    # Anomaly Distribution by Column
    if anomaly_counts:
        st.write("Anomalies by Metric")
        anomaly_df = pd.DataFrame({
            'Metric': list(anomaly_counts.keys()),
            'Count': list(anomaly_counts.values())
        })
        fig = px.bar(
            anomaly_df,
            x='Metric',
            y='Count',
            color='Metric',
            title='Anomalies by Metric'
        )
        st.plotly_chart(fig, width='stretch', key="anomaly_distribution")
    
    # Anomaly Table
    st.write("Anomaly Details")
    if len(anomalies) > 0:
        display_cols = ['timestamp', 'cell_id', 'rsrp', 'sinr', 'download_mbps', 'latency_ms', 'anomaly_column']
        existing_cols = [col for col in display_cols if col in anomalies.columns]
        st.dataframe(anomalies[existing_cols].round(2), width='stretch')
    
    # Anomaly Scatter Plot
    st.subheader("📊 Anomaly Visualization")
    fig = px.scatter(
        prepared_data,
        x='timestamp',
        y='rsrp',
        color='is_anomaly',
        hover_data=['cell_id', 'sinr', 'download_mbps'],
        title='RSRP Anomalies Over Time',
        color_discrete_map={True: 'red', False: 'blue'}
    )
    st.plotly_chart(fig, width='stretch', key="anomaly_scatter")
    
else:
    st.success("✅ No anomalies detected in the data!")
    st.info("ℹ️ Anomaly detection uses IQR method to find unusual measurements.")

# ==================== ROOT CAUSE ANALYSIS ====================
st.subheader("🔍 Root Cause Analysis")

if rc_stats is not None:
    st.warning(f"🔍 {rc_stats['total_problems']} problems detected - Analyzing root causes")
    
    # Severity Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🔴 Critical (High)", rc_stats['severity_counts'].get('High', 0))
    with col2:
        st.metric("🟡 Warning (Medium)", rc_stats['severity_counts'].get('Medium', 0))
    with col3:
        st.metric("🟢 Info (Low)", rc_stats['severity_counts'].get('Low', 0))
    
    st.markdown("---")
    
    # Top Causes
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("📊 Top Causes")
        if rc_stats['cause_counts']:
            cause_df = pd.DataFrame({
                'Cause': list(rc_stats['cause_counts'].keys()),
                'Count': list(rc_stats['cause_counts'].values())
            }).head(5)
            fig = px.bar(
                cause_df,
                x='Count',
                y='Cause',
                orientation='h',
                title='Top Root Causes'
            )
            st.plotly_chart(fig, width='stretch', key="root_cause_top")
        else:
            st.info("No causes identified")
    
    with col2:
        st.write("🔍 Critical Cells")
        if rc_stats['critical_cells']:
            critical_data = []
            for cell in rc_stats['critical_cells']:
                cell_info = analyzer.get_cell_root_causes(cell)
                if cell_info:
                    critical_data.append({
                        "Cell": cell,
                        "Problems": cell_info['total_problems'],
                        "Top Cause": list(cell_info['common_causes'].keys())[0] if cell_info['common_causes'] else "None"
                    })
            st.dataframe(pd.DataFrame(critical_data), width='stretch')
        else:
            st.success("✅ No critical cells detected")
    
    st.markdown("---")
    
    # Detailed Cell Analysis
    st.subheader("📋 Detailed Cell Analysis")
    
    # اختيار خلية للتحليل
    cells_with_problems = prepared_data[prepared_data['problem']]['cell_id'].unique().tolist()
    
    if cells_with_problems:
        selected_cell = st.selectbox("Select Cell for Analysis", cells_with_problems)
        
        if selected_cell:
            cell_analysis = analyzer.get_cell_root_causes(selected_cell)
            
            if cell_analysis:
                st.write(f"Cell {selected_cell} Analysis")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("📊 Total Problems", cell_analysis['total_problems'])
                    st.write("Severity Distribution")
                    st.write(f"🔴 High: {cell_analysis['severity_counts'].get('High', 0)}")
                    st.write(f"🟡 Medium: {cell_analysis['severity_counts'].get('Medium', 0)}")
                    st.write(f"🟢 Low: {cell_analysis['severity_counts'].get('Low', 0)}")
                
                with col2:
                    st.write("Common Causes")
                    for cause, count in cell_analysis['common_causes'].items():
                        st.write(f"• {cause}: {count} times")
                    
                    st.write("Recommendations")
                    for rec in cell_analysis['recommendations']:
                        st.write(f"✅ {rec}")
else:
    st.info("ℹ️ No problems detected - root cause analysis not needed")

# ==================== ML PREDICTION ====================
# ==================== ML PREDICTION ====================
try:
    ml_result = analyzer.train_ml_model()
    
    if ml_result is not None and isinstance(ml_result, dict):
        model = ml_result.get('model')
        if model is not None:
            accuracy = ml_result.get('accuracy', 0)
            feature_importance = ml_result.get('feature_importance', {})
            X_test = ml_result.get('X_test')
            y_test = ml_result.get('y_test')
            n_samples = ml_result.get('n_samples', 0)
            
            # توقع كل البيانات
            prepared_data = analyzer.predict_all_problems(model)
            ml_stats = analyzer.get_ml_statistics(model, X_test, y_test)
            
            st.success(f"✅ Model trained on {n_samples} samples (Accuracy: {accuracy}%)")
            
            # ML Performance Cards
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("🎯 Accuracy", f"{ml_stats['accuracy']}%" if ml_stats else "N/A")
            with col2:
                st.metric("📊 Precision", f"{ml_stats['precision']}%" if ml_stats else "N/A")
            with col3:
                st.metric("📈 Recall", f"{ml_stats['recall']}%" if ml_stats else "N/A")
            with col4:
                st.metric("⭐ F1 Score", f"{ml_stats['f1_score']}%" if ml_stats else "N/A")
            
            st.markdown("---")
            
            # Feature Importance
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("📊 Feature Importance")
                if feature_importance:
                    importance_df = pd.DataFrame({
                        'Feature': list(feature_importance.keys()),
                        'Importance': list(feature_importance.values())
                    }).sort_values('Importance', ascending=True)
                    
                    fig = px.bar(
                        importance_df,
                        x='Importance',
                        y='Feature',
                        orientation='h',
                        title='What affects network problems most?'
                    )
                    st.plotly_chart(fig, use_container_width=True, key="ml_feature_importance")
                else:
                    st.info("No feature importance data")
            
            with col2:
                st.write("🔮 ML Predictions on Data")
                if 'ml_result' in prepared_data.columns:
                    pred_counts = prepared_data['ml_result'].value_counts().reset_index()
                    pred_counts.columns = ['Result', 'Count']
                    
                    fig = px.pie(
                        pred_counts,
                        values='Count',
                        names='Result',
                        title='ML Prediction Distribution',
                        color='Result',
                        color_discrete_map={
                            '⚠️ Problem': 'red',
                            '✅ Healthy': 'green'
                        }
                    )
                    st.plotly_chart(fig, use_container_width=True, key="ml_prediction_pie")
                else:
                    st.info("No predictions available")
            
            st.markdown("---")
            
            # Predict New Data
            st.subheader("🔮 Predict Single Measurement")
            st.write("Enter measurement values to predict if there's a problem:")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                predict_rsrp = st.number_input("RSRP (dBm)", value=-90.0, step=0.5, key="predict_rsrp")
                predict_sinr = st.number_input("SINR (dB)", value=15.0, step=0.5, key="predict_sinr")
            with col2:
                predict_download = st.number_input("Download (Mbps)", value=30.0, step=1.0, key="predict_download")
                predict_upload = st.number_input("Upload (Mbps)", value=10.0, step=1.0, key="predict_upload")
            with col3:
                predict_latency = st.number_input("Latency (ms)", value=50.0, step=1.0, key="predict_latency")
                predict_rsrq = st.number_input("RSRQ (dB)", value=-10.0, step=0.5, key="predict_rsrq")
            
            if st.button("🔮 Predict", key="predict_button"):
                predict_data = pd.DataFrame([{
                    'rsrp': predict_rsrp,
                    'rsrq': predict_rsrq,
                    'sinr': predict_sinr,
                    'download_mbps': predict_download,
                    'upload_mbps': predict_upload,
                    'latency_ms': predict_latency
                }])
                
                temp_analyzer = TelecomAnalyzer(pd.concat([prepared_data, predict_data]))
                temp_result = temp_analyzer.train_ml_model()
                
                if temp_result is not None and isinstance(temp_result, dict) and temp_result.get('model') is not None:
                    pred = temp_analyzer.predict_problem(predict_data.iloc[0], temp_result['model'])
                    if pred:
                        if "Problem" in pred['prediction']:
                            st.error(f"🚨 {pred['prediction']} (Confidence: {pred['confidence']}%)")
                        else:
                            st.success(f"✅ {pred['prediction']} (Confidence: {pred['confidence']}%)")
                        st.write(f"Prediction Confidence: {pred['confidence']}%")
                    else:
                        st.warning("Could not make prediction")
                else:
                    st.warning("Could not train model for prediction")
        else:
            st.warning("⚠️ Not enough data to train ML model (need at least 5 samples with both healthy and problem cases)")
            st.info("ℹ️ The model needs data with both healthy and problematic measurements to learn patterns.")
    else:
        st.warning("⚠️ Not enough data to train ML model (need at least 5 samples with both healthy and problem cases)")
        st.info("ℹ️ The model needs data with both healthy and problematic measurements to learn patterns.")
        
except Exception as e:
    st.warning(f"⚠️ ML Prediction skipped: {e}")
    st.info("ℹ️ Make sure you have at least 5 samples with both healthy and problematic measurements.")





# ==================== COVERAGE GAPS ====================
st.subheader("🗺️ Coverage Gaps Detection")

if gap_stats and gap_stats['has_gaps']:
    st.warning(f"⚠️ {gap_stats['total_gaps']} coverage gaps detected!")
    
    # Gap Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Total Gaps", gap_stats['total_gaps'])
    with col2:
        affected_cells = len(gap_stats['affected_cells'])
        st.metric("📡 Affected Cells", affected_cells)
    with col3:
        st.metric("📈 Gap Types", len(gap_stats['gap_types']))
    
    st.markdown("---")
    
    # Gap Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("📊 Gap Distribution")
        gap_df = pd.DataFrame({
            'Type': list(gap_stats['gap_counts'].keys()),
            'Count': list(gap_stats['gap_counts'].values())
        })
        fig = px.bar(
            gap_df,
            x='Type',
            y='Count',
            color='Type',
            title='Coverage Gaps by Type',
            color_discrete_map={
                'Weak Signal': 'orange',
                'Poor Quality': 'gold',
                'No Coverage': 'red'
            }
        )
        st.plotly_chart(fig, use_container_width=True, key="coverage_gaps_distribution")
    
    with col2:
        st.write("📈 Gap Percentages")
        gap_pct_df = pd.DataFrame({
            'Type': list(gap_stats['gap_percentages'].keys()),
            'Percentage': list(gap_stats['gap_percentages'].values())
        })
        fig = px.pie(
            gap_pct_df,
            values='Percentage',
            names='Type',
            title='Gap Percentage of Total Data',
            color='Type',
            color_discrete_map={
                'Weak Signal': 'orange',
                'Poor Quality': 'gold',
                'No Coverage': 'red'
            }
        )
        st.plotly_chart(fig, use_container_width=True, key="coverage_gaps_pie")
    
    st.markdown("---")
    
    # Recommendations
    st.subheader("💡 Coverage Recommendations")
    for rec in gap_recommendations:
        st.write(rec)
    
    # Gap Locations Map
    st.subheader("📍 Gap Locations")
    
    # تجميع نقاط الفجوات
    gap_data = pd.DataFrame()
    
    # Weak Signal
    weak_signal = prepared_data[prepared_data['rsrp'] < -100]
    if len(weak_signal) > 0:
        weak_signal['gap_type'] = 'Weak Signal'
        gap_data = pd.concat([gap_data, weak_signal])
    
    # No Coverage
    no_coverage = prepared_data[prepared_data['rsrp'] < -120]
    if len(no_coverage) > 0:
        no_coverage['gap_type'] = 'No Coverage'
        gap_data = pd.concat([gap_data, no_coverage])
    
    # Poor Quality
    poor_quality = prepared_data[prepared_data['sinr'] < 5]
    if len(poor_quality) > 0:
        poor_quality['gap_type'] = 'Poor Quality'
        gap_data = pd.concat([gap_data, poor_quality])
    
    if len(gap_data) > 0:
        gap_data = gap_data.drop_duplicates(subset=['timestamp', 'cell_id'])
        
        # عرض على الخريطة
        map_gaps = folium.Map(
            location=[gap_data['latitude'].mean(), gap_data['longitude'].mean()],
            zoom_start=14
        )
        
        for _, row in gap_data.iterrows():
            color_map = {
                'Weak Signal': 'orange',
                'Poor Quality': 'gold',
                'No Coverage': 'red'
            }
            color = color_map.get(row['gap_type'], 'gray')
            
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=10,
                popup=f"Type: {row['gap_type']}<br>RSRP: {row['rsrp']} dBm<br>SINR: {row['sinr']} dB",
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.8
            ).add_to(map_gaps)
        
        st_folium(map_gaps, width=1000, height=500)
    else:
        st.info("No gap location data available")
else:
    st.success("✅ No coverage gaps detected in the data!")
    st.info("ℹ️ Coverage gaps are areas with weak signal (RSRP < -100 dBm) or poor quality (SINR < 5 dB).")

# ==================== CAPACITY PLANNING ====================
st.subheader("📊 Capacity Planning")

if capacity_data:
    st.success(f"✅ Capacity analysis complete - {capacity_data['total_samples']} total samples")
    
    # Capacity Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Total Samples", capacity_data['total_samples'])
    with col2:
        st.metric("🕐 Peak Hour", f"{capacity_data['peak_hour']:02d}:00" if capacity_data['peak_hour'] is not None else "N/A")
    with col3:
        st.metric("📈 Peak Load", capacity_data['peak_load'])
    
    st.markdown("---")
    
    # Cell Capacity Analysis
    st.subheader("📋 Cell Capacity Analysis")
    
    cell_df = pd.DataFrame(capacity_data['cell_analysis'])
    
    # إضافة ألوان حسب الحالة
    def color_status(val):
        if val == "🔴 Critical":
            return 'background-color: #ffcccc'
        elif val == "🟡 Warning":
            return 'background-color: #fff3cd'
        else:
            return 'background-color: #d4edda'
    
    styled_cell_df = cell_df.style.map(color_status, subset=['status'])
    st.dataframe(styled_cell_df, use_container_width=True)
    
    st.markdown("---")
    
    # Capacity Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("📊 Problem Ratio by Cell")
        fig = px.bar(
            cell_df,
            x='cell_id',
            y='problem_ratio',
            color='status',
            title='Problem Ratio per Cell (%)',
            color_discrete_map={
                '🔴 Critical': 'red',
                '🟡 Warning': 'orange',
                '✅ Normal': 'green'
            }
        )
        st.plotly_chart(fig, use_container_width=True, key="capacity_problem_ratio")
    
    with col2:
        st.write("📈 Average Speed by Cell")
        fig = px.bar(
            cell_df,
            x='cell_id',
            y=['avg_download', 'avg_upload'],
            title='Download/Upload Speed per Cell',
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True, key="capacity_speed")
    
    st.markdown("---")
    
    # Peak Hour Chart
    st.subheader("📈 Hourly Load Distribution")
    
    # حساب التوزيع بالساعات
    prepared_data['hour'] = prepared_data['timestamp'].dt.hour
    hourly_data = prepared_data.groupby('hour').size().reset_index()
    hourly_data.columns = ['Hour', 'Count']
    
    fig = px.bar(
        hourly_data,
        x='Hour',
        y='Count',
        title='Network Activity by Hour',
        color='Count',
        color_continuous_scale='Blues'
    )
    
    # إضافة خط أوقات الذروة
    if capacity_data['peak_hour'] is not None:
        fig.add_vline(
            x=capacity_data['peak_hour'],
            line_dash="dash",
            line_color="red",
            annotation_text=f"Peak: {capacity_data['peak_hour']:02d}:00"
        )
    
    st.plotly_chart(fig, use_container_width=True, key="capacity_hourly")
    
    st.markdown("---")
    
    # Recommendations
    st.subheader("💡 Capacity Recommendations")
    for rec in capacity_recommendations:
        if rec.startswith("🔴"):
            st.error(rec)
        elif rec.startswith("🟡"):
            st.warning(rec)
        elif rec.startswith("✅"):
            st.success(rec)
        else:
            st.info(rec)
    
else:
    st.warning("⚠️ Not enough data for capacity analysis (need at least 1 sample)")
    st.info("ℹ️ Capacity planning analyzes network load and identifies bottlenecks.")

# ==================== REAL-TIME DASHBOARD ====================
st.subheader("⚡ Real-time Dashboard")

if realtime_stats and realtime_stats['total_samples'] > 0:
    
    # Auto-refresh
    auto_refresh = st.checkbox("🔄 Auto-refresh (every 600 seconds)", value=True)
    
    if auto_refresh:
        st.markdown("""
        <meta http-equiv="refresh" content="600">
        """, unsafe_allow_html=True)
        st.caption("⏳ Page will refresh automatically every 600 seconds")
    
    st.markdown("---")
    
    # Live Metrics Cards
    st.write("📊 Live Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📡 Total Samples", realtime_stats['total_samples'])
    with col2:
        st.metric("🏥 Health Score", f"{realtime_stats['current_health']}/100")
    with col3:
        st.metric("⚠️ Current Problems", realtime_stats['current_problems'])
    with col4:
        st.metric("⏱️ Last 5min Samples", realtime_stats['last_5min_samples'])
    
    st.markdown("---")
    
    # Last 5 Minutes Stats
    st.write("📈 Last 5 Minutes Averages")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        avg_rsrp = realtime_stats.get('avg_rsrp_5min')
        st.metric("📡 RSRP", f"{avg_rsrp:.1f} dBm" if avg_rsrp else "N/A")
    with col2:
        avg_sinr = realtime_stats.get('avg_sinr_5min')
        st.metric("📶 SINR", f"{avg_sinr:.1f} dB" if avg_sinr else "N/A")
    with col3:
        avg_download = realtime_stats.get('avg_download_5min')
        st.metric("⬇️ Download", f"{avg_download:.1f} Mbps" if avg_download else "N/A")
    with col4:
        avg_latency = realtime_stats.get('avg_latency_5min')
        st.metric("⏱️ Latency", f"{avg_latency:.1f} ms" if avg_latency else "N/A")
    
    st.markdown("---")
    
    # Latest Measurements
    st.write("📋 Latest Measurements")
    latest_df = pd.DataFrame(realtime_stats['latest_measurements'])
    if len(latest_df) > 0:
        st.dataframe(latest_df, use_container_width=True)
    
    st.markdown("---")
    
    # Cell Status
    st.write("📡 Cell Status")
    if cells_status:
        cell_status_df = pd.DataFrame(cells_status)
        
        # تنسيق الألوان
        def color_cell_status(val):
            if val == "🔴 Critical":
                return 'background-color: #ffcccc'
            elif val == "🟡 Warning":
                return 'background-color: #fff3cd'
            else:
                return 'background-color: #d4edda'
        
        styled_cell_df = cell_status_df.style.map(color_cell_status, subset=['status'])
        st.dataframe(styled_cell_df, use_container_width=True)
        
        # Cell Status Chart
        status_counts = cell_status_df['status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        
        fig = px.pie(
            status_counts,
            values='Count',
            names='Status',
            title='Cell Status Distribution',
            color='Status',
            color_discrete_map={
                '🟢 Excellent': 'green',
                '🟡 Warning': 'orange',
                '🔴 Critical': 'red'
            }
        )
        st.plotly_chart(fig, use_container_width=True, key="realtime_cell_status")
    
    st.markdown("---")
    
    # Last Update Time
    if realtime_stats.get('latest_timestamp'):
        st.caption(f"🕐 Last update: {realtime_stats['latest_timestamp']}")
    
else:
    st.warning("⚠️ No data available for real-time dashboard")
    st.info("ℹ️ Collect some measurements first to see real-time data")

# ==================== NETWORK SIMULATION ====================
st.subheader("🔮 Network Simulation (What-If Analysis)")

st.info("💡 Simulate the impact of network improvements on performance")

simulation_type = st.selectbox(
    "Select Improvement",
    [
        "Improve RSRP",
        "Improve SINR",
        "Reduce Latency",
        "Increase Bandwidth",
        "Add New Cell"
    ]
)

# إعدادات المحاكاة
col1, col2 = st.columns(2)

with col1:
    if simulation_type == "Improve RSRP":
        sim_value = st.slider("RSRP Improvement (dB)", min_value=1, max_value=20, value=5)
        sim_unit = "dB"
    elif simulation_type == "Improve SINR":
        sim_value = st.slider("SINR Improvement (dB)", min_value=1, max_value=20, value=5)
        sim_unit = "dB"
    elif simulation_type == "Reduce Latency":
        sim_value = st.slider("Latency Reduction (ms)", min_value=5, max_value=50, value=20)
        sim_unit = "ms"
    elif simulation_type == "Increase Bandwidth":
        sim_value = st.slider("Bandwidth Increase (%)", min_value=10, max_value=100, value=50)
        sim_unit = "%"
    elif simulation_type == "Add New Cell":
        sim_value = st.slider("New Cell RSRP Improvement (dB)", min_value=1, max_value=20, value=5)
        sim_unit = "dB"

with col2:
    st.write("Simulation Parameters")
    st.write(f"📊 Improvement Type: {simulation_type}")
    st.write(f"📈 Value: {sim_value} {sim_unit}")
    st.write(f"📡 Samples: {len(prepared_data)}")

if st.button("🚀 Run Simulation", use_container_width=True):
    with st.spinner("Running simulation..."):
        # تنفيذ المحاكاة
        simulated_data = analyzer.simulate_improvement(simulation_type, sim_value)
        
        # حساب التأثير
        impact = analyzer.get_simulation_impact(prepared_data, simulated_data)
        
        st.success("✅ Simulation complete!")
        
        # عرض النتائج
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🔴 Original Problems", impact['original_problems'])
        with col2:
            st.metric("🟢 Simulated Problems", impact['simulated_problems'])
        with col3:
            st.metric("📉 Problems Reduced", f"{impact['problems_reduced']} (-{impact['reduction_percentage']}%)")
        with col4:
            st.metric("📊 RSRP Improvement", f"+{impact['avg_rsrp_improvement']:.1f} dBm")
        
        # Chart: قبل وبعد
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("📊 Original vs Simulated RSRP")
            fig = px.histogram(
                pd.DataFrame({
                    'Original': prepared_data['rsrp'],
                    'Simulated': simulated_data['rsrp']
                }),
                title='RSRP Distribution Comparison'
            )
            st.plotly_chart(fig, use_container_width=True, key="sim_rsrp_hist")
        
        with col2:
            st.write("📊 Problem Reduction")
            prob_df = pd.DataFrame({
                'Status': ['Original Problems', 'Simulated Problems'],
                'Count': [impact['original_problems'], impact['simulated_problems']]
            })
            fig = px.bar(
                prob_df,
                x='Status',
                y='Count',
                color='Status',
                title='Problem Count Reduction'
            )
            st.plotly_chart(fig, use_container_width=True, key="sim_problem_bar")

# ==================== CUSTOM ALERTS ====================
st.subheader("🔔 Custom Alerts")

st.info("Set custom thresholds to get alerts when network performance drops below certain levels")

col1, col2 = st.columns(2)

with col1:
    st.write("📡 Signal Thresholds")
    alert_rsrp = st.slider("RSRP Alert Threshold (dBm)", min_value=-120, max_value=-80, value=-100)
    alert_sinr = st.slider("SINR Alert Threshold (dB)", min_value=0, max_value=20, value=5)

with col2:
    st.write("⚡ Performance Thresholds")
    alert_latency = st.slider("Latency Alert Threshold (ms)", min_value=50, max_value=200, value=100)
    alert_download = st.slider("Download Alert Threshold (Mbps)", min_value=0, max_value=50, value=10)

if st.button("🔍 Check Alerts", use_container_width=True):
    # تحليل البيانات
    alerts = []
    
    # 1. RSRP Alert
    rsrp_problems = prepared_data[prepared_data['rsrp'] < alert_rsrp]
    if len(rsrp_problems) > 0:
        alerts.append({
            "type": "📡 Weak Signal",
            "count": len(rsrp_problems),
            "percentage": round(len(rsrp_problems) / len(prepared_data) * 100, 1),
            "severity": "High" if len(rsrp_problems) > len(prepared_data) * 0.2 else "Medium",
            "suggestion": "Consider adding repeaters or improving coverage"
        })
    
    # 2. SINR Alert
    sinr_problems = prepared_data[prepared_data['sinr'] < alert_sinr]
    if len(sinr_problems) > 0:
        alerts.append({
            "type": "📶 Poor SINR",
            "count": len(sinr_problems),
            "percentage": round(len(sinr_problems) / len(prepared_data) * 100, 1),
            "severity": "High" if len(sinr_problems) > len(prepared_data) * 0.2 else "Medium",
            "suggestion": "Check for interference sources"
        })
    
    # 3. Latency Alert
    latency_problems = prepared_data[prepared_data['latency_ms'] > alert_latency]
    if len(latency_problems) > 0:
        alerts.append({
            "type": "⏱️ High Latency",
            "count": len(latency_problems),
            "percentage": round(len(latency_problems) / len(prepared_data) * 100, 1),
            "severity": "High" if len(latency_problems) > len(prepared_data) * 0.2 else "Medium",
            "suggestion": "Check backhaul and network load"
        })
    
    # 4. Download Alert
    download_problems = prepared_data[prepared_data['download_mbps'] < alert_download]
    if len(download_problems) > 0:
        alerts.append({
            "type": "⬇️ Low Download Speed",
            "count": len(download_problems),
            "percentage": round(len(download_problems) / len(prepared_data) * 100, 1),
            "severity": "High" if len(download_problems) > len(prepared_data) * 0.2 else "Medium",
            "suggestion": "Check capacity and bandwidth"
        })
    
    # عرض النتائج
    if alerts:
        st.warning(f"🚨 {len(alerts)} alerts triggered!")
        
        # عرض التنبيهات
        for alert in alerts:
            if alert['severity'] == "High":
                st.error(f"🔴 {alert['type']}: {alert['count']} samples ({alert['percentage']}%) - {alert['suggestion']}")
            else:
                st.warning(f"🟡 {alert['type']}: {alert['count']} samples ({alert['percentage']}%) - {alert['suggestion']}")
        
        # Chart
        alert_df = pd.DataFrame(alerts)
        fig = px.bar(
            alert_df,
            x='type',
            y='count',
            color='severity',
            title='Alerts Summary',
            color_discrete_map={
                'High': 'red',
                'Medium': 'orange'
            }
        )
        st.plotly_chart(fig, use_container_width=True, key="alerts_chart")
        
    else:
        st.success("✅ No alerts triggered! All metrics are within thresholds.")










# ==================== COVERAGE HEATMAP ====================
st.subheader("🗺️ Coverage Heatmap")

try:
    map_rsrp = create_coverage_map_rsrp(prepared_data)
    map_sinr = create_coverage_map_sinr(prepared_data)
    
    if map_rsrp and map_sinr:
        tab1, tab2 = st.tabs(["📡 RSRP Coverage", "📶 SINR Coverage"])
        
        with tab1:
            st.write("Signal Strength (RSRP) Coverage Map")
            st_folium(map_rsrp, width=1000, height=500)
        
        with tab2:
            st.write("Signal Quality (SINR) Coverage Map")
            st_folium(map_sinr, width=1000, height=500)
    else:
        st.warning("⚠️ Not enough data to create coverage map. Need at least 3 measurements with coordinates.")
except Exception as e:
    st.warning(f"⚠️ Could not create coverage map: {e}")
    st.info("💡 Make sure you have at least 3 measurements with latitude/longitude data.")
# ==================== DOWNLOAD RESULTS ====================
st.subheader("💾 Download Results")
csv = prepared_data.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name="analysis_results.csv",
    mime="text/csv"
)

# ==================== DATA COMPARISON ====================
st.subheader("📊 Data Comparison")

# اختيار نوع المقارنة
comparison_type = st.radio(
    "Select Comparison Type",
    ["Compare Two Periods", "Compare Two Cells"],
    horizontal=True
)

if comparison_type == "Compare Two Periods":
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("📅 Period 1")
        p1_start = st.date_input("Start 1", value=prepared_data['timestamp'].min().date(), key="p1_start")
        p1_end = st.date_input("End 1", value=prepared_data['timestamp'].max().date(), key="p1_end")
    
    with col2:
        st.write("📅 Period 2")
        p2_start = st.date_input("Start 2", value=prepared_data['timestamp'].min().date(), key="p2_start")
        p2_end = st.date_input("End 2", value=prepared_data['timestamp'].max().date(), key="p2_end")
    
    if st.button("🔍 Compare Periods"):
        p1_start_dt = pd.Timestamp(p1_start)
        p1_end_dt = pd.Timestamp(p1_end)
        p2_start_dt = pd.Timestamp(p2_start)
        p2_end_dt = pd.Timestamp(p2_end)
        
        comparison = analyzer.compare_periods(p1_start_dt, p1_end_dt, p2_start_dt, p2_end_dt)
        
        if comparison:
            st.success(f"✅ Period 1: {comparison['period1']['count']} samples, Period 2: {comparison['period2']['count']} samples")
            
            # عرض الفروقات
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                diff_rsrp = comparison['difference']['rsrp']
                delta_rsrp = f"{diff_rsrp:.1f} dBm"
                st.metric("📡 RSRP", f"{comparison['period2']['avg_rsrp']:.1f}", delta_rsrp)
            with col2:
                diff_sinr = comparison['difference']['sinr']
                delta_sinr = f"{diff_sinr:.1f} dB"
                st.metric("📶 SINR", f"{comparison['period2']['avg_sinr']:.1f}", delta_sinr)
            with col3:
                diff_download = comparison['difference']['download']
                delta_download = f"{diff_download:.1f} Mbps"
                st.metric("⬇️ Download", f"{comparison['period2']['avg_download']:.1f}", delta_download)
            with col4:
                diff_latency = comparison['difference']['latency']
                delta_latency = f"{diff_latency:.1f} ms"
                st.metric("⏱️ Latency", f"{comparison['period2']['avg_latency']:.1f}", delta_latency)
            
            # Chart
            fig = px.box(
                pd.concat([comparison['period1_data'], comparison['period2_data']]),
                x='timestamp',
                y='rsrp',
                color='timestamp',
                title='RSRP Comparison'
            )
            st.plotly_chart(fig, use_container_width=True, key="compare_periods_chart")
        else:
            st.warning("⚠️ No data in one of the periods")

elif comparison_type == "Compare Two Cells":
    cells = sorted(prepared_data['cell_id'].unique())
    col1, col2 = st.columns(2)
    
    with col1:
        cell1 = st.selectbox("📡 Cell 1", cells, key="cell1")
    with col2:
        cell2 = st.selectbox("📡 Cell 2", cells, key="cell2")
    
    if cell1 == cell2:
        st.warning("⚠️ Please select two different cells")
    elif st.button("🔍 Compare Cells"):
        comparison = analyzer.compare_cells(cell1, cell2)
        
        if comparison:
            st.success(f"✅ Cell {cell1}: {comparison['stats1']['count']} samples, Cell {cell2}: {comparison['stats2']['count']} samples")
            
            # عرض الفروقات
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                diff_rsrp = comparison['difference']['rsrp']
                delta_rsrp = f"{diff_rsrp:.1f} dBm"
                st.metric("📡 RSRP", f"{comparison['stats2']['avg_rsrp']:.1f}", delta_rsrp)
            with col2:
                diff_sinr = comparison['difference']['sinr']
                delta_sinr = f"{diff_sinr:.1f} dB"
                st.metric("📶 SINR", f"{comparison['stats2']['avg_sinr']:.1f}", delta_sinr)
            with col3:
                diff_download = comparison['difference']['download']
                delta_download = f"{diff_download:.1f} Mbps"
                st.metric("⬇️ Download", f"{comparison['stats2']['avg_download']:.1f}", delta_download)
            with col4:
                diff_latency = comparison['difference']['latency']
                delta_latency = f"{diff_latency:.1f} ms"
                st.metric("⏱️ Latency", f"{comparison['stats2']['avg_latency']:.1f}", delta_latency)
            
            # Chart
            combined = pd.concat([
                comparison['cell1_data'].assign(cell=cell1),
                comparison['cell2_data'].assign(cell=cell2)
            ])
            fig = px.box(
                combined,
                x='cell',
                y='rsrp',
                color='cell',
                title='RSRP Comparison'
            )
            st.plotly_chart(fig, use_container_width=True, key="compare_cells_chart")
        else:
            st.warning("⚠️ No data in one of the cells")

# ==================== EXPORT PDF ====================
st.subheader("📄 Export Report")

if st.button("📥 Download PDF Report"):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib.utils import ImageReader
        import io
        from datetime import datetime
        
        # Create PDF
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        
        # Title
        c.setFont("Helvetica-Bold", 24)
        c.drawString(50, height - 50, "Telecom Network Analysis Report")
        
        # Date
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 80, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # Summary
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 120, "Network Summary")
        
        c.setFont("Helvetica", 12)
        y = height - 150
        summary_data = [
            f"Health Score: {health}/100",
            f"Average RSRP: {stats['avg_rsrp']:.1f} dBm",
            f"Average SINR: {stats['avg_sinr']:.1f} dB",
            f"Download Speed: {stats['avg_download']:.1f} Mbps",
            f"Upload Speed: {stats['avg_upload']:.1f} Mbps",
            f"Latency: {stats['avg_latency']:.1f} ms",
            f"Total Samples: {len(prepared_data)}",
            f"Problems Detected: {stats['problems']}"
        ]
        
        for line in summary_data:
            c.drawString(50, y, line)
            y -= 25
        
        # Footer
        c.setFont("Helvetica", 10)
        c.drawString(50, 50, "Generated by Telecom Network Analyzer")
        c.drawString(50, 35, "© 2026 - All Rights Reserved")
        
        c.save()
        
        # Download
        st.download_button(
            label="📥 Download PDF Report",
            data=buffer.getvalue(),
            file_name=f"telecom_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf"
        )
    except ImportError:
        st.warning("⚠️ ReportLab not installed. Run: pip install reportlab")
    except Exception as e:
        st.error(f"❌ Error generating PDF: {e}")

# ==================== PDF REPORT (NEW) ====================
st.subheader("📄 Generate Detailed PDF Report")

if st.button("📥 Generate Detailed PDF Report"):
    with st.spinner("Generating detailed PDF report..."):
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas
            from reportlab.lib.utils import ImageReader
            import io
            from datetime import datetime
            
            # استخدم دالة التقرير من analyzer
            pdf_data = analyzer.generate_pdf_report()
            
            if pdf_data:
                st.download_button(
                    label="📥 Download Detailed PDF Report",
                    data=pdf_data,
                    file_name=f"telecom_detailed_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf"
                )
                st.success("✅ Detailed PDF report generated successfully!")
            else:
                st.error("❌ Could not generate PDF. Make sure reportlab is installed.")
        except Exception as e:
            st.error(f"❌ Error generating PDF: {e}")

# ==================== EXPORT TO EXCEL ====================
st.subheader("📊 Export to Excel")

if st.button("📥 Export to Excel"):
    with st.spinner("Generating Excel file..."):
        try:
            excel_data = analyzer.export_to_excel()
            if excel_data:
                st.download_button(
                    label="📥 Download Excel Report",
                    data=excel_data,
                    file_name=f"network_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                st.success("✅ Excel report generated successfully!")
            else:
                st.error("❌ Could not generate Excel file")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# ==================== DATA QUALITY REPORT ====================
st.subheader("📋 Data Quality Report")

if st.button("📊 Generate Data Quality Report", use_container_width=True):
    with st.spinner("Analyzing data quality..."):
        
        # ===== 1. Missing Values =====
        missing_data = prepared_data.isnull().sum()
        missing_data = missing_data[missing_data > 0]
        
        # ===== 2. Duplicate Rows =====
        duplicates = prepared_data.duplicated().sum()
        
        # ===== 3. Outliers =====
        outlier_cols = ['rsrp', 'sinr', 'download_mbps', 'upload_mbps', 'latency_ms']
        outliers = {}
        for col in outlier_cols:
            if col in prepared_data.columns:
                Q1 = prepared_data[col].quantile(0.25)
                Q3 = prepared_data[col].quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 - 1.5 * IQR
                upper = Q3 + 1.5 * IQR
                outlier_count = len(prepared_data[(prepared_data[col] < lower) | (prepared_data[col] > upper)])
                outliers[col] = outlier_count
        
        # ===== 4. Data Types =====
        dtypes = prepared_data.dtypes
        
        # ===== 5. Unique Values =====
        unique_counts = prepared_data.nunique()
        
        # عرض التقرير
        st.success("✅ Data Quality Report Generated!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("🔍 Missing Values")
            if len(missing_data) > 0:
                st.dataframe(missing_data.reset_index().rename(columns={'index': 'Column', 0: 'Missing Count'}))
            else:
                st.info("✅ No missing values found")
            
            st.write("📊 Duplicate Rows")
            st.metric("Duplicate Rows", duplicates)
            
            st.write("📈 Outliers")
            outlier_df = pd.DataFrame({
                'Column': list(outliers.keys()),
                'Outlier Count': list(outliers.values())
            })
            st.dataframe(outlier_df, use_container_width=True)
        
        with col2:
            st.write("📋 Data Types")
            st.dataframe(dtypes.reset_index().rename(columns={'index': 'Column', 0: 'Data Type'}))
            
            st.write("🔢 Unique Values")
            st.dataframe(unique_counts.reset_index().rename(columns={'index': 'Column', 0: 'Unique Count'}))
        
        # ===== 6. Quality Score =====
        st.subheader("📊 Data Quality Score")
        
        # حساب درجة الجودة
        quality_score = 100
        
        # خصم النقاط للمفقودات
        if len(missing_data) > 0:
            quality_score -= min(len(missing_data) * 5, 30)
        
        # خصم النقاط للتكرار
        if duplicates > 0:
            quality_score -= min(duplicates * 2, 20)
        
        # خصم النقاط للشواذ
        total_outliers = sum(outliers.values())
        if total_outliers > 0:
            quality_score -= min(int(total_outliers * 0.5), 20)
        
        quality_score = max(0, quality_score)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Quality Score", f"{quality_score}/100")
        with col2:
            status = "🟢 Good" if quality_score >= 80 else "🟡 Fair" if quality_score >= 60 else "🔴 Poor"
            st.metric("📈 Status", status)
        with col3:
            st.metric("📋 Total Issues", len(missing_data) + duplicates + total_outliers)
        
        # ===== 7. Recommendations =====
        st.subheader("💡 Data Quality Recommendations")
        
        recommendations = []
        
        if len(missing_data) > 0:
            recommendations.append(f"🔴 Missing Data: {len(missing_data)} columns have missing values. Consider imputing or removing them.")
        if duplicates > 0:
            recommendations.append(f"🟡 Duplicate Rows: {duplicates} duplicate rows found. Consider removing them.")
        
        if total_outliers > 0:
            recommendations.append(f"🟡 Outliers: {total_outliers} outliers detected. Consider investigating or removing them.")
        
        if not recommendations:
            recommendations.append("✅ Data quality looks good! No major issues detected.")
        
        for rec in recommendations:
            st.write(rec)
        
        # ===== 8. Download Report =====
        if st.button("📥 Download Quality Report", key="download_quality"):
            report_data = {
                "Metric": ["Missing Values", "Duplicate Rows", "Total Outliers", "Quality Score"],
                "Value": [len(missing_data), duplicates, total_outliers, quality_score]
            }
            report_df = pd.DataFrame(report_data)
            csv = report_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Quality Report CSV",
                data=csv,
                file_name="data_quality_report.csv",
                mime="text/csv"
            )

# ==================== FOOTER ====================
st.markdown("---")
st.caption("Telecom Network Analyzer | Built with Python + Streamlit + Plotly")
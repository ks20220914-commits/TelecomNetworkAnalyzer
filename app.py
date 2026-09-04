import streamlit as st
import pandas as pd
import plotly.express as px
from analyzer import TelecomAnalyzer
from db_helper import get_data_as_dataframe

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="📡 Telecom Analyzer",
    page_icon="📡",
    layout="wide"
)

# ==================== CONVERT G-NETTRACK DATA ====================
def convert_gnetrack_data(df):
    """تحويل بيانات G-NetTrack للشكل المطلوب"""
    try:
        # غير الأسماء
        df = df.rename(columns={
            "Timestamp": "timestamp",
            "Latitude": "latitude",
            "Longitude": "longitude",
            "Level": "rsrp"
        })
        
        # أضف الأعمدة الناقصة بقيم افتراضية
        df["cell_id"] = 1
        df["rsrq"] = -10
        df["sinr"] = 15
        df["download_mbps"] = 30
        df["upload_mbps"] = 10
        df["latency_ms"] = 40
        
        # اختار الأعمدة المطلوبة
        df_final = df[["timestamp", "cell_id", "latitude", "longitude", 
                       "rsrp", "rsrq", "sinr", "download_mbps", 
                       "upload_mbps", "latency_ms"]]
        
        return df_final
    except Exception as e:
        st.error(f"❌ تحويل البيانات فشل: {e}")
        return df

# ==================== HEADER ====================
st.title("📡 Telecom Network Analyzer")
st.markdown("---")

# ==================== LOAD DATA ====================
uploaded_file = st.file_uploader("📤 Upload CSV or TXT", type=["csv", "txt"])

if uploaded_file:
    try:
        # لو الملف txt من G-NetTrack
        if uploaded_file.name.endswith('.txt'):
            data = pd.read_csv(uploaded_file, sep='\t')
            
            # شوف لو فيه الأعمدة المطلوبة
            if 'Operatorname' in data.columns:
                data = convert_gnetrack_data(data)
                st.info("✅ تم تحويل بيانات G-NetTrack بنجاح")
            else:
                st.warning("⚠️ تنسيق TXT غير معروف، حاول تستخدم CSV")
                data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_csv(uploaded_file)
            st.info("✅ تم تحميل ملف CSV بنجاح")
    except Exception as e:
        st.error(f"❌ خطأ في قراءة الملف: {e}")
        st.stop()
else:
    # نحاول نقرا من قاعدة البيانات
    try:
        data = get_data_as_dataframe()
        if len(data) > 0:
            st.info(f"✅ Loaded {len(data)} measurements from database (telecom.db)")
        else:
            st.warning("⚠️no data found in database, using sample_data.csv")
            data = pd.read_csv("sample_data.csv")
    except Exception as e:
        st.warning(f"⚠️ Database cannot be read: {e}")
        st.info("📁using sample_data.csv")
        data = pd.read_csv("sample_data.csv")

# ==================== ANALYZER ====================
analyzer = TelecomAnalyzer(data)
prepared_data = analyzer.prepare_data()
stats = analyzer.get_stats()
health = analyzer.health_score()

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

# ==================== SIGNAL QUALITY CHARTS ====================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Signal Quality")
    signal_dist = prepared_data["signal_quality"].value_counts().reset_index()
    signal_dist.columns = ["Quality", "Count"]
    fig = px.bar(signal_dist, x="Quality", y="Count", color="Quality")
    st.plotly_chart(fig, use_container_width=True, key="signal_quality")

with col2:
    st.subheader("📊 SINR Quality")
    sinr_dist = prepared_data["sinr_quality"].value_counts().reset_index()
    sinr_dist.columns = ["Quality", "Count"]
    fig = px.bar(sinr_dist, x="Quality", y="Count", color="Quality")
    st.plotly_chart(fig, use_container_width=True, key="sinr_quality")

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
st.plotly_chart(fig, use_container_width=True, key="rsrp_trend")

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
st.plotly_chart(fig, use_container_width=True, key="sinr_trend")

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
st.plotly_chart(fig, use_container_width=True, key="speed_trend")

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
st.plotly_chart(fig, use_container_width=True, key="latency_trend")

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

# ==================== LOCATION MAP ====================
st.subheader("🗺️ Location Map")
map_data = prepared_data[["latitude", "longitude", "rsrp", "cell_id"]].copy()
st.map(map_data, latitude="latitude", longitude="longitude")

# ==================== DOWNLOAD RESULTS ====================
st.subheader("💾 Download Results")
csv = prepared_data.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name="analysis_results.csv",
    mime="text/csv"
)

# ==================== FOOTER ====================
st.markdown("---")
st.caption("Telecom Network Analyzer | Built with Python + Streamlit + Plotly")
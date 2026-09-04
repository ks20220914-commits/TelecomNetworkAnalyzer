import streamlit as st
import pandas as pd
import plotly.express as px
from analyzer import TelecomAnalyzer

# إعدادات الصفحة
st.set_page_config(page_title="📡 Telecom Analyzer", page_icon="📡", layout="wide")

# العنوان
st.title("📡 Telecom Network Analyzer")
st.markdown("---")

# رفع الملف
uploaded_file = st.file_uploader("📤 Upload CSV", type=["csv"])

# تحميل البيانات
if uploaded_file:
    data = pd.read_csv(uploaded_file)
else:
    # بيانات تجريبية لو مفيش ملف
    try:
        data = pd.read_csv("sample_data.csv")
        st.info("✅ Using sample data - upload your own CSV if needed")
    except:
        st.error("❌ Please upload a CSV file or add sample_data.csv")
        st.stop()

# تحليل البيانات
analyzer = TelecomAnalyzer(data)
prepared_data = analyzer.prepare_data()
stats = analyzer.get_stats()
health = analyzer.health_score()

# ========== KPI CARDS ==========
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

# ========== CHARTS ==========
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Signal Quality")
    signal_dist = prepared_data["signal_quality"].value_counts().reset_index()
    signal_dist.columns = ["Quality", "Count"]
    fig = px.bar(signal_dist, x="Quality", y="Count", color="Quality")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📊 SINR Quality")
    sinr_dist = prepared_data["sinr_quality"].value_counts().reset_index()
    sinr_dist.columns = ["Quality", "Count"]
    fig = px.bar(sinr_dist, x="Quality", y="Count", color="Quality")
    st.plotly_chart(fig, use_container_width=True)

# ========== RSRP OVER TIME ==========
st.subheader("📡 RSRP Over Time")
fig = px.line(prepared_data, x="timestamp", y="rsrp", color="cell_id", 
              markers=True, title="RSRP Trend")
fig.add_hline(y=-100, line_dash="dash", annotation_text="⚠️ Poor Signal")
st.plotly_chart(fig, use_container_width=True)

# ========== SINR OVER TIME ==========
st.subheader("📶 SINR Over Time")
fig = px.line(prepared_data, x="timestamp", y="sinr", color="cell_id",
              markers=True, title="SINR Trend")
fig.add_hline(y=5, line_dash="dash", annotation_text="⚠️ Poor SINR")
st.plotly_chart(fig, use_container_width=True)

# ========== SPEED ==========
st.subheader("🚀 Download & Upload Speed")
speed_data = prepared_data.melt(id_vars=["timestamp"], 
                                value_vars=["download_mbps", "upload_mbps"],
                                var_name="Type", value_name="Mbps")
fig = px.line(speed_data, x="timestamp", y="Mbps", color="Type", markers=True)
st.plotly_chart(fig, use_container_width=True)

# ========== LATENCY ==========
st.subheader("⏱️ Latency Over Time")
fig = px.line(prepared_data, x="timestamp", y="latency_ms", color="cell_id",
              markers=True, title="Latency Trend")
fig.add_hline(y=100, line_dash="dash", annotation_text="⚠️ High Latency")
st.plotly_chart(fig, use_container_width=True)

# ========== CELL STATISTICS ==========
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

# ========== PROBLEMS ==========
st.subheader("⚠️ Detected Problems")
problems = prepared_data[prepared_data["problem"]]
if len(problems) == 0:
    st.success("✅ No network problems detected!")
else:
    st.warning(f"⚠️ {len(problems)} problematic samples found")
    st.dataframe(problems[["timestamp", "cell_id", "rsrp", "sinr", 
                          "download_mbps", "latency_ms"]].round(2), 
                 use_container_width=True)

# ========== MAP ==========
st.subheader("🗺️ Location Map")
map_data = prepared_data[["latitude", "longitude", "rsrp", "cell_id"]].copy()
st.map(map_data, latitude="latitude", longitude="longitude")

# ========== DOWNLOAD ==========
st.subheader("💾 Download Results")
csv = prepared_data.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download CSV", csv, "analysis_results.csv", "text/csv")

# ========== FOOTER ==========
st.markdown("---")
st.caption("Telecom Network Analyzer | Built with Python + Streamlit + Plotly")
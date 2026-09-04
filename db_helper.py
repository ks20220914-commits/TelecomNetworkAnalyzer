import sqlite3
import pandas as pd

DB_NAME = "telecom.db"

def get_data_as_dataframe():
    """جلب كل البيانات من قاعدة البيانات"""
    try:
        conn = sqlite3.connect(DB_NAME)
        
        query = """
            SELECT 
                timestamp,
                cell_id,
                latitude,
                longitude,
                rsrp,
                rsrq,
                sinr,
                download_mbps,
                upload_mbps,
                latency_ms
            FROM measurements
            ORDER BY timestamp ASC
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()

def get_measurements_count():
    """عدد القياسات"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM measurements")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except:
        return 0

def get_latest_measurement():
    """أحدث قياس"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM measurements ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        return row
    except:
        return None
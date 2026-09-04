import pandas as pd

class TelecomAnalyzer:
    def __init__(self, data):
        self.data = data.copy()
    
    def prepare_data(self):
        """تجهيز البيانات وتحويلها للصحيح"""
        # تحويل الوقت
        self.data["timestamp"] = pd.to_datetime(self.data["timestamp"], errors="coerce")
        
        # تحويل الأرقام
        numeric_cols = ["latitude", "longitude", "rsrp", "rsrq", "sinr", 
                       "download_mbps", "upload_mbps", "latency_ms"]
        for col in numeric_cols:
            self.data[col] = pd.to_numeric(self.data[col], errors="coerce")
        
        # حذف القيم الفارغة
        self.data.dropna(subset=numeric_cols, inplace=True)
        
        # تصنيف الإشارة
        self.data["signal_quality"] = self.data["rsrp"].apply(self.classify_signal)
        
        # تصنيف SINR
        self.data["sinr_quality"] = self.data["sinr"].apply(self.classify_sinr)
        
        # اكتشاف المشاكل
        self.data["weak_signal"] = self.data["rsrp"] < -100
        self.data["poor_sinr"] = self.data["sinr"] < 5
        self.data["high_latency"] = self.data["latency_ms"] > 100
        self.data["low_download"] = self.data["download_mbps"] < 10
        self.data["problem"] = (self.data["weak_signal"] | self.data["poor_sinr"] | 
                               self.data["high_latency"] | self.data["low_download"])
        
        return self.data
    
    def classify_signal(self, rsrp):
        if rsrp >= -80: return "Excellent"
        elif rsrp >= -90: return "Good"
        elif rsrp >= -100: return "Fair"
        else: return "Poor"
    
    def classify_sinr(self, sinr):
        if sinr >= 20: return "Excellent"
        elif sinr >= 13: return "Good"
        elif sinr >= 5: return "Fair"
        else: return "Poor"
    
    def get_stats(self):
        """إحصائيات سريعة"""
        return {
            "avg_rsrp": self.data["rsrp"].mean(),
            "avg_sinr": self.data["sinr"].mean(),
            "avg_download": self.data["download_mbps"].mean(),
            "avg_upload": self.data["upload_mbps"].mean(),
            "avg_latency": self.data["latency_ms"].mean(),
            "total_samples": len(self.data),
            "problems": self.data["problem"].sum()
        }
    
    def health_score(self):
        """حساب درجة صحة الشبكة"""
        score = 100
        avg_rsrp = self.data["rsrp"].mean()
        avg_sinr = self.data["sinr"].mean()
        avg_latency = self.data["latency_ms"].mean()
        avg_download = self.data["download_mbps"].mean()
        
        if avg_rsrp < -100: score -= 25
        elif avg_rsrp < -90: score -= 10
        
        if avg_sinr < 5: score -= 25
        elif avg_sinr < 10: score -= 10
        
        if avg_latency > 100: score -= 20
        elif avg_latency > 50: score -= 10
        
        if avg_download < 10: score -= 20
        elif avg_download < 25: score -= 10
        
        return max(0, min(100, score))
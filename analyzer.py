import pandas as pd

class TelecomAnalyzer:
    def __init__(self, data):
        self.data = data.copy()
    
    def prepare_data(self):
        """تجهيز البيانات وتحويلها للصحيح"""
        self.data["timestamp"] = pd.to_datetime(self.data["timestamp"], errors="coerce")
        
        numeric_cols = ["latitude", "longitude", "rsrp", "rsrq", "sinr", 
                    "download_mbps", "upload_mbps", "latency_ms"]
        for col in numeric_cols:
            self.data[col] = pd.to_numeric(self.data[col], errors="coerce")
        
        self.data.dropna(subset=numeric_cols, inplace=True)
        
        self.data["signal_quality"] = self.data["rsrp"].apply(self.classify_signal)
        self.data["sinr_quality"] = self.data["sinr"].apply(self.classify_sinr)
        
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
    
    # ==================== UX SCORE ====================
    def calculate_ux_score(self, row):
        rsrp = row['rsrp']
        sinr = row['sinr']
        latency = row['latency_ms']
        download = row['download_mbps']
        
        if rsrp <= -140: rsrp_score = 0
        elif rsrp >= -60: rsrp_score = 100
        else: rsrp_score = ((rsrp + 140) / 80) * 100
        
        if sinr <= -10: sinr_score = 0
        elif sinr >= 30: sinr_score = 100
        else: sinr_score = ((sinr + 10) / 40) * 100
        
        if latency >= 200: latency_score = 0
        elif latency <= 10: latency_score = 100
        else: latency_score = ((200 - latency) / 190) * 100
        
        if download >= 100: download_score = 100
        elif download <= 0: download_score = 0
        else: download_score = (download / 100) * 100
        
        ux_score = (rsrp_score * 0.3) + (sinr_score * 0.3) + (latency_score * 0.2) + (download_score * 0.2)
        return round(ux_score, 1)
    
    def add_ux_score(self):
        self.data['ux_score'] = self.data.apply(self.calculate_ux_score, axis=1)
        self.data['ux_category'] = self.data['ux_score'].apply(self.classify_ux)
        return self.data
    
    def classify_ux(self, score):
        if score >= 80: return "Excellent 🟢"
        elif score >= 60: return "Good 🟡"
        elif score >= 40: return "Fair 🟠"
        else: return "Poor 🔴"
    
    def get_ux_statistics(self):
        if 'ux_score' not in self.data.columns:
            self.add_ux_score()
        
        return {
            "avg_ux": self.data['ux_score'].mean(),
            "min_ux": self.data['ux_score'].min(),
            "max_ux": self.data['ux_score'].max(),
            "excellent_count": len(self.data[self.data['ux_category'] == "Excellent 🟢"]),
            "good_count": len(self.data[self.data['ux_category'] == "Good 🟡"]),
            "fair_count": len(self.data[self.data['ux_category'] == "Fair 🟠"]),
            "poor_count": len(self.data[self.data['ux_category'] == "Poor 🔴"])
        }
    
    # ==================== HANDOVER ANALYSIS ====================
    def detect_handovers(self):
        if 'cell_id' not in self.data.columns:
            return None
        
        df = self.data.sort_values('timestamp').reset_index(drop=True)
        df['prev_cell'] = df['cell_id'].shift(1)
        df['cell_changed'] = df['cell_id'] != df['prev_cell']
        df['handover'] = df['cell_changed'] & df['prev_cell'].notna()
        
        handovers = df[df['handover']].copy()
        
        if len(handovers) > 0:
            handovers['from_cell'] = handovers['prev_cell']
            handovers['to_cell'] = handovers['cell_id']
            handovers['handover_quality'] = handovers.apply(self.calculate_handover_quality, axis=1)
        
        return handovers
    
    def calculate_handover_quality(self, row):
        rsrp = row['rsrp']
        sinr = row['sinr']
        quality_score = 0
        
        if rsrp >= -80: quality_score += 50
        elif rsrp >= -90: quality_score += 35
        elif rsrp >= -100: quality_score += 20
        else: quality_score += 5
        
        if sinr >= 20: quality_score += 50
        elif sinr >= 13: quality_score += 35
        elif sinr >= 5: quality_score += 20
        else: quality_score += 5
        
        if quality_score >= 80: return "Excellent 🟢"
        elif quality_score >= 60: return "Good 🟡"
        elif quality_score >= 40: return "Fair 🟠"
        else: return "Poor 🔴"
    
    def get_handover_statistics(self, handovers):
        if handovers is None or len(handovers) == 0:
            return None
        
        return {
            "total_handovers": len(handovers),
            "unique_cells": len(handovers['cell_id'].unique()),
            "avg_rsrp": handovers['rsrp'].mean(),
            "avg_sinr": handovers['sinr'].mean(),
            "avg_latency": handovers['latency_ms'].mean(),
            "quality_distribution": handovers['handover_quality'].value_counts().to_dict(),
        }
    
    def get_handover_pairs(self, handovers):
        if handovers is None or len(handovers) == 0:
            return None
        
        pairs = handovers.groupby(['from_cell', 'to_cell']).agg(
            count=('from_cell', 'size'),
            avg_rsrp=('rsrp', 'mean'),
            avg_sinr=('sinr', 'mean'),
            avg_latency=('latency_ms', 'mean'),
            quality=('handover_quality', lambda x: x.value_counts().index[0] if len(x) > 0 else 'Unknown')
        ).reset_index()
        
        return pairs
    
    # ==================== TIME-SERIES FORECASTING ====================
    def prepare_time_series(self, column, freq='5min'):
        df = self.data[['timestamp', column]].copy()
        df = df.sort_values('timestamp')
        df.set_index('timestamp', inplace=True)
        df = df.resample(freq).mean()
        df = df.dropna()
        return df
    
    def forecast_simple(self, data, steps=5):
        if len(data) < 3:
            return None, None
        
        forecast = []
        confidence = []
        last_values = data[-3:].tolist()
        
        for i in range(steps):
            if len(last_values) >= 3:
                forecast_value = (last_values[-1] * 0.5 + last_values[-2] * 0.3 + last_values[-3] * 0.2)
            elif len(last_values) == 2:
                forecast_value = (last_values[-1] * 0.6 + last_values[-2] * 0.4)
            else:
                forecast_value = last_values[-1] if last_values else 0
            
            forecast.append(round(forecast_value, 1))
            std = data.std() if len(data) > 1 else 2
            confidence.append((round(forecast_value - std, 1), round(forecast_value + std, 1)))
            last_values.append(forecast_value)
            if len(last_values) > 3:
                last_values.pop(0)
        
        return forecast, confidence
    
    def get_forecast(self, column, steps=5, freq='5min'):
        try:
            ts_data = self.prepare_time_series(column, freq)
            if len(ts_data) < 3:
                return None, None, None
            
            forecast, confidence = self.forecast_simple(ts_data[column].values, steps)
            if forecast is None:
                return None, None, None
            
            last_date = ts_data.index[-1]
            future_dates = [last_date + pd.Timedelta(minutes=5 * (i + 1)) for i in range(steps)]
            return future_dates, forecast, confidence
        except Exception as e:
            print(f"Forecast error: {e}")
            return None, None, None
    
    def get_trend_analysis(self, column):
        try:
            ts_data = self.prepare_time_series(column, freq='5min')
            if len(ts_data) < 5:
                return None
            
            x = list(range(len(ts_data)))
            y = ts_data[column].values
            n = len(x)
            sum_x = sum(x)
            sum_y = sum(y)
            sum_xy = sum([x[i] * y[i] for i in range(n)])
            sum_x2 = sum([x[i] ** 2 for i in range(n)])
            
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2) if (n * sum_x2 - sum_x**2) != 0 else 0
            
            if slope > 1: trend = "↑ Increasing"
            elif slope < -1: trend = "↓ Decreasing"
            else: trend = "→ Stable"
            
            return {
                "slope": round(slope, 2),
                "trend": trend,
                "data_points": n,
                "first_value": y[0],
                "last_value": y[-1],
                "change": round(y[-1] - y[0], 1)
            }
        except Exception as e:
            print(f"Trend analysis error: {e}")
            return None
    
    # ==================== ANOMALY DETECTION ====================
    def detect_anomalies_iqr(self, column, multiplier=1.5):
        Q1 = self.data[column].quantile(0.25)
        Q3 = self.data[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - multiplier * IQR
        upper_bound = Q3 + multiplier * IQR
        anomalies = self.data[(self.data[column] < lower_bound) | (self.data[column] > upper_bound)]
        return anomalies, lower_bound, upper_bound
    
    def detect_anomalies_zscore(self, column, threshold=2.5):
        mean = self.data[column].mean()
        std = self.data[column].std()
        if std == 0:
            return pd.DataFrame(), 0, 0
        self.data[f'{column}_zscore'] = (self.data[column] - mean) / std
        anomalies = self.data[abs(self.data[f'{column}_zscore']) > threshold]
        return anomalies, mean, std
    
    def detect_all_anomalies(self, columns=None):
        if columns is None:
            columns = ['rsrp', 'sinr', 'download_mbps', 'upload_mbps', 'latency_ms']
        all_anomalies = pd.DataFrame()
        anomaly_counts = {}
        
        for col in columns:
            anomalies, _, _ = self.detect_anomalies_iqr(col)
            anomaly_counts[col] = len(anomalies)
            if len(anomalies) > 0:
                anomalies['anomaly_column'] = col
                all_anomalies = pd.concat([all_anomalies, anomalies])
        
        if len(all_anomalies) > 0:
            all_anomalies = all_anomalies.drop_duplicates(subset=['timestamp', 'cell_id'])
        
        return all_anomalies, anomaly_counts
    
    def get_anomaly_score(self, row, columns=None):
        if columns is None:
            columns = ['rsrp', 'sinr', 'download_mbps', 'upload_mbps', 'latency_ms']
        
        score = 0
        for col in columns:
            mean = self.data[col].mean()
            std = self.data[col].std()
            if std > 0:
                zscore = abs((row[col] - mean) / std)
                if zscore > 2:
                    score += zscore
        return round(score, 1)
    
    def add_anomaly_score(self):
        self.data['anomaly_score'] = self.data.apply(self.get_anomaly_score, axis=1)
        self.data['is_anomaly'] = self.data['anomaly_score'] > 5
        return self.data
    
    def get_anomaly_statistics(self):
        if 'anomaly_score' not in self.data.columns:
            self.add_anomaly_score()
        
        anomalies = self.data[self.data['is_anomaly']]
        return {
            "total_anomalies": len(anomalies),
            "avg_anomaly_score": self.data['anomaly_score'].mean(),
            "max_anomaly_score": self.data['anomaly_score'].max(),
            "anomaly_percentage": round((len(anomalies) / len(self.data)) * 100, 1) if len(self.data) > 0 else 0,
            "anomaly_cells": anomalies['cell_id'].unique().tolist() if len(anomalies) > 0 else []
        }
    
    # ==================== ROOT CAUSE ANALYSIS ====================
    def analyze_root_cause(self, row):
        causes = []
        recommendations = []
        severity = "Low"
        
        if row['rsrp'] < -100:
            causes.append("📡 Weak Signal (RSRP < -100 dBm)")
            recommendations.append("Check coverage area / Consider adding a repeater")
            severity = "High"
        elif row['rsrp'] < -90:
            causes.append("📡 Fair Signal (RSRP between -100 and -90 dBm)")
            recommendations.append("Improve antenna placement / Check for obstacles")
            if severity != "High": severity = "Medium"
        
        if row['sinr'] < 5:
            causes.append("📶 Poor Signal Quality (SINR < 5 dB)")
            recommendations.append("Check for interference / Change frequency")
            severity = "High"
        elif row['sinr'] < 10:
            causes.append("📶 Fair Signal Quality (SINR between 5 and 10 dB)")
            recommendations.append("Monitor interference levels")
            if severity != "High": severity = "Medium"
        
        if row['latency_ms'] > 150:
            causes.append("⏱️ High Latency (> 150 ms)")
            recommendations.append("Check backhaul / Reduce network load")
            if severity != "High": severity = "High"
        elif row['latency_ms'] > 100:
            causes.append("⏱️ Medium Latency (100-150 ms)")
            recommendations.append("Monitor latency trends")
            if severity != "High" and severity != "Medium": severity = "Medium"
        
        if row['download_mbps'] < 10:
            causes.append("⬇️ Low Download Speed (< 10 Mbps)")
            recommendations.append("Check capacity / Increase bandwidth")
            if severity != "High": severity = "High"
        elif row['download_mbps'] < 25:
            causes.append("⬇️ Medium Download Speed (10-25 Mbps)")
            recommendations.append("Monitor speed trends")
            if severity == "Low": severity = "Medium"
        
        if row['upload_mbps'] < 3:
            causes.append("⬆️ Low Upload Speed (< 3 Mbps)")
            recommendations.append("Check uplink capacity")
            if severity != "High": severity = "Medium"
        
        return {
            "causes": causes,
            "recommendations": recommendations,
            "severity": severity,
            "has_problem": len(causes) > 0
        }
    
    def add_root_cause_analysis(self):
        if 'problem' not in self.data.columns:
            return self.data
        
        problem_rows = self.data[self.data['problem']].copy()
        
        if len(problem_rows) > 0:
            results = problem_rows.apply(self.analyze_root_cause, axis=1)
            self.data['root_causes'] = None
            self.data['recommendations'] = None
            self.data['severity'] = None
            
            for idx, result in results.items():
                self.data.at[idx, 'root_causes'] = ', '.join(result['causes']) if result['causes'] else 'No issues'
                self.data.at[idx, 'recommendations'] = ', '.join(result['recommendations']) if result['recommendations'] else 'Monitor only'
                self.data.at[idx, 'severity'] = result['severity']
        
        return self.data
    
    def get_root_cause_statistics(self):
        if 'root_causes' not in self.data.columns:
            self.add_root_cause_analysis()
        
        problem_data = self.data[self.data['problem']]
        if len(problem_data) == 0:
            return None
        
        severity_counts = problem_data['severity'].value_counts().to_dict()
        all_causes = []
        for causes in problem_data['root_causes'].dropna():
            all_causes.extend(causes.split(', '))
        cause_counts = pd.Series(all_causes).value_counts().to_dict()
        
        return {
            "total_problems": len(problem_data),
            "severity_counts": severity_counts,
            "cause_counts": cause_counts,
            "critical_cells": problem_data[problem_data['severity'] == 'High']['cell_id'].unique().tolist(),
            "top_cause": max(cause_counts, key=cause_counts.get) if cause_counts else "No causes"
        }
    
    def get_cell_root_causes(self, cell_id):
        if 'root_causes' not in self.data.columns:
            self.add_root_cause_analysis()
        
        cell_data = self.data[(self.data['cell_id'] == cell_id) & (self.data['problem'] == True)]
        if len(cell_data) == 0:
            return None
        
        results = {
            "cell_id": cell_id,
            "total_problems": len(cell_data),
            "severity_counts": cell_data['severity'].value_counts().to_dict(),
            "common_causes": {},
            "recommendations": []
        }
        
        all_causes = []
        all_recommendations = []
        for _, row in cell_data.iterrows():
            if pd.notna(row['root_causes']):
                all_causes.extend(row['root_causes'].split(', '))
            if pd.notna(row['recommendations']):
                all_recommendations.extend(row['recommendations'].split(', '))
        
        results["common_causes"] = pd.Series(all_causes).value_counts().head(3).to_dict() if all_causes else {}
        results["recommendations"] = list(set(all_recommendations))[:3] if all_recommendations else []
        return results
    
    # ==================== ML PREDICTION ====================
    def prepare_ml_data(self):
        if 'problem' not in self.data.columns:
            return None, None
        
        features = ['rsrp', 'rsrq', 'sinr', 'download_mbps', 'upload_mbps', 'latency_ms']
        for col in features:
            if col not in self.data.columns:
                return None, None
        X = self.data[features].copy()
        y = self.data['problem'].copy()
        X = X.fillna(X.mean())
        return X, y
    
    def train_ml_model(self):
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score
        
        X, y = self.prepare_ml_data()
        if X is None or len(X) < 5:
            return None, None, None
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.3, random_state=42, stratify=y
            )
        except ValueError:
            X_train, X_test, y_train, y_test = train_test_split(
                            X, y, test_size=0.3, random_state=42
                        )

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        feature_importance = dict(zip(X.columns, model.feature_importances_.round(3)))
        
        return {
            "model": model,
            "accuracy": round(accuracy * 100, 1),
            "feature_importance": feature_importance,
            "X_train": X_train,
            "X_test": X_test,
            "y_train": y_train,
            "y_test": y_test,
            "y_pred": y_pred,
            "features": X.columns.tolist(),
            "n_samples": len(X)
        }
    
    def predict_problem(self, row, model):
        if model is None:
            return None, None
        
        features = ['rsrp', 'rsrq', 'sinr', 'download_mbps', 'upload_mbps', 'latency_ms']
        try:
            X = pd.DataFrame([[row[col] for col in features]], columns=features)
            X = X.fillna(X.mean())
            prediction = model.predict(X)[0]
            probability = model.predict_proba(X)[0]
            confidence = round(max(probability) * 100, 1)
            
            return {
                "prediction": "⚠️ Problem" if prediction else "✅ Healthy",
                "confidence": confidence,
                "probability": probability.tolist()
            }
        except Exception as e:
            print(f"Prediction error: {e}")
            return None, None
    
    def predict_all_problems(self, model):
        if model is None:
            return None
        
        features = ['rsrp', 'rsrq', 'sinr', 'download_mbps', 'upload_mbps', 'latency_ms']
        try:
            X = self.data[features].copy()
            X = X.fillna(X.mean())
            predictions = model.predict(X)
            probabilities = model.predict_proba(X)
            
            self.data['ml_prediction'] = predictions
            self.data['ml_confidence'] = [round(max(p) * 100, 1) for p in probabilities]
            self.data['ml_result'] = self.data['ml_prediction'].apply(
                lambda x: "⚠️ Problem" if x else "✅ Healthy"
            )
            return self.data
        except Exception as e:
            print(f"Prediction error: {e}")
            return None
    
    def get_ml_statistics(self, model, X, y):
        if model is None:
            return None
        
        from sklearn.metrics import classification_report
        try:
            y_pred = model.predict(X)
            report = classification_report(y, y_pred, output_dict=True, zero_division=0)
            
            return {
                "accuracy": round(report['accuracy'] * 100, 1) if 'accuracy' in report else 0,
                "precision": round(report['weighted avg']['precision'] * 100, 1),
                "recall": round(report['weighted avg']['recall'] * 100, 1),
                "f1_score": round(report['weighted avg']['f1-score'] * 100, 1)
            }
        except Exception as e:
            print(f"Statistics error: {e}")
            return None
    
    # ==================== PDF REPORT ====================
    def generate_pdf_report(self, filename="network_report.pdf"):
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas
            from datetime import datetime
            import io
            
            buffer = io.BytesIO()
            c = canvas.Canvas(buffer, pagesize=A4)
            width, height = A4
            
            c.setFont("Helvetica-Bold", 28)
            c.drawString(50, height - 50, "📡 Telecom Network Report")
            c.setFont("Helvetica", 12)
            c.drawString(50, height - 80, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            c.line(50, height - 95, width - 50, height - 95)
            
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, height - 130, "📊 Network Summary")
            c.setFont("Helvetica", 12)
            y = height - 160
            
            stats = self.get_stats()
            health = self.health_score()
            ux_stats = self.get_ux_statistics() if hasattr(self, 'get_ux_statistics') else None
            
            summary_lines = [
                f"Health Score: {health}/100",
                f"Total Samples: {stats['total_samples']}",
                f"Problems Detected: {stats['problems']}",
                f"Average RSRP: {stats['avg_rsrp']:.1f} dBm",
                f"Average SINR: {stats['avg_sinr']:.1f} dB",
                f"Download Speed: {stats['avg_download']:.1f} Mbps",
                f"Upload Speed: {stats['avg_upload']:.1f} Mbps",
                f"Latency: {stats['avg_latency']:.1f} ms",
            ]
            if ux_stats:
                summary_lines.append(f"Average UX Score: {ux_stats['avg_ux']:.1f}/100")
            
            for line in summary_lines:
                c.drawString(50, y, line)
                y -= 25
            
            c.showPage()
            
            # صفحة 2: تحليل الإشارة
            c.setFont("Helvetica-Bold", 20)
            c.drawString(50, height - 50, "📶 Signal Analysis")
            c.setFont("Helvetica", 12)
            y = height - 90
            
            signal_dist = self.data['signal_quality'].value_counts()
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y, "Signal Quality Distribution")
            y -= 25
            c.setFont("Helvetica", 12)
            for quality, count in signal_dist.items():
                percentage = (count / len(self.data)) * 100
                c.drawString(70, y, f"{quality}: {count} ({percentage:.1f}%)")
                y -= 20
            y -= 15
            
            sinr_dist = self.data['sinr_quality'].value_counts()
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y, "SINR Quality Distribution")
            y -= 25
            c.setFont("Helvetica", 12)
            for quality, count in sinr_dist.items():
                percentage = (count / len(self.data)) * 100
                c.drawString(70, y, f"{quality}: {count} ({percentage:.1f}%)")
                y -= 20
            
            c.showPage()
            
            # صفحة 3: الخلايا
            c.setFont("Helvetica-Bold", 20)
            c.drawString(50, height - 50, "📋 Cell Performance & Problems")
            c.setFont("Helvetica", 12)
            y = height - 90
            
            cell_stats = self.data.groupby('cell_id').agg(
                samples=('cell_id', 'count'),
                avg_rsrp=('rsrp', 'mean'),
                avg_sinr=('sinr', 'mean'),
                avg_download=('download_mbps', 'mean'),
                problems=('problem', 'sum')
            ).reset_index()
            
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y, "Cell Statistics")
            y -= 25
            c.setFont("Helvetica", 10)
            for _, row in cell_stats.iterrows():
                line = f"Cell {row['cell_id']}: {row['samples']} samples, RSRP: {row['avg_rsrp']:.1f} dBm, SINR: {row['avg_sinr']:.1f} dB, Problems: {row['problems']}"
                c.drawString(50, y, line)
                y -= 18
                if y < 50:
                    c.showPage()
                    y = height - 50
            
            c.showPage()
            
            # صفحة 4: التوصيات
            c.setFont("Helvetica-Bold", 20)
            c.drawString(50, height - 50, "💡 Recommendations")
            c.setFont("Helvetica", 12)
            y = height - 90
            
            recommendations = []
            if stats['avg_rsrp'] < -100:
                recommendations.append("🔴 Weak signal detected. Consider adding repeaters or improving coverage.")
            elif stats['avg_rsrp'] < -90:
                recommendations.append("🟡 Signal strength is fair. Monitor for potential issues.")
            
            if stats['avg_sinr'] < 5:
                recommendations.append("🔴 Poor signal quality detected. Check for interference sources.")
            elif stats['avg_sinr'] < 10:
                recommendations.append("🟡 Signal quality is fair. Monitor interference levels.")
            
            if stats['avg_latency'] > 100:
                recommendations.append("🔴 High latency detected. Check backhaul and network load.")
            elif stats['avg_latency'] > 50:
                recommendations.append("🟡 Latency is moderate. Monitor trends.")
            
            if stats['avg_download'] < 10:
                recommendations.append("🔴 Low download speeds detected. Check capacity and bandwidth.")
            elif stats['avg_download'] < 25:
                recommendations.append("🟡 Download speeds are moderate. Monitor for congestion.")
            
            if stats['problems'] > 0:
                recommendations.append(f"⚠️ {stats['problems']} problem samples detected. Investigate affected cells.")
            
            if not recommendations:
                recommendations.append("✅ Network performance looks good. Continue monitoring.")
            
            for rec in recommendations:
                c.drawString(50, y, rec)
                y -= 25
                if y < 50:
                    c.showPage()
                    y = height - 50
            
            c.showPage()
            c.setFont("Helvetica", 10)
            c.drawString(50, 50, "Generated by Telecom Network Analyzer")
            c.drawString(50, 35, "© 2026 - All Rights Reserved")
            c.save()
            
            return buffer.getvalue()
        except ImportError:
            print("ReportLab not installed. Run: pip install reportlab")
            return None
        except Exception as e:
            print(f"PDF generation error: {e}")
            return None
    
    # ==================== COVERAGE GAPS ====================
    def detect_coverage_gaps(self, rsrp_threshold=-100, sinr_threshold=5):
        gaps = []
        weak_signal = self.data[self.data['rsrp'] < rsrp_threshold]
        poor_quality = self.data[self.data['sinr'] < sinr_threshold]
        no_coverage = self.data[self.data['rsrp'] < -120]
        
        if len(weak_signal) > 0:
            gaps.append({
                "type": "Weak Signal",
                "count": len(weak_signal),
                "percentage": round((len(weak_signal) / len(self.data)) * 100, 1),
                "cells": weak_signal['cell_id'].unique().tolist(),
                "avg_rsrp": weak_signal['rsrp'].mean()
            })
        
        if len(poor_quality) > 0:
            gaps.append({
                "type": "Poor Quality",
                "count": len(poor_quality),
                "percentage": round((len(poor_quality) / len(self.data)) * 100, 1),
                "cells": poor_quality['cell_id'].unique().tolist(),
                "avg_sinr": poor_quality['sinr'].mean()
            })
        
        if len(no_coverage) > 0:
            gaps.append({
                "type": "No Coverage",
                "count": len(no_coverage),
                "percentage": round((len(no_coverage) / len(self.data)) * 100, 1),
                "cells": no_coverage['cell_id'].unique().tolist(),
                "avg_rsrp": no_coverage['rsrp'].mean()
            })
        
        return gaps
    
    def get_coverage_gap_statistics(self, gaps):
        if not gaps:
            return None
        total_gaps = sum(gap['count'] for gap in gaps)
        return {
            "total_gaps": total_gaps,
            "gap_types": [gap['type'] for gap in gaps],
            "gap_counts": {gap['type']: gap['count'] for gap in gaps},
            "gap_percentages": {gap['type']: gap['percentage'] for gap in gaps},
            "affected_cells": list(set().union(*[set(gap['cells']) for gap in gaps])),
            "has_gaps": total_gaps > 0
        }
    
    def get_coverage_recommendations(self, gaps):
        recommendations = []
        if not gaps:
            return ["✅ No coverage gaps detected. Network coverage looks good."]
        
        for gap in gaps:
            if gap['type'] == "Weak Signal":
                recommendations.append(f"🟡 {gap['type']}: {gap['count']} samples ({gap['percentage']}%) - Consider adding repeaters or small cells in affected areas.")
            elif gap['type'] == "Poor Quality":
                recommendations.append(f"🟠 {gap['type']}: {gap['count']} samples ({gap['percentage']}%) - Check for interference sources or adjust frequency planning.")
            elif gap['type'] == "No Coverage":
                recommendations.append(f"🔴 {gap['type']}: {gap['count']} samples ({gap['percentage']}%) - New site required or major coverage expansion needed.")
        
        if len(gaps) >= 2:
            recommendations.append("⚠️ Multiple coverage issues detected. Consider comprehensive network audit.")
        return recommendations
    
    # ==================== الفكرة 11: CAPACITY PLANNING ====================
    def analyze_capacity(self):
        """تحليل سعة الشبكة"""
        total_samples = len(self.data)
        if total_samples == 0:
            return None
        
        # تحليل التحميل لكل خلية
        cell_load = self.data.groupby('cell_id').agg(
            samples=('cell_id', 'count'),
            avg_download=('download_mbps', 'mean'),
            avg_upload=('upload_mbps', 'mean'),
            avg_latency=('latency_ms', 'mean'),
            problem_ratio=('problem', lambda x: (x.sum() / len(x)) * 100)
        ).reset_index()
        
        # تحليل أوقات الذروة
        self.data['hour'] = self.data['timestamp'].dt.hour
        hourly_load = self.data.groupby('hour').size()
        peak_hour = hourly_load.idxmax() if len(hourly_load) > 0 else None
        peak_load = hourly_load.max() if len(hourly_load) > 0 else 0
        
        # تحليل استخدام السعة
        capacity_analysis = []
        for _, row in cell_load.iterrows():
            status = "✅ Normal"
            if row['problem_ratio'] > 30:
                status = "🔴 Critical"
            elif row['problem_ratio'] > 15:
                status = "🟡 Warning"
            
            capacity_analysis.append({
                "cell_id": row['cell_id'],
                "samples": row['samples'],
                "avg_download": row['avg_download'],
                "avg_upload": row['avg_upload'],
                "avg_latency": row['avg_latency'],
                "problem_ratio": round(row['problem_ratio'], 1),
                "status": status
            })
        
        return {
            "total_samples": total_samples,
            "peak_hour": peak_hour,
            "peak_load": peak_load,
            "cell_analysis": capacity_analysis,
            "avg_download_all": self.data['download_mbps'].mean(),
            "avg_upload_all": self.data['upload_mbps'].mean(),
            "avg_latency_all": self.data['latency_ms'].mean()
        }
    
    def get_capacity_recommendations(self, capacity_data):
        """توصيات لتحسين السعة"""
        if not capacity_data:
            return ["No capacity data available"]
        
        recommendations = []
        
        for cell in capacity_data['cell_analysis']:
            if cell['status'] == "🔴 Critical":
                recommendations.append(f"🔴 Cell {cell['cell_id']}: Critical load ({cell['problem_ratio']}% problems). Consider capacity upgrade or load balancing.")
            elif cell['status'] == "🟡 Warning":
                recommendations.append(f"🟡 Cell {cell['cell_id']}: High load ({cell['problem_ratio']}% problems). Monitor and plan for expansion.")
        
        if capacity_data['peak_hour'] is not None:
            recommendations.append(f"📊 Peak hour: {capacity_data['peak_hour']:02d}:00 with {capacity_data['peak_load']} samples. Consider additional resources during peak times.")
        
        if not recommendations:
            recommendations.append("✅ Network capacity looks balanced. Continue monitoring.")
        
        return recommendations
    
    # ==================== الفكرة 12: REAL-TIME DASHBOARD ====================
    def get_realtime_stats(self):
        """إحصائيات لحظية للـ Real-time Dashboard"""
        total_samples = len(self.data)
        if total_samples == 0:
            return None
        
        # آخر 10 قياسات
        latest_data = self.data.sort_values('timestamp', ascending=False).head(10)
        
        # آخر 5 دقائق
        last_5min = self.data[self.data['timestamp'] >= (self.data['timestamp'].max() - pd.Timedelta(minutes=5))]
        
        return {
            "total_samples": total_samples,
            "latest_measurements": latest_data[['timestamp', 'cell_id', 'rsrp', 'sinr', 'download_mbps', 'latency_ms']].to_dict('records'),
            "last_5min_samples": len(last_5min),
            "current_health": self.health_score(),
            "current_problems": self.data['problem'].sum(),
            "latest_timestamp": self.data['timestamp'].max() if total_samples > 0 else None,
            "avg_rsrp_5min": last_5min['rsrp'].mean() if len(last_5min) > 0 else None,
            "avg_sinr_5min": last_5min['sinr'].mean() if len(last_5min) > 0 else None,
            "avg_download_5min": last_5min['download_mbps'].mean() if len(last_5min) > 0 else None,
            "avg_latency_5min": last_5min['latency_ms'].mean() if len(last_5min) > 0 else None
        }
    
    def get_cells_status(self):
        """حالة كل خلية للـ Real-time Dashboard"""
        cell_status = []
        
        for cell_id in self.data['cell_id'].unique():
            cell_data = self.data[self.data['cell_id'] == cell_id]
            latest = cell_data.sort_values('timestamp', ascending=False).head(1)
            
            if len(latest) > 0:
                row = latest.iloc[0]
                status = "🟢 Excellent"
                if row['rsrp'] < -100 or row['sinr'] < 5:
                    status = "🔴 Critical"
                elif row['rsrp'] < -90 or row['sinr'] < 10:
                    status = "🟡 Warning"
                
                cell_status.append({
                    "cell_id": cell_id,
                    "rsrp": row['rsrp'],
                    "sinr": row['sinr'],
                    "download": row['download_mbps'],
                    "latency": row['latency_ms'],
                    "status": status,
                    "last_update": row['timestamp']
                })
        
        return cell_status
# ==================== EXPORT TO EXCEL ====================
def export_to_excel(self, filename="network_report.xlsx"):
    """تصدير البيانات إلى Excel مع Sheets متعددة"""
    try:
        import pandas as pd
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill, Alignment
        import io
        
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Sheet 1: Summary
            summary_data = {
                'Metric': ['Health Score', 'Total Samples', 'Problems', 'Avg RSRP', 'Avg SINR', 
                          'Avg Download', 'Avg Upload', 'Avg Latency'],
                'Value': [
                    self.health_score(),
                    len(self.data),
                    self.data['problem'].sum(),
                    round(self.data['rsrp'].mean(), 2),
                    round(self.data['sinr'].mean(), 2),
                    round(self.data['download_mbps'].mean(), 2),
                    round(self.data['upload_mbps'].mean(), 2),
                    round(self.data['latency_ms'].mean(), 2)
                ]
            }
            pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
            
            # Sheet 2: All Data
            self.data.to_excel(writer, sheet_name='All Data', index=False)
            
            # Sheet 3: Cell Statistics
            cell_stats = self.data.groupby('cell_id').agg(
                samples=('cell_id', 'count'),
                avg_rsrp=('rsrp', 'mean'),
                avg_sinr=('sinr', 'mean'),
                avg_download=('download_mbps', 'mean'),
                problems=('problem', 'sum')
            ).reset_index()
            cell_stats.to_excel(writer, sheet_name='Cell Stats', index=False)
            
            # Sheet 4: Problems
            if self.data['problem'].sum() > 0:
                self.data[self.data['problem']].to_excel(writer, sheet_name='Problems', index=False)
            
            # Sheet 5: UX Score Distribution
            if 'ux_category' in self.data.columns:
                ux_dist = self.data['ux_category'].value_counts().reset_index()
                ux_dist.columns = ['Category', 'Count']
                ux_dist.to_excel(writer, sheet_name='UX Distribution', index=False)
        
        output.seek(0)
        return output.getvalue()
        
    except Exception as e:
        print(f"Export error: {e}")
        return None
# ==================== DATA COMPARISON ====================
def compare_periods(self, period1_start, period1_end, period2_start, period2_end):
    """مقارنة بين فترتين زمنيتين"""
    # فلترة البيانات
    period1 = self.data[
        (self.data['timestamp'] >= period1_start) &
        (self.data['timestamp'] <= period1_end)
    ]
    period2 = self.data[
        (self.data['timestamp'] >= period2_start) &
        (self.data['timestamp'] <= period2_end)
    ]
    
    if len(period1) == 0 or len(period2) == 0:
        return None
    
    # حساب الإحصائيات
    stats1 = {
        "count": len(period1),
        "avg_rsrp": period1['rsrp'].mean(),
        "avg_sinr": period1['sinr'].mean(),
        "avg_download": period1['download_mbps'].mean(),
        "avg_latency": period1['latency_ms'].mean(),
        "problems": period1['problem'].sum()
    }
    
    stats2 = {
        "count": len(period2),
        "avg_rsrp": period2['rsrp'].mean(),
        "avg_sinr": period2['sinr'].mean(),
        "avg_download": period2['download_mbps'].mean(),
        "avg_latency": period2['latency_ms'].mean(),
        "problems": period2['problem'].sum()
    }
    
    # حساب الفروقات
    diff = {
        "rsrp": stats2['avg_rsrp'] - stats1['avg_rsrp'],
        "sinr": stats2['avg_sinr'] - stats1['avg_sinr'],
        "download": stats2['avg_download'] - stats1['avg_download'],
        "latency": stats2['avg_latency'] - stats1['avg_latency'],
        "problems": stats2['problems'] - stats1['problems']
    }
    
    return {
        "period1": stats1,
        "period2": stats2,
        "difference": diff,
        "period1_data": period1,
        "period2_data": period2
    }

def compare_cells(self, cell1, cell2):
    """مقارنة بين خليتين"""
    cell1_data = self.data[self.data['cell_id'] == cell1]
    cell2_data = self.data[self.data['cell_id'] == cell2]
    
    if len(cell1_data) == 0 or len(cell2_data) == 0:
        return None
    
    stats1 = {
        "count": len(cell1_data),
        "avg_rsrp": cell1_data['rsrp'].mean(),
        "avg_sinr": cell1_data['sinr'].mean(),
        "avg_download": cell1_data['download_mbps'].mean(),
        "avg_latency": cell1_data['latency_ms'].mean(),
        "problems": cell1_data['problem'].sum()
    }
    
    stats2 = {
        "count": len(cell2_data),
        "avg_rsrp": cell2_data['rsrp'].mean(),
        "avg_sinr": cell2_data['sinr'].mean(),
        "avg_download": cell2_data['download_mbps'].mean(),
        "avg_latency": cell2_data['latency_ms'].mean(),
        "problems": cell2_data['problem'].sum()
    }
    
    diff = {
        "rsrp": stats2['avg_rsrp'] - stats1['avg_rsrp'],
        "sinr": stats2['avg_sinr'] - stats1['avg_sinr'],
        "download": stats2['avg_download'] - stats1['avg_download'],
        "latency": stats2['avg_latency'] - stats1['avg_latency'],
        "problems": stats2['problems'] - stats1['problems']
    }
    
    return {
        "cell1": cell1,
        "cell2": cell2,
        "stats1": stats1,
        "stats2": stats2,
        "difference": diff,
        "cell1_data": cell1_data,
        "cell2_data": cell2_data
    }
# ==================== NETWORK SIMULATION ====================
def simulate_improvement(self, improvement_type, value):
    """محاكاة تحسين في الشبكة"""
    simulated_data = self.data.copy()
    
    if improvement_type == "Improve RSRP":
        # تحسين RSRP بـ X dB
        simulated_data['rsrp'] = simulated_data['rsrp'] + value
    
    elif improvement_type == "Improve SINR":
        # تحسين SINR بـ X dB
        simulated_data['sinr'] = simulated_data['sinr'] + value
    
    elif improvement_type == "Reduce Latency":
        # تقليل الـ Latency
        simulated_data['latency_ms'] = simulated_data['latency_ms'] - value
        simulated_data['latency_ms'] = simulated_data['latency_ms'].clip(lower=0)
    
    elif improvement_type == "Increase Bandwidth":
        # زيادة السرعة
        simulated_data['download_mbps'] = simulated_data['download_mbps'] * (1 + value/100)
        simulated_data['upload_mbps'] = simulated_data['upload_mbps'] * (1 + value/100)
    
    elif improvement_type == "Add New Cell":
        # إضافة خلية جديدة تحسن التغطية
        simulated_data['rsrp'] = simulated_data['rsrp'] + value
        simulated_data['sinr'] = simulated_data['sinr'] + value/2
    
    # إعادة حساب المشاكل
    simulated_data['problem'] = (
        (simulated_data['rsrp'] < -100) |
        (simulated_data['sinr'] < 5) |
        (simulated_data['latency_ms'] > 100) |
        (simulated_data['download_mbps'] < 10)
    )
    
    return simulated_data

def get_simulation_impact(self, original_data, simulated_data):
    """تحليل تأثير المحاكاة"""
    original_problems = original_data['problem'].sum()
    simulated_problems = simulated_data['problem'].sum()
    
    return {
        "original_problems": original_problems,
        "simulated_problems": simulated_problems,
        "problems_reduced": original_problems - simulated_problems,
        "reduction_percentage": round(((original_problems - simulated_problems) / max(original_problems, 1)) * 100, 1),
        "avg_rsrp_improvement": round(simulated_data['rsrp'].mean() - original_data['rsrp'].mean(), 2),
        "avg_sinr_improvement": round(simulated_data['sinr'].mean() - original_data['sinr'].mean(), 2),
        "avg_latency_improvement": round(original_data['latency_ms'].mean() - simulated_data['latency_ms'].mean(), 2)
    }

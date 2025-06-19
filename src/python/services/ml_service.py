import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib
from datetime import datetime, timedelta
import os

class MLService:
    def __init__(self, session):
        self.session = session
        self.model = None
        self.scaler = StandardScaler()
        self.model_path = "models/irrigation_model.pkl"
        self.scaler_path = "models/scaler.pkl"
        
        # Criar diretório de modelos se não existir
        os.makedirs("models", exist_ok=True)
        
        # Tentar carregar modelo existente
        self.load_model()
    
    def prepare_data(self, sensor_data, climate_data):
        """
        Prepara os dados para treinamento do modelo
        """
        # Combinar dados de sensores e clima
        df_sensors = pd.DataFrame(sensor_data)
        df_climate = pd.DataFrame(climate_data)
        
        if df_sensors.empty or df_climate.empty:
            return None
        
        # Converter timestamps
        df_sensors['timestamp'] = pd.to_datetime(df_sensors['timestamp'])
        df_climate['timestamp'] = pd.to_datetime(df_climate['timestamp'])
        
        # Mesclar dados por timestamp (aproximação de 1 hora)
        df_sensors['timestamp_hour'] = df_sensors['timestamp'].dt.floor('H')
        df_climate['timestamp_hour'] = df_climate['timestamp'].dt.floor('H')
        
        merged_df = pd.merge(df_sensors, df_climate, 
                           left_on='timestamp_hour', 
                           right_on='timestamp_hour', 
                           how='inner', suffixes=('_sensor', '_climate'))
        
        if merged_df.empty:
            return None
        
        # Criar features
        features = []
        for _, row in merged_df.iterrows():
            feature_vector = [
                row['soil_moisture'],           # Umidade do solo
                row['soil_ph'],                 # pH do solo
                float(row['phosphorus_present']), # Fósforo (0 ou 1)
                float(row['potassium_present']),  # Potássio (0 ou 1)
                row['temperature'],             # Temperatura
                row['air_humidity'],            # Umidade do ar
                float(row['rain_forecast']),    # Previsão de chuva (0 ou 1)
                row['timestamp_sensor'].hour,   # Hora do dia
                row['timestamp_sensor'].month   # Mês
            ]
            features.append(feature_vector)
        
        # Criar target (decisão de irrigação baseada na lógica atual)
        targets = []
        for _, row in merged_df.iterrows():
            # Aplicar a mesma lógica do ESP32
            irrigate = False
            
            if not row['rain_forecast']:
                if row['soil_moisture'] < 40 and row['phosphorus_present']:
                    irrigate = True
                
                if row['potassium_present'] and row['soil_moisture'] > 60:
                    irrigate = False
                
                if row['soil_moisture'] < 40 and (row['soil_ph'] < 5.5 or row['soil_ph'] > 7.0):
                    irrigate = False
                
                if row['soil_moisture'] > 70:
                    irrigate = False
                
                if (not row['phosphorus_present'] or not row['potassium_present']) and \
                   (row['soil_moisture'] >= 30 and row['soil_moisture'] <= 50):
                    irrigate = True
            
            targets.append(1 if irrigate else 0)
        
        return np.array(features), np.array(targets)
    
    def train_model(self, sensor_data, climate_data):
        """
        Treina o modelo de predição de irrigação
        """
        # Preparar dados
        X, y = self.prepare_data(sensor_data, climate_data)
        
        if X is None or len(X) < 10:
            return {"success": False, "message": "Dados insuficientes para treinamento (mínimo 10 registros)"}
        
        # Dividir dados em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Normalizar features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Criar e treinar modelo
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train_scaled, y_train)
        
        # Avaliar modelo
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Salvar modelo
        self.save_model()
        
        return {
            "success": True,
            "accuracy": accuracy,
            "training_samples": len(X_train),
            "test_samples": len(X_test),
            "classification_report": classification_report(y_test, y_pred)
        }
    
    def predict_irrigation(self, soil_moisture, soil_ph, phosphorus_present, 
                          potassium_present, temperature, air_humidity, 
                          rain_forecast, hour=None, month=None):
        """
        Prediz se deve irrigar baseado nos dados atuais
        """
        if self.model is None:
            return {"success": False, "message": "Modelo não treinado"}
        
        if hour is None:
            hour = datetime.now().hour
        if month is None:
            month = datetime.now().month
        
        # Criar feature vector
        features = np.array([[
            soil_moisture,
            soil_ph,
            float(phosphorus_present),
            float(potassium_present),
            temperature,
            air_humidity,
            float(rain_forecast),
            hour,
            month
        ]])
        
        # Normalizar features
        features_scaled = self.scaler.transform(features)
        
        # Fazer predição
        prediction = self.model.predict(features_scaled)[0]
        probability = self.model.predict_proba(features_scaled)[0]
        
        return {
            "success": True,
            "should_irrigate": bool(prediction),
            "confidence": float(max(probability)),
            "irrigation_probability": float(probability[1]) if len(probability) > 1 else 0.0
        }
    
    def get_feature_importance(self):
        """
        Retorna a importância das features do modelo
        """
        if self.model is None:
            return None
        
        feature_names = [
            'Umidade do Solo', 'pH do Solo', 'Fósforo Presente', 
            'Potássio Presente', 'Temperatura', 'Umidade do Ar',
            'Previsão de Chuva', 'Hora do Dia', 'Mês'
        ]
        
        importance = self.model.feature_importances_
        return dict(zip(feature_names, importance))
    
    def save_model(self):
        """
        Salva o modelo treinado
        """
        if self.model is not None:
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.scaler, self.scaler_path)
    
    def load_model(self):
        """
        Carrega modelo salvo
        """
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
                self.model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
                return True
        except Exception as e:
            print(f"Erro ao carregar modelo: {e}")
        return False
    
    def get_model_status(self):
        """
        Retorna o status atual do modelo
        """
        return {
            "model_loaded": self.model is not None,
            "model_path": self.model_path,
            "scaler_path": self.scaler_path
        } 
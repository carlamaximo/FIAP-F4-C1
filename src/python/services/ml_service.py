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
            print("❌ Dados vazios detectados")
            return None
        
        print(f"📊 Preparando dados: {len(df_sensors)} sensores, {len(df_climate)} clima")
        
        # Converter timestamps
        df_sensors['timestamp'] = pd.to_datetime(df_sensors['timestamp'])
        df_climate['timestamp'] = pd.to_datetime(df_climate['timestamp'])
        
        # Mesclar dados por timestamp (aproximação de 1 hora)
        df_sensors['timestamp_hour'] = df_sensors['timestamp'].dt.floor('h')  # Corrigido: 'H' -> 'h'
        df_climate['timestamp_hour'] = df_climate['timestamp'].dt.floor('h')  # Corrigido: 'H' -> 'h'
        
        print(f"🕐 Timestamps únicos - Sensores: {df_sensors['timestamp_hour'].nunique()}, Clima: {df_climate['timestamp_hour'].nunique()}")
        
        merged_df = pd.merge(df_sensors, df_climate, 
                           left_on='timestamp_hour', 
                           right_on='timestamp_hour', 
                           how='inner', suffixes=('_sensor', '_climate'))
        
        print(f"🔄 Registros combinados: {len(merged_df)}")
        
        if merged_df.empty:
            print("❌ Nenhum registro combinado encontrado")
            # Tentar combinação mais flexível
            return self._prepare_data_flexible(df_sensors, df_climate)
        
        # Criar features
        features = []
        for _, row in merged_df.iterrows():
            try:
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
            except Exception as e:
                print(f"⚠️ Erro ao processar linha: {e}")
                continue
        
        if len(features) < 10:
            print(f"❌ Poucos features válidos: {len(features)}")
            return self._prepare_data_flexible(df_sensors, df_climate)
        
        # Criar target (decisão de irrigação baseada na lógica atual)
        targets = []
        for _, row in merged_df.iterrows():
            try:
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
            except Exception as e:
                print(f"⚠️ Erro ao processar target: {e}")
                targets.append(0)
        
        print(f"✅ Features criados: {len(features)}, Targets: {len(targets)}")
        return np.array(features), np.array(targets)
    
    def _prepare_data_flexible(self, df_sensors, df_climate):
        """
        Método alternativo para combinar dados quando timestamps não coincidem
        """
        print("🔄 Usando método flexível de combinação...")
        
        # Pegar os primeiros registros de cada tipo
        min_records = min(len(df_sensors), len(df_climate), 50)
        
        features = []
        targets = []
        
        for i in range(min_records):
            try:
                sensor_row = df_sensors.iloc[i]
                climate_row = df_climate.iloc[i]
                
                feature_vector = [
                    sensor_row['soil_moisture'],
                    sensor_row['soil_ph'],
                    float(sensor_row['phosphorus_present']),
                    float(sensor_row['potassium_present']),
                    climate_row['temperature'],
                    climate_row['air_humidity'],
                    float(climate_row['rain_forecast']),
                    sensor_row['timestamp'].hour,
                    sensor_row['timestamp'].month
                ]
                features.append(feature_vector)
                
                # Lógica de irrigação
                irrigate = False
                if not climate_row['rain_forecast']:
                    if sensor_row['soil_moisture'] < 40 and sensor_row['phosphorus_present']:
                        irrigate = True
                    if sensor_row['potassium_present'] and sensor_row['soil_moisture'] > 60:
                        irrigate = False
                    if sensor_row['soil_moisture'] < 40 and (sensor_row['soil_ph'] < 5.5 or sensor_row['soil_ph'] > 7.0):
                        irrigate = False
                    if sensor_row['soil_moisture'] > 70:
                        irrigate = False
                    if (not sensor_row['phosphorus_present'] or not sensor_row['potassium_present']) and \
                       (sensor_row['soil_moisture'] >= 30 and sensor_row['soil_moisture'] <= 50):
                        irrigate = True
                
                targets.append(1 if irrigate else 0)
                
            except Exception as e:
                print(f"⚠️ Erro no método flexível: {e}")
                continue
        
        print(f"✅ Método flexível: {len(features)} features criados")
        return np.array(features), np.array(targets)
    
    def train_model(self, sensor_data, climate_data):
        """
        Treina o modelo de predição de irrigação
        """
        # Preparar dados
        X, y = self.prepare_data(sensor_data, climate_data)
        
        if X is None or len(X) < 10:
            return {"success": False, "message": f"Dados insuficientes para treinamento (mínimo 10 registros, obtidos: {len(X) if X is not None else 0})"}
        
        print(f"🎯 Treinando modelo com {len(X)} amostras...")
        
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
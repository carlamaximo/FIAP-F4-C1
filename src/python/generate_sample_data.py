#!/usr/bin/env python3
"""
Script para gerar dados de exemplo para treinar o modelo de Machine Learning
FarmTech Solutions - Fase 4
"""

import random
from datetime import datetime, timedelta
from database.oracle import get_session
from services.climate_service import ClimateService
from services.sensor_service import SensorRecordService

def generate_sample_data():
    """
    Gera dados de exemplo para treinar o modelo de ML
    """
    session = get_session()
    climate_service = ClimateService(session)
    sensor_service = SensorRecordService(session)
    
    print("🌾 Gerando dados de exemplo para FarmTech Solutions - Fase 4")
    print("=" * 60)
    
    # Limpar dados existentes (opcional)
    print("🗑️ Limpando dados existentes...")
    # climate_service.delete_all()  # Descomente se quiser limpar
    # sensor_service.delete_all()   # Descomente se quiser limpar
    
    # Gerar dados para os últimos 30 dias
    start_date = datetime.now() - timedelta(days=30)
    current_date = start_date
    
    print(f"📅 Gerando dados de {start_date.strftime('%d/%m/%Y')} até hoje")
    
    climate_records = 0
    sensor_records = 0
    
    while current_date <= datetime.now():
        # Gerar múltiplas leituras por dia (a cada 4 horas)
        for hour in [6, 10, 14, 18, 22]:
            timestamp = current_date.replace(hour=hour, minute=random.randint(0, 59))
            
            # Dados climáticos realistas
            # Temperatura varia ao longo do dia (mais quente à tarde)
            base_temp = 20
            if hour == 6:  # Manhã
                temperature = base_temp + random.uniform(-2, 5)
            elif hour == 10:  # Meio da manhã
                temperature = base_temp + random.uniform(2, 8)
            elif hour == 14:  # Tarde (mais quente)
                temperature = base_temp + random.uniform(8, 15)
            elif hour == 18:  # Final da tarde
                temperature = base_temp + random.uniform(3, 10)
            else:  # Noite
                temperature = base_temp + random.uniform(-3, 3)
            
            # Umidade do ar (inversamente proporcional à temperatura)
            air_humidity = max(30, min(95, 80 - temperature * 1.5 + random.uniform(-10, 10)))
            
            # Previsão de chuva (mais provável à tarde/noite)
            rain_probability = 0.1
            if hour >= 14:
                rain_probability = 0.3
            rain_forecast = random.random() < rain_probability
            
            # Criar registro climático
            climate_data = {
                "temperature": round(temperature, 1),
                "air_humidity": round(air_humidity, 1),
                "rain_forecast": rain_forecast,
                "timestamp": timestamp
            }
            
            climate_service.create_climate_data(climate_data)
            climate_records += 1
            
            # Dados dos sensores (relacionados aos dados climáticos)
            # Umidade do solo diminui com temperatura alta e sem chuva
            base_moisture = 60
            if temperature > 25:
                base_moisture -= 15
            if rain_forecast:
                base_moisture += 20
            
            soil_moisture = max(10, min(90, base_moisture + random.uniform(-10, 10)))
            
            # pH do solo (relativamente estável)
            soil_ph = 6.0 + random.uniform(-0.5, 0.5)
            
            # Nutrientes (presença varia)
            phosphorus_present = random.random() > 0.3  # 70% de chance de estar presente
            potassium_present = random.random() > 0.2   # 80% de chance de estar presente
            
            # Status de irrigação (baseado na lógica do ESP32)
            irrigate = False
            if not rain_forecast:
                if soil_moisture < 40 and phosphorus_present:
                    irrigate = True
                if potassium_present and soil_moisture > 60:
                    irrigate = False
                if soil_moisture < 40 and (soil_ph < 5.5 or soil_ph > 7.0):
                    irrigate = False
                if soil_moisture > 70:
                    irrigate = False
                if (not phosphorus_present or not potassium_present) and (soil_moisture >= 30 and soil_moisture <= 50):
                    irrigate = True
            
            irrigation_status = "ATIVADA" if irrigate else "DESLIGADA"
            
            # Criar registro de sensor
            sensor_data = {
                "soil_moisture": round(soil_moisture, 1),
                "soil_ph": round(soil_ph, 1),
                "phosphorus_present": phosphorus_present,
                "potassium_present": potassium_present,
                "irrigation_status": irrigation_status,
                "timestamp": timestamp
            }
            
            sensor_service.create_sensor_record(sensor_data)
            sensor_records += 1
        
        current_date += timedelta(days=1)
    
    print(f"✅ Dados gerados com sucesso!")
    print(f"📊 Registros climáticos: {climate_records}")
    print(f"🧪 Registros de sensores: {sensor_records}")
    print(f"📈 Total de registros: {climate_records + sensor_records}")
    print("\n🎯 Agora você pode treinar o modelo de Machine Learning no dashboard!")
    print("🌐 Execute: streamlit run app_dashboard.py")

if __name__ == "__main__":
    generate_sample_data() 
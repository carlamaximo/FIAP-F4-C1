import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

from services.climate_service import ClimateService
from services.component_service import ComponentService
from services.sensor_service import SensorRecordService
from services.application_service import ApplicationService
from services.crops_service import CropService
from services.producer_service import ProducerService
from services.ml_service import MLService

from database.oracle import get_session

session = get_session()

application_service = ApplicationService(session)
component_service = ComponentService(session)
crop_service = CropService(session)
producer_service = ProducerService(session)
sensor_service = SensorRecordService(session)
climate_service = ClimateService(session)
ml_service = MLService(session)


# from weasyprint import HTML


st.set_page_config(page_title="FarmTech Solutions - Fase 4", layout="wide", page_icon="🌾")

# Sidebar com navegação
st.sidebar.title("🌾 FarmTech Solutions")
st.sidebar.markdown("**Fase 4 - Sistema Inteligente**")

aba = st.sidebar.radio(
    "Navegação:", 
    ["🏠 Visão Geral", "🌤️ Dados Climáticos", "🧪 Registros de Sensores", 
     "🤖 Machine Learning", "⚙️ Componentes", "📊 Análises Avançadas"]
)

# ---------------------- VISÃO GERAL --------------------------
if aba == "🏠 Visão Geral":
    st.title("🌾 FarmTech Solutions - Dashboard Inteligente")
    st.markdown("**Fase 4: Sistema de Irrigação com IA e Monitoramento Avançado**")
    
    # Status do modelo ML
    model_status = ml_service.get_model_status()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if model_status["model_loaded"]:
            st.success("🤖 Modelo ML: Ativo")
        else:
            st.warning("🤖 Modelo ML: Não treinado")
    
    with col2:
        st.info("📊 Dados em Tempo Real")
    
    with col3:
        st.info("💧 Sistema de Irrigação")
    
    with col4:
        st.info("🌡️ Monitoramento Climático")
    
    # Dados atuais dos sensores
    sensor_df = pd.DataFrame(sensor_service.list_sensor_records())
    
    if sensor_df.empty:
        st.info("Nenhum dado de sensor disponível para mostrar a situação atual da safra.")
    else:
        sensor_df["timestamp"] = pd.to_datetime(sensor_df["timestamp"])
        latest = sensor_df.sort_values("timestamp", ascending=False).iloc[0]
        
        st.subheader("🌱 Estado Atual da Safra")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            # Gauge chart para umidade
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = latest['soil_moisture'],
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Umidade do Solo (%)"},
                delta = {'reference': 50},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 30], 'color': "lightgray"},
                        {'range': [30, 60], 'color': "yellow"},
                        {'range': [60, 100], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig.update_layout(height=200)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.metric("pH do Solo", f"{latest['soil_ph']:.2f}")
        
        with col3:
            phos = "✅ Presente" if latest["phosphorus_present"] else "❌ Ausente"
            st.metric("Fósforo (P)", phos)
        
        with col4:
            pot = "✅ Presente" if latest["potassium_present"] else "❌ Ausente"
            st.metric("Potássio (K)", pot)
        
        with col5:
            status = latest["irrigation_status"]
            emoji = "💧" if status == "ATIVADA" else "⛔"
            st.metric("Irrigação", f"{emoji} {status}")
        
        # Predição ML se modelo estiver disponível
        if model_status["model_loaded"]:
            st.subheader("🤖 Predição de Irrigação - IA")
            
            # Buscar dados climáticos mais recentes
            climate_df = pd.DataFrame(climate_service.list_climate_data())
            if not climate_df.empty:
                climate_df["timestamp"] = pd.to_datetime(climate_df["timestamp"])
                latest_climate = climate_df.sort_values("timestamp", ascending=False).iloc[0]
                
                prediction = ml_service.predict_irrigation(
                    soil_moisture=latest['soil_moisture'],
                    soil_ph=latest['soil_ph'],
                    phosphorus_present=latest['phosphorus_present'],
                    potassium_present=latest['potassium_present'],
                    temperature=latest_climate['temperature'],
                    air_humidity=latest_climate['air_humidity'],
                    rain_forecast=latest_climate['rain_forecast']
                )
                
                if prediction["success"]:
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        decision = "💧 IRRIGAR" if prediction["should_irrigate"] else "⛔ NÃO IRRIGAR"
                        color = "green" if prediction["should_irrigate"] else "red"
                        st.markdown(f"<h3 style='color: {color}; text-align: center;'>{decision}</h3>", unsafe_allow_html=True)
                    
                    with col2:
                        st.metric("Confiança", f"{prediction['confidence']:.1%}")
                    
                    with col3:
                        st.metric("Prob. Irrigação", f"{prediction['irrigation_probability']:.1%}")

# ---------------------- MACHINE LEARNING --------------------------
elif aba == "🤖 Machine Learning":
    st.title("🤖 Machine Learning - Sistema de Predição")
    st.markdown("**Modelo de IA para Decisões de Irrigação Inteligente**")
    
    # Status do modelo
    model_status = ml_service.get_model_status()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Status do Modelo")
        if model_status["model_loaded"]:
            st.success("✅ Modelo carregado e pronto para uso")
            st.info(f"📁 Modelo salvo em: {model_status['model_path']}")
        else:
            st.warning("⚠️ Modelo não treinado")
            st.info("Treine o modelo com dados históricos para ativar predições")
    
    with col2:
        st.subheader("🎯 Treinar Modelo")
        if st.button("🚀 Treinar Modelo com Dados Históricos"):
            with st.spinner("Treinando modelo..."):
                sensor_data = sensor_service.list_sensor_records()
                climate_data = climate_service.list_climate_data()
                
                result = ml_service.train_model(sensor_data, climate_data)
                
                if result["success"]:
                    st.success("✅ Modelo treinado com sucesso!")
                    st.metric("Acurácia", f"{result['accuracy']:.1%}")
                    st.metric("Amostras de Treino", result['training_samples'])
                    st.metric("Amostras de Teste", result['test_samples'])
                    
                    with st.expander("📋 Relatório de Classificação"):
                        st.text(result['classification_report'])
                else:
                    st.error(f"❌ Erro no treinamento: {result['message']}")
    
    # Feature Importance
    if model_status["model_loaded"]:
        st.subheader("📈 Importância das Features")
        importance = ml_service.get_feature_importance()
        
        if importance:
            # Criar gráfico de barras com Plotly
            fig = px.bar(
                x=list(importance.values()),
                y=list(importance.keys()),
                orientation='h',
                title="Importância das Variáveis no Modelo",
                labels={'x': 'Importância', 'y': 'Variável'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # Simulador de Predição
    st.subheader("🎮 Simulador de Predição")
    st.markdown("Teste diferentes cenários para ver a predição do modelo:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        soil_moisture = st.slider("Umidade do Solo (%)", 0, 100, 45)
        soil_ph = st.slider("pH do Solo", 0.0, 14.0, 6.5)
        phosphorus_present = st.checkbox("Fósforo Presente", value=True)
    
    with col2:
        potassium_present = st.checkbox("Potássio Presente", value=True)
        temperature = st.slider("Temperatura (°C)", -10, 50, 25)
        air_humidity = st.slider("Umidade do Ar (%)", 0, 100, 60)
    
    with col3:
        rain_forecast = st.checkbox("Previsão de Chuva", value=False)
        hour = st.slider("Hora do Dia", 0, 23, 12)
        month = st.slider("Mês", 1, 12, 6)
    
    if st.button("🔮 Fazer Predição"):
        if model_status["model_loaded"]:
            prediction = ml_service.predict_irrigation(
                soil_moisture, soil_ph, phosphorus_present,
                potassium_present, temperature, air_humidity,
                rain_forecast, hour, month
            )
            
            if prediction["success"]:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    decision = "💧 IRRIGAR" if prediction["should_irrigate"] else "⛔ NÃO IRRIGAR"
                    color = "green" if prediction["should_irrigate"] else "red"
                    st.markdown(f"<h2 style='color: {color}; text-align: center;'>{decision}</h2>", unsafe_allow_html=True)
                
                with col2:
                    st.metric("Confiança", f"{prediction['confidence']:.1%}")
                
                with col3:
                    st.metric("Prob. Irrigação", f"{prediction['irrigation_probability']:.1%}")
        else:
            st.error("❌ Modelo não treinado. Treine o modelo primeiro!")

# ---------------------- CLIMATE DATA -------------------------
elif aba == "🌤️ Dados Climáticos":
    st.title("🌤️ Dados Climáticos")
    df = pd.DataFrame(climate_service.list_climate_data())

    if df.empty:
        st.info("Nenhum dado climático disponível.")
    else:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        st.dataframe(df, use_container_width=True)

        st.subheader("📊 Visualização de tendências climáticas")

        # Gráficos interativos com Plotly
        col1, col2 = st.columns(2)
        
        with col1:
            fig_temp = px.line(df, x="timestamp", y="temperature", 
                             title="Temperatura ao longo do tempo",
                             markers=True)
            fig_temp.update_layout(height=400)
            st.plotly_chart(fig_temp, use_container_width=True)
        
        with col2:
            fig_hum = px.line(df, x="timestamp", y="air_humidity", 
                            title="Umidade do ar ao longo do tempo",
                            markers=True)
            fig_hum.update_layout(height=400)
            st.plotly_chart(fig_hum, use_container_width=True)
        
        # Gráfico de dispersão
        fig_scatter = px.scatter(df, x="temperature", y="air_humidity", 
                               title="Correlação entre temperatura e umidade",
                               color="rain_forecast")
        st.plotly_chart(fig_scatter, use_container_width=True)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Exportar como CSV",
            data=csv,
            file_name='climate_data.csv',
            mime='text/csv'
        )

        # CRUD operations
        with st.expander("➕ Novo Registro Climático"):
            col1, col2, col3 = st.columns(3)
            with col1:
                temperature = st.number_input("Temperatura (°C)", format="%.2f")
            with col2:
                air_humidity = st.number_input("Umidade do ar (%)", format="%.2f")
            with col3:
                rain_forecast = st.checkbox("Previsão de chuva")

            if st.button("Cadastrar"):
                record = climate_service.create_climate_data({
                    "temperature": temperature,
                    "air_humidity": air_humidity,
                    "rain_forecast": rain_forecast,
                    "timestamp": datetime.utcnow()
                })
                st.success(f"Registro criado com ID {record['id']}")
                st.rerun()

        with st.expander("✏️ Editar ou remover registro climático"):
            ids = [r["id"] for r in climate_service.list_climate_data()]
            selected_id = st.selectbox("Selecione o registro:", ids)
            if selected_id:
                registro = climate_service.get_climate_data(selected_id)
                temp = st.number_input("Nova Temperatura", value=registro["temperature"], format="%.2f")
                hum = st.number_input("Nova Umidade", value=registro["air_humidity"], format="%.2f")
                rain = st.checkbox("Chuva prevista", value=registro["rain_forecast"])
                if st.button("Atualizar"):
                    climate_service.update_climate_data(selected_id, {"temperature": temp, "air_humidity": hum, "rain_forecast": rain})
                    st.success("Atualizado com sucesso!")
                    st.rerun()
                if st.button("Deletar"):
                    climate_service.delete_climate_data(selected_id)
                    st.success("Removido com sucesso!")
                    st.rerun()

# ---------------------- SENSOR RECORDS -------------------------
elif aba == "🧪 Registros de Sensores":
    st.title("🧪 Registros dos Sensores")
    df = pd.DataFrame(sensor_service.list_sensor_records())

    if df.empty:
        st.info("Nenhum registro de sensor disponível.")
    else:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        st.dataframe(df, use_container_width=True)

        # Gráficos interativos
        col1, col2 = st.columns(2)
        
        with col1:
            fig_moisture = px.line(df, x="timestamp", y="soil_moisture", 
                                 title="Umidade do Solo ao longo do tempo",
                                 markers=True)
            fig_moisture.update_layout(height=400)
            st.plotly_chart(fig_moisture, use_container_width=True)
        
        with col2:
            fig_ph = px.line(df, x="timestamp", y="soil_ph", 
                           title="pH do Solo ao longo do tempo",
                           markers=True)
            fig_ph.update_layout(height=400)
            st.plotly_chart(fig_ph, use_container_width=True)

        with st.expander("📊 Visualização de Nutrientes e Irrigação"):
            # Gráfico de nutrientes
            df['phosphorus_present'] = df['phosphorus_present'].astype(bool)
            df['potassium_present'] = df['potassium_present'].astype(bool)
            
            nutrient_data = []
            for _, row in df.iterrows():
                nutrient_data.append({
                    'timestamp': row['timestamp'],
                    'nutrient': 'Fósforo',
                    'present': row['phosphorus_present']
                })
                nutrient_data.append({
                    'timestamp': row['timestamp'],
                    'nutrient': 'Potássio',
                    'present': row['potassium_present']
                })
            
            nutrient_df = pd.DataFrame(nutrient_data)
            fig_nutrients = px.scatter(nutrient_df, x="timestamp", y="nutrient", 
                                     color="present", title="Presença de Nutrientes")
            st.plotly_chart(fig_nutrients, use_container_width=True)

            # Gráfico de status de irrigação
            df_sorted = df.sort_values(by="timestamp")
            df_sorted['status_numeric'] = df_sorted['irrigation_status'].apply(lambda x: 1 if x == "ATIVADA" else 0)
            
            fig_irrigation = px.line(df_sorted, x="timestamp", y="status_numeric", 
                                   title="Status de Irrigação ao longo do tempo")
            fig_irrigation.update_layout(height=400)
            st.plotly_chart(fig_irrigation, use_container_width=True)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Exportar como CSV",
            data=csv,
            file_name='sensor_data.csv',
            mime='text/csv'
        )

        # CRUD operations
        with st.expander("➕ Novo Registro de Sensor"):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                soil_moisture = st.number_input("Umidade do Solo (%)", format="%.2f")
            with col2:
                soil_ph = st.number_input("pH do Solo", format="%.2f")
            with col3:
                phosphorus_present = st.checkbox("Fósforo Presente")
            with col4:
                potassium_present = st.checkbox("Potássio Presente")

            irrigation_status = st.selectbox("Status da Irrigação", ["ATIVADA", "DESLIGADA"])

            if st.button("Cadastrar"):
                record = sensor_service.create_sensor_record({
                    "soil_moisture": soil_moisture,
                    "soil_ph": soil_ph,
                    "phosphorus_present": phosphorus_present,
                    "potassium_present": potassium_present,
                    "irrigation_status": irrigation_status,
                    "timestamp": datetime.utcnow()
                })
                st.success(f"Registro criado com ID {record['id']}")
                st.rerun()

        with st.expander("✏️ Editar ou remover registro de sensor"):
            ids = [r["id"] for r in sensor_service.list_sensor_records()]
            selected_id = st.selectbox("Selecione o registro:", ids)
            if selected_id:
                registro = sensor_service.get_sensor_record(selected_id)
                moisture = st.number_input("Nova Umidade", value=registro["soil_moisture"], format="%.2f")
                ph = st.number_input("Novo pH", value=registro["soil_ph"], format="%.2f")
                phos = st.checkbox("Fósforo Presente", value=registro["phosphorus_present"])
                pot = st.checkbox("Potássio Presente", value=registro["potassium_present"])
                status = st.selectbox("Status", ["ATIVADA", "DESLIGADA"], 
                                    index=0 if registro["irrigation_status"] == "ATIVADA" else 1)
                
                if st.button("Atualizar"):
                    sensor_service.update_sensor_record(selected_id, {
                        "soil_moisture": moisture, 
                        "soil_ph": ph, 
                        "phosphorus_present": phos, 
                        "potassium_present": pot,
                        "irrigation_status": status
                    })
                    st.success("Atualizado com sucesso!")
                    st.rerun()
                if st.button("Deletar"):
                    sensor_service.delete_sensor_record(selected_id)
                    st.success("Removido com sucesso!")
                    st.rerun()

# ---------------------- ANÁLISES AVANÇADAS -------------------------
elif aba == "📊 Análises Avançadas":
    st.title("📊 Análises Avançadas e Insights")
    st.markdown("**Análises preditivas e correlações entre variáveis**")
    
    # Carregar dados
    sensor_df = pd.DataFrame(sensor_service.list_sensor_records())
    climate_df = pd.DataFrame(climate_service.list_climate_data())
    
    if not sensor_df.empty and not climate_df.empty:
        sensor_df["timestamp"] = pd.to_datetime(sensor_df["timestamp"])
        climate_df["timestamp"] = pd.to_datetime(climate_df["timestamp"])
        
        # Mesclar dados
        sensor_df['timestamp_hour'] = sensor_df['timestamp'].dt.floor('H')
        climate_df['timestamp_hour'] = climate_df['timestamp'].dt.floor('H')
        
        merged_df = pd.merge(sensor_df, climate_df, 
                           left_on='timestamp_hour', 
                           right_on='timestamp_hour', 
                           how='inner', suffixes=('_sensor', '_climate'))
        
        if not merged_df.empty:
            st.subheader("🔍 Correlações entre Variáveis")
            
            # Matriz de correlação
            numeric_cols = ['soil_moisture', 'soil_ph', 'temperature', 'air_humidity']
            correlation_matrix = merged_df[numeric_cols].corr()
            
            fig_corr = px.imshow(correlation_matrix, 
                               title="Matriz de Correlação entre Variáveis",
                               color_continuous_scale='RdBu')
            st.plotly_chart(fig_corr, use_container_width=True)
            
            # Análise temporal
            st.subheader("⏰ Análise Temporal")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Umidade por hora do dia
                merged_df['hour'] = merged_df['timestamp_sensor'].dt.hour
                hourly_moisture = merged_df.groupby('hour')['soil_moisture'].mean().reset_index()
                
                fig_hourly = px.bar(hourly_moisture, x='hour', y='soil_moisture',
                                  title="Umidade Média por Hora do Dia")
                st.plotly_chart(fig_hourly, use_container_width=True)
            
            with col2:
                # Temperatura vs Umidade do Solo
                fig_temp_moisture = px.scatter(merged_df, x='temperature', y='soil_moisture',
                                             title="Temperatura vs Umidade do Solo",
                                             color='irrigation_status')
                st.plotly_chart(fig_temp_moisture, use_container_width=True)
            
            # Estatísticas descritivas
            st.subheader("📈 Estatísticas Descritivas")
            st.dataframe(merged_df[numeric_cols].describe())
            
            # Análise de padrões de irrigação
            st.subheader("💧 Padrões de Irrigação")
            
            irrigation_patterns = merged_df.groupby('irrigation_status').agg({
                'soil_moisture': ['mean', 'std', 'min', 'max'],
                'soil_ph': ['mean', 'std'],
                'temperature': ['mean', 'std'],
                'air_humidity': ['mean', 'std']
            }).round(2)
            
            st.dataframe(irrigation_patterns)
            
        else:
            st.warning("Dados insuficientes para análise avançada")
    else:
        st.info("Adicione dados de sensores e clima para visualizar análises avançadas")

# ---------------------- COMPONENTES -------------------------
elif aba == "⚙️ Componentes":
    st.title("⚙️ Gerenciamento de Componentes")
    df = pd.DataFrame(component_service.list_components())

    if df.empty:
        st.info("Nenhum componente cadastrado.")
    else:
        st.dataframe(df, use_container_width=True)

        with st.expander("➕ Novo Componente"):
            col1, col2, col3 = st.columns(3)
            with col1:
                name = st.text_input("Nome do Componente")
            with col2:
                component_type = st.selectbox("Tipo", ["Sensor", "Atuador", "Controlador"])
            with col3:
                status = st.selectbox("Status", ["Ativo", "Inativo", "Manutenção"])

            description = st.text_area("Descrição")

            if st.button("Cadastrar"):
                record = component_service.create_component({
                    "name": name,
                    "component_type": component_type,
                    "status": status,
                    "description": description
                })
                st.success(f"Componente criado com ID {record['id']}")
                st.rerun()

        with st.expander("✏️ Editar ou remover componente"):
            ids = [r["id"] for r in component_service.list_components()]
            selected_id = st.selectbox("Selecione o componente:", ids)
            if selected_id:
                registro = component_service.get_component(selected_id)
                name = st.text_input("Nome", value=registro["name"])
                component_type = st.selectbox("Tipo", ["Sensor", "Atuador", "Controlador"], 
                                            index=["Sensor", "Atuador", "Controlador"].index(registro["component_type"]))
                status = st.selectbox("Status", ["Ativo", "Inativo", "Manutenção"], 
                                    index=["Ativo", "Inativo", "Manutenção"].index(registro["status"]))
                description = st.text_area("Descrição", value=registro["description"])
                
                if st.button("Atualizar"):
                    component_service.update_component(selected_id, {
                        "name": name, 
                        "component_type": component_type, 
                        "status": status,
                        "description": description
                    })
                    st.success("Atualizado com sucesso!")
                    st.rerun()
                if st.button("Deletar"):
                    component_service.delete_component(selected_id)
                    st.success("Removido com sucesso!")
                    st.rerun()
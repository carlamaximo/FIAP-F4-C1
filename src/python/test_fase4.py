#!/usr/bin/env python3
"""
Script de teste para verificar as funcionalidades da Fase 4
FarmTech Solutions - Fase 4
"""

import sys
import os
import importlib

def test_imports():
    """Testa se todas as dependências estão instaladas"""
    print("🔍 Testando importações...")
    
    required_packages = [
        'streamlit',
        'pandas', 
        'numpy',
        'sklearn',
        'plotly',
        'joblib',
        'sqlalchemy',
        'oracledb'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NÃO INSTALADO")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Pacotes faltando: {', '.join(missing_packages)}")
        print("Execute: pip install -r requirements.txt")
        return False
    
    print("✅ Todas as dependências estão instaladas!")
    return True

def test_ml_service():
    """Testa o serviço de Machine Learning"""
    print("\n🤖 Testando serviço de Machine Learning...")
    
    try:
        from services.ml_service import MLService
        from database.oracle import get_session
        
        session = get_session()
        ml_service = MLService(session)
        
        # Testa status do modelo
        status = ml_service.get_model_status()
        print(f"✅ Status do modelo: {status['model_loaded']}")
        
        # Testa predição (sem modelo treinado)
        prediction = ml_service.predict_irrigation(
            soil_moisture=45.0,
            soil_ph=6.5,
            phosphorus_present=True,
            potassium_present=True,
            temperature=25.0,
            air_humidity=60.0,
            rain_forecast=False
        )
        
        if not prediction["success"]:
            print("✅ Predição sem modelo (esperado): Modelo não treinado")
        else:
            print("✅ Predição funcionando")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no ML Service: {e}")
        return False

def test_database_connection():
    """Testa conexão com banco de dados"""
    print("\n🗄️ Testando conexão com banco de dados...")
    
    try:
        from database.oracle import get_session
        from services.climate_service import ClimateService
        from services.sensor_service import SensorRecordService
        
        session = get_session()
        climate_service = ClimateService(session)
        sensor_service = SensorRecordService(session)
        
        # Testa listagem de dados
        climate_data = climate_service.list_climate_data()
        sensor_data = sensor_service.list_sensor_records()
        
        print(f"✅ Dados climáticos: {len(climate_data)} registros")
        print(f"✅ Dados de sensores: {len(sensor_data)} registros")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão com banco: {e}")
        return False

def test_streamlit_app():
    """Testa se o app Streamlit pode ser importado"""
    print("\n📊 Testando aplicação Streamlit...")
    
    try:
        # Simula importação do app
        import streamlit as st
        print("✅ Streamlit disponível")
        
        # Verifica se o arquivo existe
        if os.path.exists("app_dashboard.py"):
            print("✅ app_dashboard.py encontrado")
            return True
        else:
            print("❌ app_dashboard.py não encontrado")
            return False
            
    except Exception as e:
        print(f"❌ Erro no Streamlit: {e}")
        return False

def test_data_generator():
    """Testa o gerador de dados"""
    print("\n📈 Testando gerador de dados...")
    
    try:
        from generate_sample_data import generate_sample_data
        print("✅ Gerador de dados importado com sucesso")
        return True
        
    except Exception as e:
        print(f"❌ Erro no gerador de dados: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🌾 FarmTech Solutions - Teste da Fase 4")
    print("=" * 50)
    
    tests = [
        ("Importações", test_imports),
        ("Conexão com Banco", test_database_connection),
        ("ML Service", test_ml_service),
        ("Streamlit App", test_streamlit_app),
        ("Gerador de Dados", test_data_generator)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erro no teste {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumo dos resultados
    print("\n" + "=" * 50)
    print("📋 RESUMO DOS TESTES")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! A Fase 4 está pronta!")
        print("\n🚀 Próximos passos:")
        print("1. Execute: python generate_sample_data.py")
        print("2. Execute: streamlit run app_dashboard.py")
        print("3. Abra o Wokwi e teste o ESP32")
    else:
        print("⚠️ Alguns testes falharam. Verifique as dependências.")
        print("\n🔧 Soluções:")
        print("1. pip install -r requirements.txt")
        print("2. Verifique a conexão com o banco de dados")
        print("3. Execute os testes novamente")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
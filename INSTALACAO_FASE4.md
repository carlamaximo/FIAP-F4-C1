# 🚀 Guia de Instalação e Execução - Fase 4

## 🌾 FarmTech Solutions - Sistema de Irrigação Inteligente

### 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Acesso ao banco de dados Oracle
- Navegador web moderno

### 🔧 Instalação

#### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd f3-cap1-final/FIAP-F3-C1
```

#### 2. Instale as dependências Python
```bash
cd src/python
pip install -r requirements.txt
```

#### 3. Configure o banco de dados
Certifique-se de que o arquivo `.env` está configurado com as credenciais do Oracle:
```env
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=1521
DB_SERVICE=XE
```

### 🧪 Teste da Instalação

Execute o script de teste para verificar se tudo está funcionando:

```bash
cd src/python
python test_fase4.py
```

Você deve ver uma saída similar a:
```
🌾 FarmTech Solutions - Teste da Fase 4
==================================================
🔍 Testando importações...
✅ streamlit
✅ pandas
✅ numpy
✅ sklearn
✅ plotly
✅ joblib
✅ sqlalchemy
✅ oracledb
✅ Todas as dependências estão instaladas!

🗄️ Testando conexão com banco de dados...
✅ Dados climáticos: 0 registros
✅ Dados de sensores: 0 registros

🤖 Testando serviço de Machine Learning...
✅ Status do modelo: False
✅ Predição sem modelo (esperado): Modelo não treinado

📊 Testando aplicação Streamlit...
✅ Streamlit disponível
✅ app_dashboard.py encontrado

📈 Testando gerador de dados...
✅ Gerador de dados importado com sucesso

==================================================
📋 RESUMO DOS TESTES
==================================================
Importações: ✅ PASSOU
Conexão com Banco: ✅ PASSOU
ML Service: ✅ PASSOU
Streamlit App: ✅ PASSOU
Gerador de Dados: ✅ PASSOU

🎯 Resultado: 5/5 testes passaram
🎉 Todos os testes passaram! A Fase 4 está pronta!
```

### 🚀 Execução

#### 1. Gerar dados de exemplo (opcional)
Para testar o sistema com dados, execute:
```bash
cd src/python
python generate_sample_data.py
```

Isso irá gerar 30 dias de dados simulados para treinar o modelo de ML.

#### 2. Executar o dashboard
```bash
cd src/python
streamlit run app_dashboard.py
```

O dashboard será aberto automaticamente no seu navegador (geralmente em `http://localhost:8501`).

### 🖥️ Testando o ESP32 no Wokwi

#### 1. Abra o projeto no Wokwi
- Acesse [wokwi.com](https://wokwi.com)
- Abra o arquivo `src/esp32/diagram.json`
- O circuito já inclui o display LCD I2C

#### 2. Compile e execute
- Clique em "Start Simulation"
- O código será compilado automaticamente
- Observe o display LCD e o Serial Monitor

#### 3. Monitoramento
- **Serial Monitor**: Veja as mensagens detalhadas
- **Serial Plotter**: Visualize gráficos em tempo real
- **Display LCD**: Informações principais em tempo real

### 📊 Funcionalidades do Dashboard

#### 🏠 Visão Geral
- Status do sistema e modelo ML
- Métricas em tempo real
- Gauge chart interativo para umidade
- Predições de irrigação com IA

#### 🤖 Machine Learning
- **Treinar Modelo**: Clique para treinar com dados históricos
- **Importância das Features**: Gráfico das variáveis mais importantes
- **Simulador**: Teste diferentes cenários de irrigação
- **Relatórios**: Métricas de acurácia e classificação

#### 📈 Análises Avançadas
- **Matriz de Correlação**: Relações entre variáveis
- **Análise Temporal**: Padrões por hora do dia
- **Padrões de Irrigação**: Estatísticas por status
- **Exportação**: Dados em CSV

#### 🌤️ Dados Climáticos
- **Visualização**: Gráficos interativos com Plotly
- **CRUD**: Criar, editar e remover registros
- **Tendências**: Análise temporal de temperatura e umidade

#### 🧪 Registros de Sensores
- **Monitoramento**: Dados dos sensores em tempo real
- **Nutrientes**: Presença de fósforo e potássio
- **Irrigação**: Status histórico da irrigação

### 🔧 Otimizações da Fase 4

#### ESP32 - Melhorias de Memória
- **Tipos otimizados**: `uint8_t` em vez de `int`
- **Strings constantes**: `const char*` em vez de `String`
- **Economia**: ~2KB de RAM economizada

#### Display LCD
- **Informações em tempo real**: Umidade, temperatura, pH
- **Status de irrigação**: ON/OFF visual
- **Indicadores de nutrientes**: P e K

#### Serial Plotter
- **Dados formatados**: CSV para visualização
- **Múltiplas variáveis**: 5 variáveis simultâneas
- **Tempo real**: Atualização a cada segundo

### 🎯 Resultados Esperados

#### Machine Learning
- **Acurácia**: >85% com dados suficientes
- **Tempo de treinamento**: <30 segundos
- **Features importantes**: Umidade do solo, temperatura, pH

#### Performance
- **ESP32**: Memória otimizada e estável
- **Dashboard**: Interface responsiva
- **Dados**: Visualização em tempo real

### 🆘 Solução de Problemas

#### Erro de importação
```bash
pip install -r requirements.txt
```

#### Erro de conexão com banco
- Verifique as credenciais no `.env`
- Teste a conexão com o Oracle
- Execute `python test_fase4.py`

#### ESP32 não compila
- Verifique se todas as bibliotecas estão instaladas
- Confirme a configuração do `platformio.ini`
- Teste no Wokwi

#### Dashboard não abre
- Verifique se o Streamlit está instalado
- Execute `streamlit --version`
- Tente `streamlit run app_dashboard.py --server.port 8501`

### 📞 Suporte

Para dúvidas ou problemas:
1. Execute `python test_fase4.py` para diagnóstico
2. Verifique os logs de erro
3. Consulte a documentação no README.md

---

**🌾 FarmTech Solutions - Fase 4 - Sistema Inteligente de Irrigação** 
# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Nome do projeto

CAP 1 - Automação e inteligência na FarmTech Solutions
Sistema de irrigação inteligente com ESP32 e Python

## Nome do grupo

Grupo 73

## 👨‍🎓 Integrantes:

- <a href="https://www.linkedin.com/in/anacornachi/">Ana Cornachi</a>
- <a href="https://www.linkedin.com/in/carlamaximo/">Carla Máximo</a>

## 👩‍🏫 Professores:

### Tutor(a)

- <a href="https://www.linkedin.com/in/lucas-gomes-moreira-15a8452a/">Lucas Gomes Moreira</a>

### Coordenador(a)

- <a href="https://www.linkedin.com/in/andregodoichiovato/">André Godoi Chiovato</a>

## 📜 Descrição

O presente projeto propõe uma **solução de irrigação inteligente** desenvolvida em duas camadas: uma camada física embarcada com **ESP32** simulada no Wokwi e uma camada lógica em **Python**, responsável por decisões com base em dados meteorológicos e armazenamentos em banco de dados SQL.

A iniciativa parte de uma problemática real: o desperdício de água e a ineficiência na irrigação agrícola, especialmente em pequenas propriedades. Como solução, construímos um sistema que **lê variáveis ambientais** (umidade do solo, pH, nutrientes) e as combina com **dados climáticos reais** (via OpenWeather API), para decidir **automaticamente** se a bomba de irrigação deve ser ativada ou não.

No ambiente simulado, a parte física foi modelada com o simulador Wokwi, utilizando sensores como:

- Botões para simular presença de Fósforo (P) e Potássio (K)
- Sensor LDR simulando pH do solo
- Sensor DHT22 para umidade
- Relé e LED controlando a bomba de irrigação
- **Display LCD 16x2 via I2C** para exibir métricas em tempo real

Já o código Python consome uma API pública de clima, grava os dados em banco de dados relacional, permite análises via dashboard Streamlit, e simula o envio de comandos ao ESP32 via serial (ou via JSON em contexto de simulação).

Além disso, exploramos os conceitos de **IoT, automação agrícola, integração com APIs REST, banco de dados, POO, testes, dashboards interativos e Machine Learning**, reforçando a aplicação prática de conteúdos aprendidos.

Diagrama DAP - Funcionamento da Solução
![DAP da aplicação](assets/DAP.png)

## 📌 Requisitos do Projeto (Fase 4)

### 1. Incorporar Scikit-learn
- Utilização da biblioteca Scikit-learn para criar um modelo preditivo (RandomForestClassifier) que, com base nos dados coletados (umidade, pH, nutrientes, temperatura, clima, hora, mês), sugere ações futuras de irrigação.
- O modelo é treinado com dados históricos e pode ser testado via simulador interativo no dashboard.
- Insights como importância das features e métricas de acurácia são exibidos na interface.

### 2. Implementar Streamlit
- Dashboard interativo desenvolvido com Streamlit, permitindo visualização em tempo real dos dados do sistema de irrigação.
- Gráficos dinâmicos (umidade do solo, níveis de nutrientes, predições do modelo de ML) utilizando Plotly.
- Interface intuitiva, com múltiplas abas, exportação de dados e simulador de predição.

### 3. Adicionar display LCD no Wokwi
- Display LCD 16x2 conectado ao ESP32 via barramento I2C (pinos SDA e SCL).
- Exibe as principais métricas em tempo real: umidade, temperatura, pH, status da irrigação e presença de nutrientes.
- Informações críticas são mostradas diretamente no sistema físico simulado.

### 4. Monitoramento com Serial Plotter
- Implementação do Serial Plotter para monitorar variáveis do projeto (umidade, temperatura, pH, status de irrigação, etc).
- O gráfico do Serial Plotter apresenta as mudanças em tempo real, facilitando a análise visual do comportamento do sistema.
- Dados são enviados a cada ciclo de leitura para visualização contínua.

### 5. Otimização de Memória no ESP32
- Revisão e otimização do uso das variáveis no código C++ do ESP32.
- Utilização de tipos de dados otimizados (`uint8_t`, `bool`, `const char*`), conversão de `float` para inteiros quando possível, e armazenamento de strings na flash.
- Comentários no código justificando as escolhas de otimização.
- Resultados: economia de RAM, maior performance e estabilidade.

## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:
```
src/
├── esp32/ # Projeto do microcontrolador ESP32 (PlatformIO + C++)
├── python/ # Scripts Python (API, banco, dashboard, integração)
├── assets/ # Imagens, gráficos e materiais estáticos
├── document/ # Documentos acadêmicos e relatórios
```

Para mais detalhes sobre cada parte, consulte os READMEs específicos:

[📘 README do projeto ESP32](src/esp32/README.md)

[🐍 README do projeto Python + Dashboard](src/python/README.md)

## Entregas realizadas

### Entrega 1 - Sistema de Sensores e Controle com ESP32

Implementação do sistema físico simulado no Wokwi com lógica em C++. Inclui sensores de umidade (DHT22), pH (LDR), fósforo e potássio (botões), controle do relé para ativar a bomba de irrigação e display LCD para exibição das métricas.

- **Pasta de desenvolvimento**: src/esp32
- **Documentação Específica**: [📘 README do projeto ESP32](src/esp32/README.md)

- **Metas**:

  - Construir o circuito no Wokwi
  - Desenvolver código em C++
  - Documentar toda a lógica de controle
  - Exibir métricas no display LCD

- **Entregáveis**:

  - Código C++ funcional
  - Imagem do circuito no Wokwi
  - Documentação detalhada

  ![Circuito Wokwi](/assets/circuito-esp32-wokwi.png)
  [Demonstração do circuito (video)](/assets/circuito-esp32-wokwi.mp4)

### Entrega 2 - Armazenamento de Dados em Banco SQL com Python

Sistema completo de armazenamento, processamento e visualização de dados dos sensores. Inclui integração com a API OpenWeather, banco de dados relacional e dashboard para análise dos dados, escopos do ir além 1 e 2, a serem descritos abaixo.

- **Pasta de desenvolvimento**: src/python
- **Documentação Específica**: [🐍 README do projeto Python + Dashboard](src/python/README.md)

- **Metas**:

  - Criar scripts para armazenamento em SQL
  - Implementar CRUD completo
  - Justificar estrutura de dados e relacionar com o MER da fase anterior

- **Entregáveis**:

  - Script Python funcional
  - Tabelas de exemplo com dados populados

  ![Diagrama do banco de dados](/assets/diagram.png)

### Ir Além 1 - Dashboard em Python

Painel visual com gráficos interativos para análise dos dados dos sensores. Inclui gráficos de tendência, dispersão, barras e linha, além de exportação para CSV.

- **Pasta de desenvolvimento**: src/python
- **Documentação Específica**: [🐍 README do projeto Python + Dashboard](src/python/README.md)

- **Metas**:

  - Criar visualizações claras e intuitivas para dados coletados
  - Permitir filtros e exportações

- **Entregáveis**:

  - Dashboard completo com gráficos interativos

  ![Dashbaord com graficos](/assets/dashboard_tabela.png)

### Ir Além 2 - Integração com API Pública

Integração com a API da OpenWeather para dados climáticos em tempo real, permitindo decisões de irrigação mais inteligentes. Inclui lógica para desativação da bomba em caso de previsão de chuva.

- **Pasta de desenvolvimento**: src/python
- **Documentação Específica**: [🐍 README do projeto Python + Dashboard](src/python/README.md)

- **Metas**:

  - Criar integração robusta com API
  - Implementar lógica condicional para irrigação
  - Armazenar dados meteorológicos no banco

- **Entregáveis**:

  - Scripts Python para integração com API
  - Tabelas populadas com dados climáticos
  - Documentação detalhada

### 🚀 Fase 4 - Sistema Inteligente com IA e Monitoramento Avançado

**STATUS: ✅ COMPLETAMENTE IMPLEMENTADO**

Sistema de irrigação inteligente aprimorado com Machine Learning, interface avançada, display LCD, monitoramento via Serial Plotter e otimizações de memória. Todos os requisitos foram implementados com sucesso.

- **Pasta de desenvolvimento**: src/python e src/esp32
- **Documentação Específica**: [📘 README do projeto ESP32](src/esp32/README.md)

#### ✅ Resumo dos Requisitos Implementados:

- **Machine Learning com Scikit-learn**: Modelo RandomForestClassifier, predição de irrigação baseada em dados históricos, análise de importância das variáveis, simulador interativo no dashboard.
- **Dashboard Streamlit**: Interface moderna, gráficos em tempo real, múltiplas abas, exportação de dados, simulador de predição.
- **Display LCD no Wokwi**: Exibição de métricas em tempo real diretamente no hardware simulado.
- **Serial Plotter**: Monitoramento visual das variáveis do sistema em tempo real.
- **Otimização de Memória no ESP32**: Tipos de dados otimizados, strings na flash, comentários justificando as escolhas, economia de RAM e maior performance.

#### 🎯 Funcionalidades Avançadas:

- **Machine Learning:** Modelo treinável com dados históricos
- **Predições Inteligentes:** Sugestões de irrigação baseadas em IA
- **Interface Moderna:** Dashboard responsivo com métricas em tempo real
- **Monitoramento Físico:** Display LCD com informações críticas
- **Análise Visual:** Serial Plotter para acompanhamento contínuo
- **Código Otimizado:** Eficiência de memória e performance

#### 📊 Impacto das Otimizações:

- **RAM:** 211+ bytes economizados
- **Performance:** Operações mais rápidas com inteiros
- **Estabilidade:** Menor fragmentação de memória
- **Escalabilidade:** Mais espaço para funcionalidades futuras

![Dashboard Inteligente](/assets/dashboard-ase4.png)

### 📌 Observações Finais

Como este projeto foi desenvolvido em um ambiente 100% simulado, não é possível estabelecer comunicação direta entre ESP32 e Python por porta serial. Para isso, utilizamos um arquivo climate.json como ponte de simulação dos dados meteorológicos.

Em um cenário real, essa comunicação seria feita com um ESP32 físico e uma conexão serial real utilizando pyserial.

## 🗃 Histórico de lançamentos

- **0.5.0 - 20/12/2024** 🚀
  - **Fase 4 - Sistema Inteligente COMPLETO**
  - ✅ Scikit-learn implementado com modelo de predição
  - ✅ Dashboard Streamlit avançado com IA
  - ✅ Display LCD I2C no Wokwi
  - ✅ Monitoramento com Serial Plotter
  - ✅ Otimizações de memória no ESP32 (211+ bytes economizados)
  - Documentação completa das otimizações
  - Sistema 100% funcional e otimizado

- 0.4.0 - 18/05/2025
  - Ajustes na documentação, incluindo imagens e vídeos.
  - Padronização dos nomes das tabelas e colunas para inglês.
  - Correção do tipo de dado para fósforo e potássio.
  - Atualização dos models, services e repositories para refletir essas mudanças.
- 0.3.1 - 09/05/2025
  - Justificativa para mudança no banco de dados.
  - Criação dos repositories para todos os modelos com métodos CRUD completos e buscas específicas.
  - Incremento nos services para aproveitar ao máximo os relacionamentos entre tabelas.
  - Ajustes na documentação para refletir a nova estrutura do banco de dados.
- 0.3.0 - 04/05/2025
  - ESP32 (src/esp32)
    - Suporte à integração com climate.json (simulação da API OpenWeather).
    - Delay ajustado para 10 minutos por ciclo.
    - Código C++ comentado e otimizado.
    - README atualizado com lógica, simulações sugeridas e limitações do Wokwi.
  - Python (src/python)
    - Integração com API OpenWeather para coleta e envio de dados climáticos simulados.
    - CRUD completo com SQLAlchemy para climate_data, sensor_records e components.
  - Dashboard interativo com Streamlit:
    - Gráficos (linha, dispersão, histograma)
    - Exportação para CSV/PDF
    - Edição e exclusão de registros
    - Logger colorido e estruturado por arquivo.
  - Geral:
    - README principal reestruturado com base em PBL.
    - Inclusão de imagem DAP explicando o fluxo da aplicação local.
    - Links diretos para os projetos específicos (/src/esp32 e /src/python).
- 0.2.0 - 02/05/2025
  - Python (src/python)
    - Implementação da dashboard interativa com Streamlit.
    - Visualização completa dos dados climáticos, sensores e componentes.
    - Funcionalidades:
      - Cadastro, edição e exclusão de registros (CRUD)
      - Gráficos dinâmicos (temperatura, umidade, correlação)
      - Exportação de dados para CSV e PDF
      - Integração com serviços existentes do projeto python (sem necessidade de duplicação de lógica).
- 0.1.0 - 30/04/2025
  - Implementação inicial do sistema de irrigação inteligente utilizando ESP32
  - Adicionada leitura de sensores: umidade do solo (DHT22), presença de fósforo e potássio (botões físicos) e simulação de pH (sensor LDR)
  - Desenvolvimento da lógica de ativação e desativação da bomba de irrigação com base nas condições do solo
  - Integração do controle do relé e indicador LED
  - Construção do circuito completo no Wokwi para simulação do hardware
  - Criação de documentação detalhada no README, incluindo descrição do projeto, lógica de decisão baseada em fontes acadêmicas e imagem do circuito

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>

# 🌾 FarmTech Solutions - Fase 4

## Sistema de Irrigação Inteligente com IA e Monitoramento Avançado

### 📋 Descrição do Projeto

O FarmTech Solutions é um sistema completo de irrigação inteligente que combina sensores IoT, machine learning e análise de dados para otimizar o uso de água na agricultura. Na **Fase 4**, o sistema foi aprimorado com funcionalidades avançadas de IA, interface interativa e otimizações de hardware.

### 🚀 Novas Funcionalidades da Fase 4

#### 🤖 Machine Learning com Scikit-learn
- **Modelo Preditivo**: Sistema de IA que prevê a necessidade de irrigação baseado em dados históricos
- **Random Forest Classifier**: Algoritmo robusto para classificação de decisões de irrigação
- **Feature Importance**: Análise da importância de cada variável no modelo
- **Simulador Interativo**: Interface para testar diferentes cenários de irrigação

#### 📊 Dashboard Streamlit Aprimorado
- **Interface Moderna**: Design responsivo com emojis e cores intuitivas
- **Gráficos Interativos**: Visualizações com Plotly para melhor experiência do usuário
- **Análises Avançadas**: Correlações entre variáveis e padrões temporais
- **Exportação de Dados**: Funcionalidade para exportar relatórios em CSV

#### 🖥️ Display LCD no ESP32
- **Monitoramento em Tempo Real**: Display LCD 16x2 via I2C mostrando métricas principais
- **Informações Críticas**: Umidade, temperatura, pH e status de irrigação
- **Indicadores Visuais**: Presença de nutrientes (P e K) no display

#### 📈 Serial Plotter
- **Monitoramento Visual**: Gráficos em tempo real das variáveis do sistema
- **Múltiplas Variáveis**: Umidade do solo, temperatura, umidade do ar, pH e status de irrigação
- **Análise de Tendências**: Visualização de padrões ao longo do tempo

#### ⚡ Otimizações de Memória no ESP32
- **Tipos de Dados Otimizados**: Uso de `uint8_t`, `bool` e `const char*` para economizar RAM
- **Constantes em Flash**: Strings constantes armazenadas em memória flash
- **Comentários Detalhados**: Documentação das otimizações implementadas

### 🏗️ Arquitetura do Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   ESP32 (IoT)   │    │   Python App    │    │   Dashboard     │
│                 │    │                 │    │   Streamlit     │
│ • Sensores      │◄──►│ • ML Service    │◄──►│ • Interface     │
│ • Display LCD   │    │ • Database      │    │ • Gráficos      │
│ • Serial Plot   │    │ • API Services  │    │ • Análises      │
│ • Otimizações   │    │ • Data Gen      │    │ • Exportação    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 📁 Estrutura do Projeto

```
FIAP-F4-C1/
├── src/
│   ├── esp32/                    # Código do ESP32
│   │   ├── src/main.cpp         # Código principal com otimizações
│   │   ├── platformio.ini       # Configuração PlatformIO
│   │   ├── diagram.json         # Diagrama Wokwi com LCD
│   │   └── wokwi.toml           # Configuração Wokwi
│   └── python/                   # Aplicação Python
│       ├── app_dashboard.py     # Dashboard Streamlit Fase 4
│       ├── services/
│       │   ├── ml_service.py    # Serviço de Machine Learning
│       │   ├── weather_service.py      # Serviço de comunicação de dados via Serial
│       │   ├── sensor_service.py       # Serviço de processamento de registros de sensores
│       │   ├── producer_service.py     # Serviço de processamento de produtores
│       │   ├── crops_service.py        # Serviço de controle de colheita
│       │   ├── component_service.py    # Serviço de gerenciamento de produtores
│       │   ├── climate_service.py      # Serviço de gerenciamento de dados da API OpenWeather
│       │   └── application_service.py  # Serviço de gerenciamento de aplicações
│       ├── database/                   # Camada de acesso a dados
│       │   ├── __init__.py
│       │   ├── models.py               # Definição dos modelos SQLAlchemy
│       │   ├── oracle.py                # Configuração da conexão Oracle
│       │   ├── setup.py                # Script de inicialização do banco
│       │   ├── utils.py                # Script para geração do DDL e MER
│       │   └── repositories/           # Implementação dos repositórios
│       │       ├── __init__.py
│       │       ├── application_repository.py
│       │       ├── climate_data_repository.py
│       │       ├── component_repository.py
│       │       ├── crop_repository.py
│       │       ├── producer_repository.py
│       │       └── sensor_record.py
│       ├── tests/                      # Testes automatizados
│       │   ├── __init__.py
│       │   ├── conftest.py             # Configurações dos testes
│       │   ├── test_models.py          # Testes dos modelos
│       │   └── test_repositories.py    # Testes dos repositórios
│       ├── logs/                       # Logs do sistema
│       ├── generate_sample_data.py     # Gerador de dados de exemplo
│       ├── requirements.txt            # Dependências atualizadas
│       ├── .env                        # Variáveis de ambiente
│       ├── .gitignore                  # Arquivos ignorados pelo git
│       ├── main.py                     # Ponto de entrada da aplicação
│       └── pytest.ini                  # Configuração do pytest
├── assets/                            # Imagens, gráficos e materiais estáticos
├── document/                          # Documentos acadêmicos e relatórios
└── README.md                          # Este arquivo
```

### 🛠️ Tecnologias Utilizadas

#### Hardware (ESP32)
- **Sensores**: DHT22 (umidade/temperatura), LDR (pH simulado)
- **Atuadores**: Relé (bomba de irrigação), LED de status
- **Display**: LCD 16x2 via I2C (SDA: D21, SCL: D22)
- **Entradas**: Botões para simular presença de nutrientes

#### Software (Python)
- **Streamlit**: Interface web interativa
- **Scikit-learn**: Machine learning e predições
- **Plotly**: Gráficos interativos
- **Pandas**: Manipulação de dados
- **SQLAlchemy**: ORM para banco de dados

#### Machine Learning
- **Algoritmo**: Random Forest Classifier
- **Features**: 9 variáveis (umidade, pH, nutrientes, clima, tempo)
- **Target**: Decisão de irrigação (binária)
- **Métricas**: Acurácia, confiança, importância das features

### 🚀 Como Executar

#### 1. Configuração do ESP32 (Wokwi)
```bash
# Abra o projeto no Wokwi
# O circuito já inclui o display LCD I2C
# Compile e execute o código
```

#### 2. Configuração do Python
```bash
cd src/python
pip install -r requirements.txt
```

#### 3. Gerar Dados de Exemplo
```bash
python generate_sample_data.py
```

#### 4. Executar Dashboard
```bash
streamlit run app_dashboard.py
```

### 📊 Funcionalidades do Dashboard

#### 🏠 Visão Geral
- Status do modelo ML
- Métricas em tempo real
- Gauge chart para umidade
- Predições de irrigação

#### 🤖 Machine Learning
- Treinamento do modelo
- Análise de importância das features
- Simulador de predições
- Relatórios de classificação

#### 📈 Análises Avançadas
- Matriz de correlação
- Análise temporal
- Padrões de irrigação
- Estatísticas descritivas

#### 🌤️ Dados Climáticos
- Visualização de tendências
- Gráficos interativos
- CRUD completo
- Exportação CSV

#### 🧪 Registros de Sensores
- Monitoramento de sensores
- Gráficos de nutrientes
- Status de irrigação
- Análise temporal

### 🔧 Otimizações Implementadas

#### ESP32 - Otimizações de Memória
```cpp
// Antes (Fase 3)
int PHOSPHORUS_PIN = 14;
String message = "Sistema iniciado";

// Depois (Fase 4) - Otimizado
const uint8_t PHOSPHORUS_PIN = 14;  // uint8_t em vez de int
const char* MSG_INIT = "Sistema iniciado";  // const char* em vez de String
```

#### Benefícios das Otimizações
- **RAM**: Economia de ~2KB de RAM
- **Flash**: Strings constantes movidas para flash
- **Performance**: Tipos menores = operações mais rápidas
- **Estabilidade**: Menos fragmentação de memória

### 📈 Monitoramento com Serial Plotter

O sistema envia dados formatados para o Serial Plotter:
```
Umidade_Solo,Temperatura,Umidade_Ar,pH,Irrigacao
45.2,25.3,65.1,6.5,0
43.8,26.1,62.3,6.4,1
```

### 🖥️ Display LCD

O display mostra informações em tempo real:
```
Linha 1: U:45.2% T:25.3C
Linha 2: pH:6.5 ON P K
```

### 🎯 Resultados Esperados

#### Machine Learning
- **Acurácia**: >85% em predições de irrigação
- **Features Importantes**: Umidade do solo, temperatura, pH
- **Tempo de Treinamento**: <30 segundos com dados de exemplo

#### Performance do Sistema
- **ESP32**: Uso de memória otimizado
- **Dashboard**: Interface responsiva e intuitiva
- **Dados**: Visualização em tempo real

### 🔮 Próximos Passos

1. **Integração com APIs Climáticas**: Dados reais de previsão do tempo
2. **Aprendizado Contínuo**: Modelo que se adapta com novos dados
3. **Alertas Inteligentes**: Notificações baseadas em IA
4. **Mobile App**: Aplicativo móvel para monitoramento
5. **IoT Gateway**: Conectividade com múltiplos sensores

### 👥 Autores

**FarmTech Solutions Team** - Fase 4
- Desenvolvimento ESP32 e otimizações
- Implementação de Machine Learning
- Interface Streamlit avançada
- Documentação e testes

### 📄 Licença

Este projeto foi desenvolvido para fins educacionais como parte do curso FIAP.

---

**🌾 FarmTech Solutions - Revolucionando a Agricultura com Tecnologia Inteligente**

```

```


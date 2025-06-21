# Sistema de sensores e controle com ESP32

## 🚀 Requisitos Fase 4 - Implementações Avançadas

Esta versão do projeto atende aos requisitos avançados da Fase 4:

### 1. Display LCD 16x2 via I2C
- O circuito inclui um display LCD 16x2 conectado ao ESP32 via barramento I2C (SDA: GPIO 21, SCL: GPIO 22).
- O display exibe em tempo real: umidade do solo, temperatura, pH, status da irrigação e presença de nutrientes (P/K).
- Mensagens de inicialização e status do sistema também são exibidas.

### 2. Monitoramento com Serial Plotter
- O código envia, a cada ciclo, as principais variáveis (umidade, temperatura, pH, status de irrigação, nutrientes) para o Serial Plotter.
- Isso permite acompanhar graficamente, em tempo real, o comportamento do sistema e as decisões de irrigação.

### 3. Otimização de Memória no ESP32
- O código foi revisado para utilizar tipos de dados otimizados (`uint8_t`, `bool`, `const char*`), reduzindo o consumo de RAM.
- Strings constantes são armazenadas na flash.
- Comentários no código justificam as escolhas de otimização.
- Essas práticas garantem maior performance e estabilidade ao firmware.

### 4. Integração Simulada com Dados Climáticos
- O sistema lê dados climáticos simulados via string JSON (exemplo: `climate_json`), representando o que seria recebido do Python em um cenário real.
- As decisões de irrigação consideram tanto sensores locais quanto dados externos (temperatura, umidade do ar, previsão de chuva).

### 5. Integração com Sistema Python
- Em ambiente real, a comunicação seria feita via porta serial (pyserial). No Wokwi, a integração é simulada via JSON embutido no código.
- O sistema Python é responsável por buscar dados climáticos reais e alimentar o ESP32.

---

# Descrição do Projeto

Este projeto implementa um sistema de irrigação inteligente utilizando a plataforma ESP32, sensores simulados no ambiente Wokwi e integração com o PlatformIO no VSCode.

O objetivo é criar um protótipo funcional capaz de **monitorar variáveis do solo** (umidade, nutrientes e pH) e **acionar a bomba de irrigação** conforme condições previamente estabelecidas, usando tanto dados locais dos sensores quanto informações climáticas externas, simuladas via JSON.

## Objetivos da entrega 1

- Construir o circuito de sensores usando as extensões Wokwi e PlatformIO.
- Criar código em C/C++ para ler os sensores e acionar o relé conforme a lógica definida.
- Comentar o código explicando a lógica utilizada.
- Documentar o circuito com imagem no README.

## Estrutura de entrega

Toda a lógica relacionada ao sistema do ESP32 (código-fonte, circuito, testes e documentação) está localizada dentro da pasta src/esp32/.

Portanto, todos os caminhos abaixo consideram como raiz o diretório src/esp32/.

| Arquivo                | Descrição                                            |
| :--------------------- | :--------------------------------------------------- |
| `src/main.cpp`         | Código fonte em C++ para controle de sensores e relé |
| `diagram.json`         | Definição do circuito no Wokwi                       |
| `circuito-esp32-wokwi-fase-4.png` | Imagem exportada do circuito da fase 4                        |
| `README.md`            | Documentação do projeto                              |

## Requisitos do sistema

Para executar este projeto, você precisará de:

- VSCode com as extensões PlatformIO e Wokwi instaladas.
- ESP32 (simulado no Wokwi).
- Python 3.10+ para integração com dados externos (simulação via JSON).
- PlatformIO CLI instalado.

## Como rodar o projeto

1. Clone o repositório.

```bash
git clone https://github.com/anacornachi/FIAP-F3-C1.git
```

2. Abra o projeto no VSCode

```bash
cd FIAP-F3-C1/src/esp32
```

3. Certifique-se de estar com as extensões Wokwi e PlatformIO instaladas.

4. Compile o projeto:

```bash
pio run
```

5. Inicie a simulação:

   - Clique em "Wokwi: Start Simulator" ou pressione Ctrl+Shift+P → "Wokwi: Start Simulator"

6. Acompanhe o comportamento dos sensores e a ativação da bomba de irrigação no monitor serial.

## Circuito desenvolvido no Wokwi

![Circuito no Wokwi](../../assets/circuito-esp32-wokwi-fase-4.png)

Legenda dos componentes:
| Componente | Simulação | GPIO ESP32 | Descrição |
|----------------------|----------------------------|------------|-----------|
| Botão de fósforo | Presença de fósforo (P) | GPIO 14 | Pressionado = presente |
| Botão de potássio | Presença de potássio (K) | GPIO 4 | Pressionado = presente |
| LDR | Simulação de pH do solo | GPIO 34 | Valor analógico convertido em escala de 0 a 14 |
| DHT22 | Umidade do solo | GPIO 5 | Sensor digital de umidade do solo |
| Relé | Bomba de irrigação | GPIO 12 | Liga/desliga automaticamente |
| LED | Status da irrigação | GPIO 13 | Aceso = bomba ativa |

## Conversão de Lux para pH

A conversão de lux (intensidade de luz) para pH é simulada usando um sensor LDR. O valor analógico é lido com a função analogRead() e mapeado para a escala de pH (0 a 14) usando a fórmula:

```cpp
int luxValue = analogRead(34);  // Leitura do sensor LDR
float ph = ((float)luxValue / 4095.0) * 14.0;  // Conversão para pH
```

Essa conversão é baseada na interpolação proporcional, considerando que valores mais altos de lux indicam um solo mais básico (maior pH) e valores mais baixos representam acidez (menor pH).

## Funcionamento geral

- A cada ciclo (10 minutos), o sistema:
  - Lê a umidade via DHT22.
  - Lê a presença de fósforo e potássio via botões.
  - Lê o pH do solo via sensor LDR (lux convertido para escala de pH).
  - Decide acionar ou desligar a bomba de irrigação conforme a lógica implementada.
  - Atualiza o status do LED vermelho conforme a irrigação ativa ou inativa.

## Demonstração do uso do Serial Plotter

![Circuito no Wokwi com serial potter](../../assets/circuito-com-serial-plotter-1.jpeg)

![Circuito no Wokwi com serial potter 2](../../assets/circuito-com-serial-plotter-2.jpeg)

## Lógica de controle da irrigação - Embasamento técnico

A decisão de irrigar ou não foi baseada em materiais técnicos reais:

- [Fonte 1 - Efeito do pH na disponibilidade de nutrientes](https://www.scielo.br/j/eagri/a/339msPdHQFSWwbrsNsPn7QM/)
- [Fonte 2 - Relação entre pH e Fósforo no solo](https://www.scielo.br/j/rbeaa/a/sPdhtHwBDqMWxn5p53hV46s)
- [Fonte 3 - Manual de Irrigação por Tangerino](https://www2.feis.unesp.br/irrigacao/pdf/conird2005_tangerino.pdf)

Com base nas leituras, define-se:

### **Cenários para ativação da irrigação**

- **Umidade do solo abaixo de 40%** e **presença de fósforo** ➔ Necessidade de água para absorção eficiente de nutrientes.
- **pH do solo entre 6,2 e 6,8** ➔ Faixa ideal para disponibilidade de fósforo, combinada com baixa umidade.

### **Cenários para desligamento da irrigação**

- **Umidade do solo acima de 70%** ➔ Evitar saturação do solo e lixiviação de nutrientes.
- **pH fora da faixa ideal** (abaixo de 5,5 ou acima de 7,0) ➔ Disponibilidade de nutrientes é reduzida.

## Lógica de Irrigação

A lógica considera tanto **dados dos sensores físicos** quanto **dados externos vindos do clima**:

### Sensores locais:

- Fósforo presente (botão)
- Potássio presente (botão)
- pH do solo (LDR convertido)
- Umidade do solo (DHT22)

### Dados climáticos externos (vindos do Python via JSON):

- `temperature`: Temperatura ambiente
- `air_humidity`: Umidade do ar
- `rain_forecast`: Previsão de chuva (booleano)

### Regras de decisão:

1. **Não irrigar** se `rain_forecast = true`
2. **Irrigar** se umidade < 40% **e** fósforo presente
3. **Não irrigar** se potássio presente **e** umidade > 60%
4. **Cancelar irrigação** se pH fora da faixa ideal (5.5 a 7.0)
5. **Nunca irrigar** se umidade > 70%
6. **Irrigar** se faltar fósforo ou potássio **e** umidade entre 30% e 50%

## Integração com API Climática (Ir Além 2)

Este projeto simula o uso de dados reais obtidos da **API OpenWeatherMap**.  
Um script Python busca dados da cidade configurada (`.env`) e envia ao ESP32 via porta serial ou arquivo `climate.json`.

### Exemplo de JSON enviado:

```json
{
  "temperature": 22.5,
  "air_humidity": 75.0,
  "rain_forecast": true
}
```

Esses dados são interpretados no setup() do C++ e usados para tomar decisões no loop().

## Testando Dados Climáticos Simulados

Para simular diferentes condições climáticas, você pode alterar diretamente o conteúdo do JSON usado no código main.cpp. Por padrão, o código usa os seguintes dados:

```cpp
String climate_json = "{\"temperature\": 22.5, \"air_humidity\": 75.0, \"rain_forecast\": false}";
```

Se quiser testar diferentes cenários, como simular presença de chuva ou mudanças na temperatura e umidade do ar, altere esse trecho para refletir os novos dados, por exemplo:

```cpp
 String climate_json = "{\"temperature\": 30.0, \"air_humidity\": 40, \"rain_forecast\": true}";
```

Depois de fazer essa alteração, carregue o código novamente no ESP32 para aplicar as novas condições. Lembre-se de que o sistema de irrigação toma decisões com base nesses dados, como:

- Previsão de Chuva (`rain_forecast`): Se verdadeiro, a irrigação é cancelada.
- Temperatura (`temperature`): Apenas exibida no monitor serial.
- Umidade do Ar (`air_humidity`): Apenas exibida no monitor serial.

## Simulações sugeridas

- Pressionar apenas o botão de fósforo com umidade baixa → irrigação deve ocorrer
- Desmarcar fósforo e potássio com umidade entre 30–50% → irrigação ocorre
- Simular rain_forecast: true no JSON → irrigação deve ser cancelada
- Forçar pH fora do ideal (ex: < 5.5 ou > 7.0) → irrigação não ocorre

## Sobre a simulação Wokwi

Como o projeto utiliza o simulador Wokwi, não é possível realizar integração real com o script Python ou com banco de dados via porta serial.

Por isso, os dados climáticos são simulados diretamente como uma string JSON no código C++, representando o que seria enviado em um cenário real:

```cpp
String climate_json = "{\"temperature\": 22.5, \"air_humidity\": 75.0, \"rain_forecast\": true}";
```

Em um cenário real (com ESP32 físico):
O script Python enviaria o JSON via pyserial

O ESP32 leria os dados com Serial.readStringUntil('\n')

A integração seria em tempo real com banco de dados e decisões automáticas

## Observações

- A conversão de lux para pH foi feita de forma simulada usando interpolação proporcional (`analogRead` mapeado para escala de pH 0–14).
- O sistema foi programado para ser robusto mesmo em variações abruptas de leitura simulada.
- As decisões foram embasadas em artigos técnicos agrícolas e guias acadêmicos para reforçar a lógica implementada.

## ❌ Possíveis Problemas e Soluções

Problema: `command not found: pio`

Se você já instalou o PlatformIO no VSCode mas ainda assim recebe a mensagem command not found: pio ao tentar executar comandos no terminal, o problema pode ser que o PATH do seu sistema não inclui o diretório correto.

Verifique se o PlatformIO está acessível:

```bash
which pio
```

Se não encontrar nada, adicione o caminho manualmente ao seu arquivo de configuração do terminal (por exemplo, ~/.zshrc no macOS):

```bash
echo 'export PATH=$HOME/.platformio/penv/bin:$PATH' >> ~/.zshrc
source ~/.zshrc
```

Alternativamente, você pode criar um link simbólico para garantir que o comando esteja acessível:

```nash
sudo ln -s ~/.platformio/penv/bin/pio /usr/local/bin/pio
```

Se ainda não funcionar, tente reinstalar o PlatformIO via pip:

```bash
python3 -m pip install platformio
```

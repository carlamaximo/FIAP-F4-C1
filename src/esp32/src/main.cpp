#include <Arduino.h>
#include "DHT.h"
#include <ArduinoJson.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// ===== OTIMIZAÇÕES DE MEMÓRIA - FASE 4 =====
// Uso de tipos de dados otimizados para economizar RAM
// uint8_t em vez de int para valores pequenos
// float mantido apenas onde necessário para precisão
// const para strings constantes (economiza RAM)

// Definições de pinos com tipos otimizados
const uint8_t PHOSPHORUS_PIN = 14;     // Botão simulando presença de fósforo
const uint8_t POTASSIUM_PIN = 4;       // Botão simulando presença de potássio
const uint8_t PH_SENSOR_PIN = 34;      // LDR simulando o sensor de pH
const uint8_t DHT_PIN = 5;             // Pino de dados do DHT22 (umidade)
const uint8_t RELAY_PIN = 12;          // Controle do relé (bomba de irrigação)
const uint8_t LED_PIN = 13;            // LED de status

// Configuração do sensor DHT
#define DHTTYPE DHT22
DHT dht(DHT_PIN, DHTTYPE);

// ===== DISPLAY LCD I2C - NOVA FUNCIONALIDADE FASE 4 =====
// Display LCD 16x2 via I2C (endereço padrão 0x27)
LiquidCrystal_I2C lcd(0x27, 16, 2);

// ===== VARIÁVEIS OTIMIZADAS - FASE 4 =====
// Uso de tipos menores para economizar RAM
float humidity = 0.0f;                 // Mantido float para precisão
float ph = 0.0f;                       // Mantido float para precisão
bool phosphorus_present = false;       // bool é mais eficiente que int
bool potassium_present = false;        // bool é mais eficiente que int
bool rain_forecast = false;            // bool é mais eficiente que int
float air_humidity = 0.0f;             // Mantido float para precisão
float temperature = 0.0f;              // Mantido float para precisão
bool irrigate = false;                 // bool para decisão de irrigação

// ===== CONTADORES PARA SERIAL PLOTTER - FASE 4 =====
uint32_t loop_counter = 0;             // Contador de loops para Serial Plotter
const uint32_t PLOT_INTERVAL = 1000;   // Intervalo para plot (1 segundo)

// ===== CONSTANTES PARA ECONOMIZAR RAM - FASE 4 =====
const char* MSG_INIT = "Sistema iniciado";
const char* MSG_IRRIGATION_ON = "IRRIGACAO: ON";
const char* MSG_IRRIGATION_OFF = "IRRIGACAO: OFF";
const char* MSG_RAIN_FORECAST = "CHUVA PREVISTA";

void setup() {
  Serial.begin(115200);

  // Configuração dos pinos
  pinMode(PHOSPHORUS_PIN, INPUT_PULLUP);
  pinMode(POTASSIUM_PIN, INPUT_PULLUP);
  pinMode(PH_SENSOR_PIN, INPUT);
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);

  // Inicialização do sensor DHT
  dht.begin();
  
  // ===== INICIALIZAÇÃO DO DISPLAY LCD - FASE 4 =====
  Wire.begin();
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("FarmTech v4.0");
  lcd.setCursor(0, 1);
  lcd.print("Inicializando...");
  
  digitalWrite(RELAY_PIN, LOW);

  delay(100);
  Serial.println(MSG_INIT);

  // ===== CABEÇALHO PARA SERIAL PLOTTER - FASE 4 =====
  Serial.println("Umidade_Solo,Temperatura,Umidade_Ar,pH,Irrigacao");

  // Simula dados climáticos vindos de script Python (como se fossem enviados via porta serial)
  String climate_json = "{\"temperature\": 22.5, \"air_humidity\": 75.0, \"rain_forecast\": false}";

  // Parseia os dados recebidos
  StaticJsonDocument<200> doc;
  DeserializationError error = deserializeJson(doc, climate_json);

  if (error) {
    Serial.println("Erro ao ler dados climaticos externos. Usando apenas sensores locais.");
    Serial.println(error.c_str());
  } else {
    temperature = doc["temperature"];
    air_humidity = doc["air_humidity"];
    rain_forecast = doc["rain_forecast"];

    Serial.print("Temperatura externa: ");
    Serial.println(temperature);
    Serial.print("Umidade do ar: ");
    Serial.println(air_humidity);
    Serial.print("Previsao de chuva: ");
    Serial.println(rain_forecast ? "Sim" : "Nao");
  }
  
  // Aguarda 2 segundos antes de começar
  delay(2000);
  lcd.clear();
}

void loop() {
  // ===== LEITURA DOS SENSORES - OTIMIZADA FASE 4 =====
  // Leitura dos botões: pressionado = presença detectada
  phosphorus_present = (digitalRead(PHOSPHORUS_PIN) == LOW);
  potassium_present = (digitalRead(POTASSIUM_PIN) == LOW);

  // Leitura do pH via LDR (simulado) - otimizada
  uint16_t ldr_value = analogRead(PH_SENSOR_PIN);  // uint16_t em vez de int
  ph = ((float)ldr_value / 4095.0f) * 14.0f;      // Converte o valor da LDR para a escala de pH

  // Leitura da umidade do solo
  humidity = dht.readHumidity();

  // ===== LÓGICA DE DECISÃO DE IRRIGAÇÃO - OTIMIZADA FASE 4 =====
  irrigate = false;  // Reset da decisão

  // 1. Não irrigar se houver previsão de chuva detectada
  if (rain_forecast) {
    Serial.println(MSG_RAIN_FORECAST);
    irrigate = false;
  } else {
    // 2. Irrigar se umidade < 40% e fósforo presente
    if (humidity < 40.0f && phosphorus_present) {
      irrigate = true;
    }
    
    // 3. Não irrigar se potássio presente e umidade > 60%
    if (potassium_present && humidity > 60.0f) {
      irrigate = false;
    }
    
    // 4. Irrigar apenas se pH estiver entre 5.5 e 7.0 (faixa ótima)
    if (humidity < 40.0f && (ph < 5.5f || ph > 7.0f)) {
      irrigate = false;
    }
    
    // 5. Nunca irrigar se umidade > 70%
    if (humidity > 70.0f) {
      irrigate = false;
    }
    
    // 6. Irrigar se faltar fósforo ou potássio, mas com umidade entre 30% e 50%
    if ((!phosphorus_present || !potassium_present) && (humidity >= 30.0f && humidity <= 50.0f)) {
      irrigate = true;
    }
  }

  // ===== CONTROLE DA BOMBA E LED - FASE 4 =====
  if (irrigate) {
    digitalWrite(RELAY_PIN, HIGH);
    digitalWrite(LED_PIN, HIGH); 
    Serial.println(MSG_IRRIGATION_ON);
  } else {
    digitalWrite(RELAY_PIN, LOW);
    digitalWrite(LED_PIN, LOW); 
    Serial.println(MSG_IRRIGATION_OFF);
  }

  // ===== ATUALIZAÇÃO DO DISPLAY LCD - FASE 4 =====
  lcd.clear();
  
  // Linha 1: Umidade e Temperatura
  lcd.setCursor(0, 0);
  lcd.print("U:");
  lcd.print(humidity, 1);
  lcd.print("% T:");
  lcd.print(temperature, 1);
  lcd.print("C");
  
  // Linha 2: pH e Status de Irrigação
  lcd.setCursor(0, 1);
  lcd.print("pH:");
  lcd.print(ph, 1);
  lcd.print(" ");
  if (irrigate) {
    lcd.print("ON ");
  } else {
    lcd.print("OFF");
  }
  
  // Indicadores de nutrientes (usando caracteres especiais se disponíveis)
  if (phosphorus_present) {
    lcd.print(" P");
  }
  if (potassium_present) {
    lcd.print(" K");
  }

  // ===== SERIAL PLOTTER - FASE 4 =====
  // Envia dados formatados para o Serial Plotter a cada segundo
  if (loop_counter % PLOT_INTERVAL == 0) {
    // Formato: Umidade_Solo,Temperatura,Umidade_Ar,pH,Irrigacao
    Serial.print(humidity);
    Serial.print(",");
    Serial.print(temperature);
    Serial.print(",");
    Serial.print(air_humidity);
    Serial.print(",");
    Serial.print(ph);
    Serial.print(",");
    Serial.println(irrigate ? 1 : 0);
  }

  // ===== EXIBIÇÃO DETALHADA NO MONITOR SERIAL - FASE 4 =====
  // Exibe as leituras no monitor serial (a cada 10 loops para não sobrecarregar)
  if (loop_counter % 10 == 0) {
    Serial.print("Umidade: ");
    Serial.print(humidity);
    Serial.print("% | Fosforo: ");
    Serial.print(phosphorus_present ? "Presente" : "Ausente");
    Serial.print(" | Potassio: ");
    Serial.print(potassium_present ? "Presente" : "Ausente");
    Serial.print(" | pH: ");
    Serial.println(ph, 1);
  }

  loop_counter++;  // Incrementa o contador de loops
  
  // Aguarda 10 minutos antes da próxima leitura
  delay(600000); // 10 minutos = 600.000 ms
}
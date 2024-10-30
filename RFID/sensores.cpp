const int TRIG_PINS[] = {3, 4, 5};           // Pinos Trig dos sensores ultrassônicos
const int ECHO_PINS[] = {6, 7, 8};           // Pinos Echo dos sensores ultrassônicos
const int LED_VERDE_PINS[] = {9, 10, 11};    // Pinos dos LEDs verdes
const int LED_VERMELHO_PINS[] = {12, 13, A0}; // Pinos dos LEDs vermelhos

void setup() {
  Serial.begin(9600);

  // Configura pinos TRIG como saída
  for (int i = 0; i < 3; i++) {
    pinMode(TRIG_PINS[i], OUTPUT);
    pinMode(ECHO_PINS[i], INPUT);
    pinMode(LED_VERDE_PINS[i], OUTPUT);
    pinMode(LED_VERMELHO_PINS[i], OUTPUT);
  }
}

long medirDistancia(int trigPin, int echoPin) {
  // Envia um pulso curto de 10 microsegundos
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Lê a duração do pulso no pino ECHO
  long duracao = pulseIn(echoPin, HIGH);
  long distancia = duracao * 0.034 / 2;  // Calcula a distância em cm

  return distancia;
}

void loop() {
  for (int i = 0; i < 3; i++) {
    long distancia = medirDistancia(TRIG_PINS[i], ECHO_PINS[i]);
    Serial.print("Sensor ");
    Serial.print(i + 1);
    Serial.print(" - Distância: ");
    Serial.print(distancia);
    Serial.println(" cm");

    // Aciona LEDs com base na presença
    if (distancia < 30) {  // Distância para presença detectada
      digitalWrite(LED_VERDE_PINS[i], HIGH);
      digitalWrite(LED_VERMELHO_PINS[i], LOW);
      Serial.print("Sensor ");
      Serial.print(i + 1);
      Serial.println(" - Presença detectada - LED Verde ON");
    } else {
      digitalWrite(LED_VERDE_PINS[i], LOW);
      digitalWrite(LED_VERMELHO_PINS[i], HIGH);
      Serial.print("Sensor ");
      Serial.print(i + 1);
      Serial.println(" - Ausência detectada - LED Vermelho ON");
    }
  }
  delay(5000);  // Intervalo entre leituras
}


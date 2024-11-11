const int TOTAL_SENSORES = 3; // Total de sensores
const int TRIG_PINS[] = {3, 4, 5};
const int ECHO_PINS[] = {6, 7, 8};
const int LED_VERDE_PINS[] = {9, 10, 11};
const int LED_VERMELHO_PINS[] = {12, 13, A0};
const int DISTANCIA_THRESHOLD = 10; // Limite para detecção de presença

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < TOTAL_SENSORES; i++) {
    pinMode(TRIG_PINS[i], OUTPUT);
    pinMode(ECHO_PINS[i], INPUT);
    pinMode(LED_VERDE_PINS[i], OUTPUT);
    pinMode(LED_VERMELHO_PINS[i], OUTPUT);
  }
}

long medirDistancia(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long duracao = pulseIn(echoPin, HIGH);
  return duracao * 0.034 / 2; // Distância em cm
}

void controlarLEDs(int indiceSensor, bool presencaDetectada) {
  if (presencaDetectada) {
    digitalWrite(LED_VERDE_PINS[indiceSensor], LOW);
    digitalWrite(LED_VERMELHO_PINS[indiceSensor], HIGH);
  } else {
    digitalWrite(LED_VERDE_PINS[indiceSensor], HIGH);
    digitalWrite(LED_VERMELHO_PINS[indiceSensor], LOW);
  }
}

void enviarDadosParaPython(int sensoresAtivos) {
  int sensoresInativos = TOTAL_SENSORES - sensoresAtivos;
  Serial.println(sensoresInativos);
}


void loop() {
 
  int sensoresAtivos = 0; // Reseta o contador de sensores ativos para calcular novamente

  for (int i = 0; i < TOTAL_SENSORES; i++) {
    long distancia = medirDistancia(TRIG_PINS[i], ECHO_PINS[i]);
    Serial.print("Sensor ");
    Serial.print(i + 1);
    Serial.print(" - Distância: ");
    Serial.print(distancia);
    Serial.println(" cm");

    bool presencaDetectada = (distancia < DISTANCIA_THRESHOLD);
    if (presencaDetectada) {
      sensoresAtivos++;
    }

    controlarLEDs(i, presencaDetectada);
  }

  enviarDadosParaPython(sensoresAtivos);

  delay(5000); // Atraso antes da próxima leitura
}


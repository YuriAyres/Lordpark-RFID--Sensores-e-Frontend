const int TOTAL_SENSORES = 3; // Total de sensores
const int TRIG_PINS[] = {3, 4, 5};
const int ECHO_PINS[] = {6, 7, 8};
const int LED_VERDE_PINS[] = {9, 10, 11};
const int LED_VERMELHO_PINS[] = {12, 13, A0};
const int DISTANCIA_THRESHOLD = 30; // Limite para detecção de presença

bool estadosSensores[TOTAL_SENSORES] = {false, false, false}; // Array para armazenar o estado de cada sensor
int sensoresAtivos = 0; // Contador de sensores detectando presença

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
    digitalWrite(LED_VERDE_PINS[indiceSensor], HIGH);
    digitalWrite(LED_VERMELHO_PINS[indiceSensor], LOW);
  } else {
    digitalWrite(LED_VERDE_PINS[indiceSensor], LOW);
    digitalWrite(LED_VERMELHO_PINS[indiceSensor], HIGH);
  }
}

void enviarDadosParaAPI(int sensoresAtivos) {
  // Aqui você deve implementar a lógica para enviar dados para sua API.
  // Exemplo:
  Serial.print("Sensores Ativos: ");
  Serial.println(sensoresAtivos);
}

void loop() {
  int sensoresAtivosAnterior = sensoresAtivos; // Guarda o valor anterior

  sensoresAtivos = 0; // Reseta o contador de sensores ativos para calcular novamente

  for (int i = 0; i < TOTAL_SENSORES; i++) {
    long distancia = medirDistancia(TRIG_PINS[i], ECHO_PINS[i]);
    Serial.print("Sensor ");
    Serial.print(i + 1);
    Serial.print(" - Distância: ");
    Serial.print(distancia);
    Serial.println(" cm");

    bool presencaDetectada = (distancia < DISTANCIA_THRESHOLD);
    if (presencaDetectada && !estadosSensores[i]) {
      // Se o sensor detectar presença e não estava ativo, atualiza
      estadosSensores[i] = true;
      sensoresAtivos++;
    } else if (!presencaDetectada && estadosSensores[i]) {
      // Se o sensor não detectar mais presença e estava ativo, atualiza
      estadosSensores[i] = false;
      sensoresAtivos--;
    }

    controlarLEDs(i, presencaDetectada);
  }

  // Envia os dados para a API sempre que houver uma alteração
  if (sensoresAtivos != sensoresAtivosAnterior) {
    enviarDadosParaAPI(TOTAL_SENSORES - sensoresAtivos);
  }

  delay(5000); // Atraso antes da próxima leitura
}


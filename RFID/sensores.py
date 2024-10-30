import RPi.GPIO as GPIO
import time
import signal
import sys

# Configurações de hardware
GPIO.setmode(GPIO.BOARD)
TRIG_PINS = [18, 16, 12]
ECHO_PINS = [24, 26, 22]
LED_VERDE_PINS = [20, 19, 13]
LED_VERMELHO_PINS = [21, 17, 27]

for pin in TRIG_PINS:
    GPIO.setup(pin, GPIO.OUT)
for pin in ECHO_PINS:
    GPIO.setup(pin, GPIO.IN)
for pin in LED_VERDE_PINS + LED_VERMELHO_PINS:
    GPIO.setup(pin, GPIO.OUT)

def medir_distancia(trig_pin, echo_pin):
    # Envia o pulso de trigger
    GPIO.output(trig_pin, True)
    time.sleep(0.00001)
    GPIO.output(trig_pin, False)

    # Calcula o tempo de ida e volta do sinal ultrassônico
    while GPIO.input(echo_pin) == 0:
        inicio = time.time()
    while GPIO.input(echo_pin) == 1:
        fim = time.time()

    duracao = fim - inicio
    distancia = (duracao * 34300) / 2  # velocidade do som (34300 cm/s)

    return distancia

# Função para finalizar o programa
def finalizar_programa(signal, frame):
    print("\nFinalizando o programa...")
    GPIO.cleanup()
    sys.exit(0)

# Captura o sinal de interrupção (CTRL+C)
signal.signal(signal.SIGINT, finalizar_programa)

# Loop principal
try:
    while True:
       for i in range(3):
            distancia = medir_distancia(TRIG_PINS[i], ECHO_PINS[i])
            print(f"Sensor {i + 1} - Distância: {distancia:.2f} cm")

            # Aciona LEDs com base na presença
            if distancia < 30:  # Ajuste para a distância desejada em cm
                GPIO.output(LED_VERDE_PINS[i], True)
                GPIO.output(LED_VERMELHO_PINS[i], False)
                print(f"Sensor {i + 1} - Presença detectada - LED Verde ON")
            else:
                GPIO.output(LED_VERDE_PINS[i], False)
                GPIO.output(LED_VERMELHO_PINS[i], True)
                print(f"Sensor {i + 1} - Ausência detectada - LED Vermelho ON")

            time.sleep(5)  # Define o intervalo entre as leituras

finally:
    GPIO.cleanup()


import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep
import signal
import sys
import requests
import spidev

# Configurações de hardware
GPIO.setmode(GPIO.BOARD)
BUZZER = 38
CS_ENTRADA = 8  # CS do leitor de entrada
CS_SAIDA = 22   # CS do leitor de saída
SERVO_ENTRADA_PIN = 10  # Pino do servo da cancela de entrada
SERVO_SAIDA_PIN = 12    # Pino do servo da cancela de saída

GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(CS_ENTRADA, GPIO.OUT)
GPIO.setup(CS_SAIDA, GPIO.OUT)

# Configuração do PWM para os servos
GPIO.setup(SERVO_ENTRADA_PIN, GPIO.OUT)
GPIO.setup(SERVO_SAIDA_PIN, GPIO.OUT)
servoEntrada = GPIO.PWM(SERVO_ENTRADA_PIN, 50)  # Frequência de 50Hz
servoSaida = GPIO.PWM(SERVO_SAIDA_PIN, 50)      # Frequência de 50Hz
servoEntrada.start(0)  # Inicializa em 0 graus
servoSaida.start(0)    # Inicializa em 0 graus

# Configuração da SPI e inicialização do leitor
spi = spidev.SpiDev()
spi.open(0, 0)  # Canal SPI 0, dispositivo 0
spi.max_speed_hz = 1000000
leitorRFID = SimpleMFRC522()

# URL da API
URL_API = "http://10.1.24.62:5000"

# Funções para o buzzer
def tocar_buzzer(frequencia, duracao):
    p = GPIO.PWM(BUZZER, frequencia)
    p.start(50)
    sleep(duracao)
    p.stop()

def buzzer_leitura_feita():
    tocar_buzzer(500, 0.5)

def buzzer_erro():
    tocar_buzzer(200, 0.5)

def buzzer_sucesso():
    tocar_buzzer(1000, 0.5)

# Função para abrir e fechar a cancela
def abrir_cancela(servo):
    servo.ChangeDutyCycle(7)  # Ajuste para abrir (aproximadamente 90 graus)
    sleep(5)  # Aguarda 5 segundos para fechar
    servo.ChangeDutyCycle(0)  # Para o PWM (cancela fecha)
    sleep(1)  # Aguarda um segundo antes de permitir o próximo movimento

# Função para finalizar o programa
def finalizar_programa(signal, frame):
    print("\nFinalizando o programa...")
    servoEntrada.stop()  # Para o PWM do servo de entrada
    servoSaida.stop()    # Para o PWM do servo de saída
    GPIO.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, finalizar_programa)

# Função para leitura com alternância de leitores
def ler_tag(cs_pin):
    # Ativar CS do leitor desejado
    GPIO.output(cs_pin, GPIO.LOW)
    sleep(0.1)  # Pequeno delay para estabilizar

    # Leitura
    try:
        tag_id, _ = leitorRFID.read()
        buzzer_leitura_feita()
        return int(tag_id)
    except Exception as e:
        print(f"Erro ao ler o RFID: {e}")
        buzzer_erro()
    finally:
        # Desativar CS após leitura
        GPIO.output(cs_pin, GPIO.HIGH)

    return None

# Funções de processamento para entrada e saída
def processar_entrada(tag):
    response = requests.get(f"{URL_API}/carros/{tag}")
    if response.status_code == 200:
        carro = response.json()
        placa = carro.get('placa')
        if placa:
            buzzer_sucesso()
            abrir_cancela(servoEntrada)  # Abre a cancela de entrada
            response = requests.post(f"{URL_API}/estacionar", json={'carro_id': tag, 'placa': placa})
            if response.status_code == 200:
                print("Veículo registrado com sucesso na entrada.")
            else:
                print("Erro ao registrar entrada.")
                buzzer_erro()
        else:
            print("ID não reconhecido.")
            buzzer_erro()
    else:
        print("Erro ao buscar dados do carro.")
        buzzer_erro()

def processar_saida(tag):
    response = requests.get(f"{URL_API}/carros/{tag}")
    if response.status_code == 200:
        carro = response.json()
        placa = carro.get('placa')
        if placa:
            buzzer_sucesso()
            abrir_cancela(servoSaida)  # Abre a cancela de saída
            response = requests.post(f"{URL_API}/sair", json={'carro_id': tag, 'placa': placa})
            if response.status_code == 200:
                print("Saída registrada com sucesso.")
            else:
                print("Erro ao registrar saída.")
                buzzer_erro()
        else:
            print("ID não reconhecido.")
            buzzer_erro()
    else:
        print("Erro ao buscar dados do carro.")
        buzzer_erro()

# Loop principal
try:
    while True:
        print("Aguardando leitura na entrada...")
        tagEntrada = ler_tag(CS_ENTRADA)
        if tagEntrada:
            processar_entrada(tagEntrada)

        print("Aguardando leitura na saída...")
        tagSaida = ler_tag(CS_SAIDA)
        if tagSaida:
            processar_saida(tagSaida)

        sleep(1)

finally:
    GPIO.cleanup()



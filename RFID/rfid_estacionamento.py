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
GPIO.setup(BUZZER, GPIO.OUT)

# Função modificada para inicializar leitores RFID com pinos CS específicos
class SimpleMFRC522Custom(SimpleMFRC522):
    def __init__(self, cs_pin):
        self.spi = spidev.SpiDev()
        self.spi.open(0, cs_pin)  # Abra o SPI no pino CS correspondente
        self.spi.max_speed_hz = 1000000
        super().__init__()

# Iniciar os leitores RFID
leitorEntrada = SimpleMFRC522Custom(cs_pin=8)  # Leitor de Entrada (CS 0)
leitorSaida = SimpleMFRC522Custom(cs_pin=22)    # Leitor de Saída (CS 1)

# URL da API (ajuste para o endereço correto do servidor)
URL_API = "http://10.1.24.62:5000"

# Funções para o buzzer
def tocar_buzzer(frequencia, duracao):
    p = GPIO.PWM(BUZZER, frequencia)
    p.start(50)  # Duty cycle de 50%
    sleep(duracao)
    p.stop()

def buzzer_leitura_feita():
    tocar_buzzer(500, 0.5)

def buzzer_erro():
    tocar_buzzer(200, 0.5)

def buzzer_sucesso():
    tocar_buzzer(1000, 0.5)

# Função para finalizar o programa
def finalizar_programa(signal, frame):
    print("\nFinalizando o programa...")
    GPIO.cleanup()
    sys.exit(0)

# Captura o sinal de interrupção (CTRL+C)
signal.signal(signal.SIGINT, finalizar_programa)

# Função para manipular a entrada de veículo
def processar_entrada(tag):
    response = requests.get(f"{URL_API}/carros/{tag}")
    if response.status_code == 200:
        carro = response.json()
        placa = carro.get('placa')
        if placa:
            buzzer_sucesso()
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

# Função para manipular a saída de veículo
def processar_saida(tag):
    response = requests.get(f"{URL_API}/carros/{tag}")
    if response.status_code == 200:
        carro = response.json()
        placa = carro.get('placa')
        if placa:
            buzzer_sucesso()
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
        tagEntrada, _ = leitorEntrada.read()
        tagEntrada = int(tagEntrada)
        buzzer_leitura_feita()
        processar_entrada(tagEntrada)

        print("Aguardando leitura na saída...")
        tagSaida, _ = leitorSaida.read()
        tagSaida = int(tagSaida)
        buzzer_leitura_feita()
        processar_saida(tagSaida)

        sleep(1)

finally:
    GPIO.cleanup()

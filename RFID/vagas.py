import serial
import requests

port = '/dev/ttyUSB0'  # Altere conforme necessário
baudrate = 9600
URL_API = "http://10.1.24.62:5000"

with serial.Serial(port, baudrate, timeout=1) as ser:
    while True:
        linha = ser.readline().decode('utf-8').strip()
        if linha:
            try:
                sensores_inativos = int(linha)
                print(f"Número de sensores inativos: {sensores_inativos}")
                # Envio dos dados para a API
                response = requests.post(URL_API, json={'sensores_inativos': sensores_inativos})
                
                # Verifica a resposta da API
                if response.status_code == 200:
                    print("Dados enviados com sucesso!")
                else:
                    print(f"Erro ao enviar dados: {response.status_code}, {response.text}")
            except ValueError:
                print("Erro ao converter para inteiro.")

            

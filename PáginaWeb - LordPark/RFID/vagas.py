import serial
import requests

port = '/dev/ttyUSB0'
baudrate = 9600
URL_API = "http://10.1.24.62:5000"

with serial.Serial(port, baudrate, timeout=1) as ser:
    while True:
        linha = ser.readline().decode('utf-8').strip()
        if linha:
            try:
                sensores_inativos = int(linha)
                print(f"Número de sensores inativos: {sensores_inativos}")
                
                # Envio dos dados para a API com timeout e manuseio de exceções
                try:
                    response = requests.post(f"{URL_API}/vagas", json={'sensores_inativos': sensores_inativos}, timeout=5)
                    
                    # Verifica a resposta da API
                    if response.status_code == 200:
                        print("Dados enviados com sucesso!")
                    else:
                        print(f"Erro ao enviar dados: {response.status_code}, {response.text}")
                except requests.exceptions.RequestException as e:
                    print(f"Erro de conexão com a API: {e}")
            except ValueError:
                print("Erro ao converter para inteiro.")


            

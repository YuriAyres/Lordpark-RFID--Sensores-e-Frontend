import RPi.GPIO as GPIO
from mfrc522_custom import MFRC522Custom

leitorRFID_entrada = MFRC522Custom(bus=0, device=0)
leitorRFID_saida = MFRC522Custom(bus=1, device=0)

try:
    print("Aproxime o cartão no leitor de entrada")
    id_entrada, text_entrada = leitorRFID_entrada.read()
    print(f"Leitor de entrada: ID={id_entrada}, Texto={text_entrada}")

    print("Aproxime o cartão no leitor de saída")
    id_saida, text_saida = leitorRFID_saida.read()
    print(f"Leitor de saída: ID={id_saida}, Texto={text_saida}")

finally:
    leitorRFID_entrada.close()
    leitorRFID_saida.close()

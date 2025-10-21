import sounddevice as sd

DEVICE_ID = 13  # <<<--- Coloque o ID 13 aqui

print(f"--- Consultando informações do dispositivo de entrada ID {DEVICE_ID} ---")
try:
    device_info = sd.query_devices(DEVICE_ID, 'input')
    samplerate = device_info['default_samplerate']
    print(f"\n[ RESPOSTA ] A taxa de amostragem padrão é: {samplerate} Hz")
except Exception as e:
    print(f"\nOcorreu um erro: {e}")
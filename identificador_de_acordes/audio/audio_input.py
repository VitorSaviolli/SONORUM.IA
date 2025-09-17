import sounddevice as sd
import numpy as np
import sys

CHUNK = 1024
RATE = 44100
VOLUME_THRESHOLD = 0.01

# TO DO: Preciso captar exatamente o acorde e somente o acorde, e nao dividir em mais chunks que o necessario
def audio_stream_generator():
    with sd.InputStream(samplerate=RATE, channels=1, dtype='int16', blocksize=CHUNK) as stream:
        while True:
            y_raw, overflowed = stream.read(CHUNK)

            #converte e normaliza os dados 
            #sounddevice por retornar array > 1 dimensao
            y = y_raw.flatten().astype(np.float32) / 32768.0

            #calcula a intensidade do volume por RMS
            volume = np.sqrt(np.mean(y**2))

            #LINHA DE TESTE
            #print(f"Volume do chunk: {np.sqrt(np.mean(y**2)):.2f}")

            if volume > VOLUME_THRESHOLD:
                yield y, RATE

# -- TESTE DO LIMIAR DE VOLUME  (para ajustes) --

if __name__ == "__main__":
    print("Iniciando o teste de entrada de áudio.")
    print("Pressione Ctrl+C para parar.")

    try:
        for y, sr in audio_stream_generator():
            volume = np.sqrt(np.mean(y**2))
            print(f"Volume Detectado: {volume:.4f}")
    
    except KeyboardInterrupt:
        print("\nTeste finalizado.")
        sys.exit(0)

    
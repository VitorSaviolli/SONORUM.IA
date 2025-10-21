import sounddevice as sd
sd.default.device[0] = 13
import numpy as np
import sys
import collections

RATE = 48000  
CHUNK = 1024
VOLUME_THRESHOLD = 0.08 
SILENCE_CHUNKS = 10     
MIN_CHORDS_CHUNKS = 5    

def sound_event_generator():
    """
    Escuta o áudio e agrupa os chunks de som em "eventos" únicos,
    retornando pausadamente o áudio completo de cada evento.
    """
    silent_chunks_buffer = collections.deque(maxlen=SILENCE_CHUNKS)
    
    recording = False
    recorded_chunks = []

    with sd.InputStream(samplerate=RATE, channels=1, dtype='int16', blocksize=CHUNK) as stream:
        print("\nAguardando som...")
        while True:
            y_raw, _ = stream.read(CHUNK)
            y = y_raw.flatten().astype(np.float32) / 32768.0
            volume = np.sqrt(np.mean(y**2))

            is_loud = volume > VOLUME_THRESHOLD
            
            if not recording:
                if is_loud:
                    # Inicia a gravação.
                    print("Som detectado, gravando...")
                    recording = True
                    recorded_chunks.append(y)
            else:
                # aqui já está gravando
                recorded_chunks.append(y)
                silent_chunks_buffer.append(not is_loud)
                
                """ Se o buffer de silêncio estiver cheio e só tiver chunks silenciosos,
                 o som terminou."""
                if all(item == True for item in silent_chunks_buffer):
                    print("Som terminado. Processando...")
                    
                    # Verifica se a gravação é longa o suficiente para ser um acorde
                    if len(recorded_chunks) > MIN_CHORDS_CHUNKS:
                        # Concatena todos os chunks em um único array
                        full_audio = np.concatenate(recorded_chunks)
                        yield full_audio, RATE

                    # Reseta para o próximo evento
                    recording = False
                    recorded_chunks = []
                    silent_chunks_buffer.clear()
                    print("\nAguardando som...")


def audio_stream_generator_simples_para_teste():
    """função para teste de volume"""
    with sd.InputStream(samplerate=RATE, channels=1, dtype='int16', blocksize=CHUNK) as stream:
        while True:
            y_raw, _ = stream.read(CHUNK)
            y = y_raw.flatten().astype(np.float32) / 32768.0
            yield y, RATE

if __name__ == "__main__":
    print(f"Iniciando o teste de entrada de áudio (Device ID: {sd.default.device[0]}, Rate: {RATE}).")
    print(f"Threshold atual: {VOLUME_THRESHOLD}")

    try:
        for y, sr in audio_stream_generator_simples_para_teste(): 
            volume = np.sqrt(np.mean(y**2))
            # Mostra uma barra de volume simples
            print(f"\nVolume Detectado: {volume:.4f} {'#' * int(volume * 200)}", end='\r')
    
    except KeyboardInterrupt:
        print("\nTeste finalizado.")
        sys.exit(0)
    except Exception as e:
        print(f"\nErro ao iniciar stream: {e}")
        print("Verifique se o RATE e o Device ID estão corretos.")


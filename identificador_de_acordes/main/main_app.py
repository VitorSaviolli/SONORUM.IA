import sys
import numpy as np
import time

from identificador_de_acordes.audio.audio_input import audio_stream_generator
from identificador_de_acordes.audio.audio_processor import extract_chroma


# -- TESTANDO O INPUT DE AUDIO E CONVERSAO EM FREQUENCIAS --
if __name__ == "__main__":
    print("Iniciando a detecção de áudio em tempo real. Pressione Ctrl+C para parar.")

    try:
        for y, sr in audio_stream_generator():
            prominent_data = extract_chroma(y, sr)
            
            if prominent_data:
                print("--- Frequências e Intensidades Detectadas ---")
                for item in prominent_data:
                #teste do audio em tempo real
                    print(f"{item:.4f}", end = ' ')
            
    except KeyboardInterrupt:
        print("\nFinalizando o programa.")
        sys.exit(0)
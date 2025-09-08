import sys
import numpy as np

from identificador_de_acordes.audio.audio_input import audio_stream_generator
from identificador_de_acordes.audio.audio_processor import analyze_chord_frequencies


# -- TESTANDO O INPUT DE AUDIO E CONVERSAO EM FREQUENCIAS --
if __name__ == "__main__":
    print("Iniciando a detecção de áudio em tempo real. Pressione Ctrl+C para parar.")

    try:
        for y, sr in audio_stream_generator():
            prominent_data = analyze_chord_frequencies(y, sr)
            
            if prominent_data:
                print("--- Frequências e Intensidades Detectadas ---")
                for item in prominent_data:
                    frequency = item['frequency']
                    magnitude = item['magnitude']
                    print(f"Frequência: {frequency:.2f} Hz, Intensidade: {magnitude:.2f}")

    except KeyboardInterrupt:
        print("\nFinalizando o programa.")
        sys.exit(0)
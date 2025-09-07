import os
import numpy as np
import librosa
from identificador_de_acordes.audio.audio_processor import analyze_chord_frequencies

def get_reference_data(chords_dir="./data/chords"):
    reference_chords = {}
    print(f"procurando em {chords_dir}")

    if not os.path.isdir(chords_dir):
        print(f"Erro: O diretório '{chords_dir}' não foi encontrado.1")
    else:
        for filename in os.listdir(chords_dir):
            if filename.endswith(".wav"):
                file_path = os.path.join(chords_dir, filename)
                chord_name = os.path.splitext(filename)[0]
                #print(f"--- Analisando {filename} ---")
                y, sr = librosa.load(file_path, sr=None)

                prominent_data = analyze_chord_frequencies(y, sr)

                if prominent_data:
                    reference_chords[chord_name] = prominent_data

    return reference_chords

if __name__ == "__main__":

    reference_chords = get_reference_data()

    for chord_name in reference_chords:
        prominent_data_list = reference_chords[chord_name]
        print(f"--- Acorde: {chord_name} ---")
    
        for item in prominent_data_list:
            frequency = item['frequency']
            magnitude = item['magnitude']
            print(f"Frequência: {frequency:.2f} Hz, Intensidade: {magnitude:.2f}")
        
        print("\n")

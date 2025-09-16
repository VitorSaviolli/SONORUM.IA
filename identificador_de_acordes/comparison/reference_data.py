import os
import json
import numpy as np
import librosa
from identificador_de_acordes.audio.audio_processor import analyze_chord_frequencies

CHORDS_DIR = "./data/chords"
CHORDS_JSON = "./data/cache/chords.json"

def get_reference_data(chords_dir=CHORDS_DIR):
    reference_chords = {}
    print(f"Procurando em {chords_dir}")

    if not os.path.isdir(chords_dir):
        print(f"Erro: O diretório '{chords_dir}' não foi encontrado.")
    else:
        for filename in os.listdir(chords_dir):
            if filename.endswith(".wav"):
                file_path = os.path.join(chords_dir, filename)
                chord_name = os.path.splitext(filename)[0]
                
                # Carrega o áudio
                y, sr = librosa.load(file_path, sr=None)

                # Extrai as frequências dominantes
                prominent_data = analyze_chord_frequencies(y, sr)

                if prominent_data:
                    reference_chords[chord_name] = [
                        {
                            "frequency": float(item["frequency"]),
                            "magnitude": float(item["magnitude"])
                        }
                        for item in prominent_data
                    ]

    return reference_chords

def save_to_json(data, output_file=CHORDS_JSON):
    """
    Lê o JSON existente (se houver) e atualiza com os novos acordes processados.
    """
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = {}
    else:
        existing_data = {}

    # Atualiza o JSON com os novos acordes
    existing_data.update(data)

    # Salva no mesmo arquivo
    with open(output_file, "w") as f:
        json.dump(existing_data, f, indent=4)

    print(f"Acordes salvos/atualizados em {output_file}")


if __name__ == "__main__":
    # Processa os acordes a partir dos arquivos .wav
    reference_chords = get_reference_data()

    # Exibe no terminal
    for chord_name in reference_chords:
        prominent_data_list = reference_chords[chord_name]
        print(f"--- Acorde: {chord_name} ---")
    
        for item in prominent_data_list:
            frequency = item['frequency']
            magnitude = item['magnitude']
            print(f"Frequência: {frequency:.2f} Hz, Intensidade: {magnitude:.2f}")
        
        print("\n")

    # Salva no JSON
    save_to_json(reference_chords, CHORDS_JSON)

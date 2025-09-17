import os
import json
import numpy as np
import librosa
from identificador_de_acordes.audio.audio_processor import extract_chroma

CHORDS_DIR = "./data/chords"     
CHORDS_JSON = "./data/cache/chords.json"  

#Salva os arquivos em JSON
def save_to_json(data, output_file=CHORDS_JSON):
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    existing_data = {}
    if os.path.exists(output_file):
        try:
            with open(output_file, "r") as f:
                existing_data = json.load(f)
        except json.JSONDecodeError:
            existing_data = {}

    existing_data.update(data)

    with open(output_file, "w") as f:
        json.dump(existing_data, f, indent=4)

    print(f"\nBase de dados salva em: {output_file}")



def get_reference_data(chords_dir=CHORDS_DIR):
    reference_chords = {}
    print(f"Analisando acordes em: {chords_dir}")

    if not os.path.isdir(chords_dir):
        print(f"Erro: Diretório '{chords_dir}' não encontrado.")
        return reference_chords

    for filename in os.listdir(chords_dir):
        if filename.endswith(".wav"):
            file_path = os.path.join(chords_dir, filename)
            chord_name = os.path.splitext(filename)[0]  

            try:
                y, sr = librosa.load(file_path, sr=None)
                
                chroma_vector = extract_chroma(y, sr)
                
                reference_chords[chord_name] = [round(val, 4) for val in chroma_vector]
                print(f"  - Processado: {chord_name}")

            except Exception as e:
                print(f"  - Erro ao processar {filename}: {e}")
                
    return reference_chords

if __name__ == "__main__":
    reference_chords = get_reference_data()

    if reference_chords:
        save_to_json(reference_chords)

        print("\n--- Verificação dos Cromagramas ---")
        for chord_name, chroma_vector in reference_chords.items():
            print(f"Acorde: {chord_name}, Vetor: {np.round(chroma_vector, 3)}")
    else:
        print("Nenhum acorde processado.")
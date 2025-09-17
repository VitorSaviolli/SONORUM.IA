import os
import json
import numpy as np
import librosa

CHORDS_DIR = "./data/chords"     
CHORDS_JSON = "./data/cache/chords.json"  

def extract_chroma(y, sr):
    """Extrai e normaliza o cromagrama médio de um sinal de áudio."""
    # Extrai o cromagrama (12 classes de notas)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    
    # Calcula a média do croma ao longo do tempo
    chroma_mean = np.mean(chroma, axis=1)
    
    # Normaliza o vetor (L2-norm) para remover influência do volume
    norm = np.linalg.norm(chroma_mean)
    if norm > 0:
        chroma_norm = chroma_mean / norm
    else:
        chroma_norm = chroma_mean  
        
    return chroma_norm.tolist()

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
                
                # Reutiliza a função principal para extrair o croma normalizado
                chroma_vector = extract_chroma(y, sr)
                
                reference_chords[chord_name] = [round(val, 4) for val in chroma_vector]
                print(f"  - Processado: {chord_name}")

            except Exception as e:
                print(f"  - Erro ao processar {filename}: {e}")
                
    return reference_chords

def save_to_json(data, output_file=CHORDS_JSON):
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    existing_data = {}
    if os.path.exists(output_file):
        try:
            with open(output_file, "r") as f:
                existing_data = json.load(f)
        except json.JSONDecodeError:
            existing_data = {} # Trata caso de arquivo vazio/corrompido

    # Atualiza o dicionário com os novos dados
    existing_data.update(data)

    # Salva o resultado final no arquivo
    with open(output_file, "w") as f:
        json.dump(existing_data, f, indent=4)

    print(f"\nBase de dados salva em: {output_file}")

if __name__ == "__main__":
    # Gera os gabaritos a partir dos arquivos de áudio
    reference_chords = get_reference_data()

    # Salva os gabaritos no arquivo JSON se algum foi processado
    if reference_chords:
        save_to_json(reference_chords)

        print("\n--- Verificação dos Cromagramas ---")
        for chord_name, chroma_vector in reference_chords.items():
            print(f"Acorde: {chord_name}, Vetor: {np.round(chroma_vector, 3)}")
    else:
        print("Nenhum acorde processado.")
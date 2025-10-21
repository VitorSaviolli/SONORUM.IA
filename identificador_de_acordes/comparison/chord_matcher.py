import json
import numpy as np
from identificador_de_acordes.audio.audio_input import sound_event_generator
from identificador_de_acordes.audio.audio_processor import extract_chroma

CHORDS_JSON = "./data/cache/chords.json"
SIMILARITY_THRESHOLD = 0.85  # similaridade mínima esperada entre a entrada e o gabarito

def load_reference_chords(json_file=CHORDS_JSON):
    with open(json_file, "r") as f:
        return json.load(f)

def cosine_similarity(v1, v2):   # calcula a similaridade entre dois cromagramas
    v1 = np.array(v1)
    v2 = np.array(v2)
    if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0:
        return 0.0
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def identify_chord(y, sr, reference_chords):
    print("\n--- INICIANDO NOVA ANÁLISE ---")
    chroma_vector = extract_chroma(y, sr)
    if chroma_vector is None:
        return None, 0.0

    # Imprime o vetor do microfone para vermos como ele se parece
    print(f"Vetor do Microfone: {[round(n, 3) for n in chroma_vector]}")
    print("Comparando com a base de dados:")

    best_match = None
    best_similarity = -1
    all_similarities = {} # Para guardar todos os resultados

    for chord_name, ref_vector in reference_chords.items():
        sim = cosine_similarity(chroma_vector, ref_vector)
        all_similarities[chord_name] = sim # Guarda o resultado
        if sim > best_similarity:
            best_similarity = sim
            best_match = chord_name

    # Imprime a pontuação de TODOS os acordes, do melhor para o pior
    sorted_sims = sorted(all_similarities.items(), key=lambda item: item[1], reverse=True)
    for chord, sim in sorted_sims:
        print(f"  - {chord:<10}: {sim:.4f}")

    if best_similarity >= SIMILARITY_THRESHOLD:
        return best_match, best_similarity
    else:
        return None, best_similarity

if __name__ == "__main__": # aqui carregamos o gabarito, comparamos com a entrada e imprimimos se o acorde foi detectado
    print("Iniciando identificação de acordes em tempo real")
    reference_chords = load_reference_chords()

    try:
        for y, sr in sound_event_generator():
            chord, similarity = identify_chord(y, sr, reference_chords)

            if chord:
                print(f"Acorde detectado: {chord} (similaridade: {similarity:.4f})")
            else:
                print(f"Nenhum acorde identificado (similaridade máxima: {similarity:.4f})")

    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário.")

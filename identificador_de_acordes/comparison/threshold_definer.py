import os
import numpy as np
import librosa
from identificador_de_acordes.audio.audio_processor import extract_chroma
from identificador_de_acordes.comparison.chord_matcher import cosine_similarity, load_reference_chords  # supondo que essas já existam
# importando as funções de extração do cromagrama, similaridade de cossenos e dos dados de referência

CHORDS_DIR = "./data/chords"

def test_thresholds():
    reference_chords = load_reference_chords()
    correct_similarities = []
    incorrect_similarities = []

    print(f"Testando {len(reference_chords)} acordes de referência...\n")

    for filename in os.listdir(CHORDS_DIR): # percorre os acordes.wav
        if not filename.endswith(".wav"):
            continue

        chord_name = os.path.splitext(filename)[0]
        file_path = os.path.join(CHORDS_DIR, filename)

        y, sr = librosa.load(file_path, sr=None)
        chroma_vector = extract_chroma(y, sr) # extrai o cromagrama do acorde
        if chroma_vector is None:
            continue

        similarities = {}
        for ref_name, ref_vector in reference_chords.items():
            sim = cosine_similarity(chroma_vector, ref_vector) # aplica a similaridade de cossenos
            similarities[ref_name] = sim

        correct_sim = similarities.get(chord_name, 0)
        correct_similarities.append(correct_sim)

        max_incorrect = max(
            [v for k, v in similarities.items() if k != chord_name], default=0
        )
        incorrect_similarities.append(max_incorrect)

        print(f"{chord_name}: correto={correct_sim:.4f}, incorreto_max={max_incorrect:.4f}")

    mean_correct = np.mean(correct_similarities)
    mean_incorrect = np.mean(incorrect_similarities)
    suggested_threshold = (mean_correct + mean_incorrect) / 2

    print("\nEstatísticas:")
    print(f"Média (acordes corretos):   {mean_correct:.4f}")
    print(f"Média (acordes incorretos): {mean_incorrect:.4f}")
    print(f"\nThreshold sugerido: {suggested_threshold:.4f}")

if __name__ == "__main__":
    test_thresholds()

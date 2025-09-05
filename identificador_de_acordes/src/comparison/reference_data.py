import os
import librosa
import numpy as np

import os
import librosa
import numpy as np

def analyze_chord_frequencies(file_path):
    """
    Carrega um arquivo de áudio, realiza a Transformada de Fourier
    e retorna as frequências mais proeminentes.
    """
    # Define o limiar de magnitude para filtrar frequências irrelevantes
    MAGNITUDE_THRESHOLD = 0.3

    try:
        y, sr = librosa.load(file_path, sr=None)
        stft_output = librosa.stft(y)
        magnitudes = np.abs(stft_output)
        freq_bins = librosa.fft_frequencies(sr=sr)
        mean_magnitudes = np.mean(magnitudes, axis=1)

        max_magnitude = np.max(mean_magnitudes)
        if max_magnitude > 0:
            normalized_magnitudes = mean_magnitudes / max_magnitude
        else:
            normalized_magnitudes = mean_magnitudes
        
        # Filtra as frequências altas que são provavelmente harmônicos (acima de 800 Hz)
        max_freq_limit = 800

        prominent_indices = np.where(
            (normalized_magnitudes > MAGNITUDE_THRESHOLD) & (freq_bins < max_freq_limit))
        
        prominent_frequencies = freq_bins[prominent_indices]
        prominent_magnitudes = normalized_magnitudes[prominent_indices]

        prominent_data = []
        for i in range(len(prominent_frequencies)):
            prominent_data.append({
                'frequency': prominent_frequencies[i],
                'magnitude': prominent_magnitudes[i]
            })

        prominent_data.sort(key=lambda item: item['frequency'])

        return prominent_data

    except Exception as e:
        print(f"Erro ao processar o arquivo {os.path.basename(file_path)}: {e}")
        return None
    

if __name__ == "__main__":

    chords_dir = "./data/chords"
    
    print(f"procurando em {chords_dir}")

    if not os.path.isdir(chords_dir):
        print(f"Erro: O diretório '{chords_dir}' não foi encontrado.")
    else:
        for filename in os.listdir(chords_dir):
            if filename.endswith(".wav"):
                file_path = os.path.join(chords_dir, filename)
                print(f"--- Analisando {filename} ---")

                frequencies = analyze_chord_frequencies(file_path)

                if frequencies is not None:
                    for item in frequencies:
                        frequency = item['frequency']
                        magnitude = item['magnitude']
                        print(f"Frequência: {frequency:.2f} Hz, Intensidade: {magnitude:.2f}")
                    print("\n")

                    
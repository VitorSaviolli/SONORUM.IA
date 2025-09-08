import os
import librosa
import numpy as np

# Define o limiar de magnitude para filtrar frequências irrelevantes
MAGNITUDE_THRESHOLD = 0.5
# Filtra as frequências altas que são provavelmente harmônicos (acima de 800 Hz)
max_freq_limit = 800

def analyze_chord_frequencies(y, sr):
    """
    Realiza a Transformada de Fourier
    e retorna as frequências mais proeminentes.
    """
    try:
        stft_output = librosa.stft(y)
        magnitudes = np.abs(stft_output)
        freq_bins = librosa.fft_frequencies(sr=sr)
        mean_magnitudes = np.mean(magnitudes, axis=1)

        max_magnitude = np.max(mean_magnitudes)
        if max_magnitude > 0:
            normalized_magnitudes = mean_magnitudes / max_magnitude
        else:
            normalized_magnitudes = mean_magnitudes

        prominent_indices = np.where(
            (normalized_magnitudes > MAGNITUDE_THRESHOLD) & (freq_bins < max_freq_limit))
        
        prominent_frequencies = freq_bins[prominent_indices[0]]
        prominent_magnitudes = normalized_magnitudes[prominent_indices[0]]

        prominent_data = []
        for i in range(len(prominent_frequencies)):
            prominent_data.append({
                'frequency': prominent_frequencies[i],
                'magnitude': prominent_magnitudes[i]
            })

        prominent_data.sort(key=lambda item: item['frequency'])

        return prominent_data

    except Exception as e:
        print(f"Erro no processamento de audio: {e}")
        return None
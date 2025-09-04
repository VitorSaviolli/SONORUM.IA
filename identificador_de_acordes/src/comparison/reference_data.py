import os
import librosa
import numpy as np

def analyze_chord_frequencies(file_path):
    """
    Carrega um arquivo de áudio, realiza a Transformada de Fourier
    e retorna as frequências mais proeminentes.
    """

    # Ele remove frequências que não são importantes ou que são apenas ruído (ainda nao apliquei)
    #limiar = 0.5 # Exemplo: 50% da magnitude máxima

    try:
        y, sr = librosa.load(file_path, sr=None)
        stft_output = librosa.stft(y)
        magnitudes = np.abs(stft_output)
        freq_bins = librosa.fft_frequencies(sr=sr)
        mean_magnitudes = np.mean(magnitudes, axis=1)
        
        #teste das 5 maiores magnitudes
        top_indices = np.argsort(mean_magnitudes)[-10:]

        #prominent_frequencies = freq_bins[np.where(mean_magnitudes > limiar)]
        prominent_frequencies = freq_bins[top_indices]


        return prominent_frequencies

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
                    print("Frequências (em Hz):")
                    for frequency in np.sort(frequencies):
                        print(f"- {frequency:.2f} Hz")
                    print("\n")
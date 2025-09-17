import os
import librosa
import numpy as np

# Define o limiar de magnitude para filtrar frequências irrelevantes
MAGNITUDE_THRESHOLD = 0.1
# Filtra as frequências altas que são provavelmente harmônicos (acima de 800 Hz)
max_freq_limit = 800

def extract_chroma(y, sr):
    try:
        """Extrai e normaliza o cromagrama médio de um sinal de áudio."""
        # Extrai o cromagrama (12 classes de notas)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        chroma_mean = np.mean(chroma, axis=1)
        norm = np.linalg.norm(chroma_mean)
        
        if norm > 0:
            chroma_norm = chroma_mean / norm
        else:
            chroma_norm = chroma_mean  
            
        return chroma_norm.tolist()

    except Exception as e:
        print(f"Erro no processamento de audio: {e}")
        return None
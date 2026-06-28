import os
import librosa
import librosa.display
import matplotlib
# Use a non-interactive backend so matplotlib saves files without opening pop-up windows
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Swara Map Configurations
swara_freqs = {
    "Sa": 261.63, "R1": 277.18, "R2": 293.66, "G2": 311.13, "G3": 329.63,
    "Ma1": 349.23, "Ma2": 369.99, "Pa": 392.00, "Da1": 415.30, "Da2": 440.00,
    "Ni2": 466.16, "Ni3": 493.88, "U-Sa": 523.25
}

string_notes = {
    "Sa": 1, "R1": 2, "R2": 3, "G2": 4, "G3": 5, "Ma1": 6, "Ma2": 7,
    "Pa": 8, "Da1": 9, "Da2": 10, "Ni2": 11, "Ni3": 12, "U-Sa": 13
}

def find_closest_swara(freq):
    closest = min(swara_freqs.items(), key=lambda x: abs(freq - x[1]))
    return closest[0]

def convert_audio_to_carnatic(audio_path, static_folder):
    """
    Processes audio path dynamically and outputs a dictionary 
    containing swara results and plot absolute paths.
    """
    # Load audio file
    y, sr = librosa.load(audio_path, sr=None)
    duration = len(y) / sr

    # =========================================================
    # GENERATE AND SAVE PLOTS
    # =========================================================
    # 1. Waveform Plot
    plt.figure(figsize=(12, 4))
    librosa.display.waveshow(y, sr=sr)
    plt.title("Waveform")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    waveform_path = os.path.join(static_folder, 'waveform.png')
    plt.savefig(waveform_path)
    plt.close()

    # 2. Spectrogram Plot
    D = librosa.stft(y)
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    plt.figure(figsize=(12, 5))
    librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='hz')
    plt.colorbar(format='%+2.0f dB')
    plt.title("Spectrogram")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Frequency (Hz)")
    plt.tight_layout()
    spectrogram_path = os.path.join(static_folder, 'spectrogram.png')
    plt.savefig(spectrogram_path)
    plt.close()

    # =========================================================
    # PITCH DETECTION & PROCESSING
    # =========================================================
    hop_length = 256
    fmin = librosa.note_to_hz('C2')
    fmax = librosa.note_to_hz('C7')
    f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=fmin, fmax=fmax, hop_length=hop_length)
    times = librosa.times_like(f0)

    # 3. Pitch Trace Plot
    plt.figure(figsize=(12, 4))
    plt.plot(times, f0, label="Pitch")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Frequency (Hz)")
    plt.title("Pitch Trace")
    plt.legend()
    plt.tight_layout()
    pitch_path = os.path.join(static_folder, 'pitch_trace.png')
    plt.savefig(pitch_path)
    plt.close()

    # Metrics processing
    average_confidence = float(np.nanmean(voiced_probs)) if not np.isnan(np.nanmean(voiced_probs)) else 0.0
    valid_pitches = f0[~np.isnan(f0)]

    # Map Notes
    detected_notes = []
    results_for_csv = []
    for pitch in valid_pitches:
        swara = find_closest_swara(pitch)
        string_number = string_notes[swara]
        detected_notes.append(f"{swara} (Str {string_number})")
        results_for_csv.append({"pitch_hz": round(float(pitch), 2), "swara": swara, "string_number": string_number})

    # Save to CSV in project directory
    df = pd.DataFrame(results_for_csv)
    csv_path = os.path.join(os.path.dirname(audio_path), "detected_music_notes.csv")
    df.to_csv(csv_path, index=False)

    # Return summary data bundle back to app.py
    return {
        "sampling_rate": sr,
        "duration": round(duration, 2),
        "confidence": round(average_confidence, 3),
        "notes": detected_notes[:50],  # Sending the top 50 sequence notes over
        "plots": {
            "waveform": "/static/waveform.png",
            "spectrogram": "/static/spectrogram.png",
            "pitch": "/static/pitch_trace.png"
        }
    }
# Raagalipii-Music-to-Music-notes-# 🎵 Raagalipii — Where Music is Seen

Raagalipii is an intelligent, web-based Carnatic Visual Studio dashboard built with **Flask** and **Vanilla JavaScript**. The system transforms uploaded vocal tracks or instrumental audio melodies into authentic, human-readable Carnatic notation (*Swaras*) alongside multi-layered music visualization charts (Waveform Envelopes, Spectrogram Overlap Matrices, and Fundamental Pitch Traces). It also includes features for live voice comparison analysis (*Gamaka matching*) and dynamic PDF swara sheet compilation.

---

## ✨ Features

- **Audio-to-Carnatic Transcription:** Dynamically transcribes uploaded audio files (`.mp3`, `.wav`, `.m4a`) into structured *Swara* sequences (e.g., $S \rightarrow R_2 \rightarrow G_3$).
- **Multi-Chart Feature Visualizations:** Projects high-fidelity analytical graphs:
  - Vocal Waveform Envelope
  - Short-Time Fourier Transform (STFT) Spectrogram
  - pYIN Fundamental Pitch Trace ($f_0$)
- **Live Studio Learning Engine:** Captures live user microphone recordings and runs a frequency-matching engine to score the user's accuracy against original patterns.
- **Dynamic Recent Activity Logging:** Saves metadata history of uploaded audio and caches files locally to let users quickly reload past sessions into the workspace.
- **On-the-Fly PDF Compilation:** Formats generated musical notations securely using native document construction guidelines for instantaneous download.

---

## 📁 Project Directory Structure

Ensure your workspace follows this organized directory layout for correct script execution and path resolution:

```text
raagalipi-project/
│
├── app.py                 # Core Flask backend server routing architecture
├── file1.py               # ML inference script containing pitch & swara extraction logic
├── README.md              # Project setup, documentation, and operational reference
│
├── uploads/               # Temporary destination directory for raw audio uploads
│
└── static/                # Static web asset files served securely by Flask
    ├── background.png     # Application layout structural wallpaper
    ├── comparison_output.png # Live graph generation output asset target
    │
    ├── css/
    │   └── style.css      # Core UX/UI layout template stylesheet
    │
    ├── history_cache/     # Local disk storage container for file persistence history
    │   └── [cached_audio_files]
    │
    ├── images/
    │   └── website logo.png # Primary application logo asset
    │
    └── js/
        └── main.js        # Main UI event bindings and client network transmission logic

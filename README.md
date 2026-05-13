# 🎬 AI IMDb Video Generator (Bilingual)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Framework: Gemini](https://img.shields.io/badge/AI-Gemini_3.0_Flash-orange.svg)](https://aistudio.google.com/)

An autonomous AI pipeline that transforms a movie title into a full **2-minute cinematic summary video**. 
Now featuring full **Bilingual (English & Hindi)** support for global and local audiences.

---

## 🌟 Key Highlights

*   **🌐 Bilingual Narration:** Swappable language logic for English (British/American) and Hindi (Natural Devanagari voiceover).
*   **🤖 Autonomous Scripting:** Leverages **Gemini 1.5 Flash** to architect 300-word cinematic scripts with segment-wise timing.
*   **⚡ Edge-TTS Integration:** Uses Microsoft's Neural engine for high-fidelity, human-like voice synthesis without API costs.
*   **🖼️ Dynamic Asset Fetching:** Real-time metadata and high-res backdrop retrieval from **TMDB**.
*   **🎬 Automated Post-Production:** Programmatic video assembly using **MoviePy** including title cards, audio-video muxing, and clean transitions.

---

## 🏗️ System Workflow

1.  **Input:** User provides `Movie Name` + `Language`.
2.  **Fetch:** `data_fetcher` pulls metadata, ratings, and backdrops.
3.  **Think:** `script_generator` (Gemini) writes a time-coded cinematic script.
4.  **Speak:** `voice_over` (Edge-TTS) generates high-quality narration.
5.  **Render:** `video_assembler` crops assets, adds overlays, and merges everything into a final `.mp4`.

---

## 🛠️ Tech Stack

| Component | Tool | Category |
| :--- | :--- | :--- |
| **Language Model** | Gemini 3.0 Flash | LLM / Generative AI |
| **Audio Engine** | Edge TTS (Neural) | Text-to-Speech |
| **Data Source** | TMDB API (v3) | Metadata & Media |
| **Editing Engine** | MoviePy + FFmpeg | Video Processing |
| **Core Logic** | Python 3.10+ | Programming |

---

## ⚙️ Quick Start

### 1. Prerequisites
Install **FFmpeg** (essential for audio/video processing):
*   **Windows:** `choco install ffmpeg` (or download from ffmpeg.org)
*   **Mac:** `brew install ffmpeg`

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/avneeshkum/imdb-video-generator.git

# Enter the directory
cd imdb-video-generator

# Install dependencies
pip install -r requirements.txt

```

### 3. Configuration

Edit `config.py` to include your API credentials:

```python
TMDB_API_KEY   = "your_tmdb_key"
GEMINI_API_KEY = "your_gemini_key"

```

---

## 🎥 Execution

Run the generator with your favorite movie and preferred language:

```bash
# Generate in Hindi (Krrish 3)
python main.py "Krrish 3" hi

# Generate in English (Interstellar)
python main.py "Interstellar" en

```

📂 **Output:** Final videos are saved in the `/output` folder.

---

## 🎙️ Supported Voice Profiles

| Language | Model | Personality |
| --- | --- | --- |
| **English** | `en-GB-RyanNeural` | Deep, Cinematic British |
| **Hindi** | `hi-IN-MadhurNeural` | Professional Indian Narrator |

---

## 📂 Project Architecture

```text
.
├── main.py                # Main orchestrator
├── config.py              # Centralized settings & keys
├── requirements.txt       # Dependency manifest
├── modules/               # Modularized logic units
│   ├── data_fetcher.py    # TMDB API interface
│   ├── script_generator.py# LLM Prompt Engineering
│   ├── voice_over.py      # Audio synthesis
│   └── video_assembler.py # Visual rendering engine
└── output/                # Generated Video Assets

```

---

## 🤝 Contributing

Feel free to fork this project and submit PRs! Suggestions for adding Ken Burns effects or automatic subtitles are welcome.

Developed by [Avneesh](https://www.google.com/search?q=https://github.com/avneeshkum)
Submitted as an AI Engineering Assignment*

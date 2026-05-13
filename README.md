# IMDb → 2-Minute Video Generator (Bilingual)

An autonomous AI pipeline that generates a full 2-minute cinematic movie review/summary video simply by providing a movie name. Now supports both **English** and **Hindi** outputs.

---

## 🚀 Key Features

* **Bilingual Support:** Generate videos in either English or Hindi (Devanagari script + Natural Narration).
* **Automatic Data Fetching:** Pulls movie metadata, ratings, and high-quality backdrops from TMDB.
* **AI Script Writing:** Uses Gemini 1.5 Flash to write engaging, 2-minute cinematic scripts.
* **Natural Voiceovers:** Uses Microsoft Edge TTS (Neural) for high-quality, human-like narration.
* **Automated Editing:** MoviePy handles the assembly of title cards, images, and audio into a final MP4.

---

## 🛠️ Tech Stack (100% Free)

| Stage | Tool | Cost |
| --- | --- | --- |
| **Movie Data** | TMDB API | Free |
| **Script Generation** | Gemini 1.5 Flash | Free |
| **Voice Over** | Edge TTS (Neural) | Free |
| **Video Assembly** | MoviePy + FFmpeg | Free |

---

## ⚙️ Setup Instructions

### Step 1: Install Python

Ensure you have Python 3.10 or higher installed. Check your version:

```bash
python --version

```

### Step 2: Install FFmpeg

FFmpeg is required for video and audio processing.

* **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to System PATH.
* **Mac:** `brew install ffmpeg`
* **Ubuntu/Linux:** `sudo apt install ffmpeg`

### Step 3: Clone & Install Dependencies

Navigate to the project folder and run:

```bash
pip install -r requirements.txt

```

### Step 4: Configure API Keys

Open `config.py` and enter your keys:

```python
TMDB_API_KEY   = "your_tmdb_key_here"
GEMINI_API_KEY = "your_gemini_key_here"

```

---

## 🎥 Usage

You can now specify the language as an optional argument (`en` for English, `hi` for Hindi).

**For Hindi Video:**

```bash
python main.py "Krrish 3" hi

```

**For English Video:**

```bash
python main.py "Interstellar" en

```

*The final video will be saved in the `output/` folder.*

---

## 📂 Project Structure

```text
imdb_video_generator/
├── main.py                ← Entry point (Handles inputs & workflow)
├── config.py              ← Configuration & API Keys
├── requirements.txt       ← Python dependencies
├── modules/
│   ├── data_fetcher.py     ← TMDB integration (Bilingual fetching)
│   ├── script_generator.py ← AI logic for Hindi/English scripts
│   ├── voice_over.py       ← Voice model switching (Madhur vs Ryan)
│   └── video_assembler.py  ← Final MP4 rendering engine
├── output/                ← Final generated videos
└── temp/                  ← Temporary files (auto-cleaned)

```

---

## 🔑 How to Get API Keys

### 1. TMDB API Key (For Movie Data)

1. Sign up at [TheMovieDB.org](https://www.themoviedb.org/signup).
2. Go to **Settings** → **API** → **Create**.
3. Copy the **API Key (v3 auth)** and paste it into `config.py`.

### 2. Gemini API Key (For Scripts)

1. Go to [Google AI Studio](https://aistudio.google.com).
2. Click **"Get API Key"** → **"Create API Key"**.
3. Copy the key and paste it into `config.py`.

---

## 🎙️ Voice Models

| Language | Default Voice Model | Style |
| --- | --- | --- |
| **English** | `en-GB-RyanNeural` | Cinematic British Male |
| **Hindi** | `hi-IN-MadhurNeural` | Deep & Professional Indian Male |

*You can change these in `config.py` to female voices like `en-US-JennyNeural` or `hi-IN-SwaraNeural`.*

---

## 🛠️ Troubleshooting

* **`ReadTimeout Error`**: TMDB server is slow. The code now has an increased timeout (30s) and error handling to skip missing images.
* **`Silent Video`**: If you don't hear audio in VS Code, open the video in **VLC Media Player**. VS Code's internal player sometimes struggles with specific codecs.
* **`ffmpeg not found`**: Ensure FFmpeg is correctly installed and added to your Environment Variables/PATH.

---

**Developed by Avneesh**

*Submitted as an AI Engineering Internship Assignment.*
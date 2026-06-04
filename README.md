<div align="center">

# ⚡ REDDITSPEAKS ⚡

### Every Reddit image has a sound. You've never heard it until now.

```
🌐 Reddit  →  👁️ Vision AI  →  💬 5-Word Caption  →  🎵 Sine Frequency  →  🎬 Video
```

<p>
<img src="https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python"/>
<img src="https://img.shields.io/badge/Ollama-LLaVA%2013B-00b894?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Audio-Sine%20Wave-orange?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Video-MoviePy-red?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Offline-100%25%20Local-success?style=for-the-badge"/>
<img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge"/>
</p>

*12 frames · 24 seconds · 1 unique tone per image · no APIs · no cloud*

</div>

---

## What Is This?

RedditSpeaks is a fully offline AI pipeline that watches Reddit, describes what it sees, and converts those descriptions into sound. The result is a synchronized 24sec audiovisual film where every image carries its own unique tone.

The AI picks where to look based on the time of day : cozy subreddits at night, nature at dawn, surreal content on a late Friday. It then generates a 5 word caption per image and maps that caption to a sine-wave frequency. Twelve images. Twelve tones. One film. Entirely on your machine.

---

## Features

<table>
<tr>
<td align="center" width="33%">

### 🎯 Time-Aware Curation
AI picks the most fitting subreddit for the current hour and day. Calm and cozy at midnight, energetic and colorful at noon.

</td>
<td align="center" width="33%">

### 👁️ Vision Understanding
LLaVA 13B reads each image and generates a precise 5 word description of what it sees.

</td>
<td align="center" width="33%">

### 🎵 Meaning → Sound
Each caption is mapped to a sine-wave frequency. Calm scenes hum low. Vivid, chaotic scenes ring high.

</td>
</tr>
<tr>
<td align="center" width="33%">

### 🎬 Synchronized Film
12 images × 2 seconds each = a 24-second audiovisual story with frame accurate audio per scene.

</td>
<td align="center" width="33%">

### 🧭 No Repeats
Tracks every visited subreddit in `visited.txt`. Each run explores somewhere new.

</td>
<td align="center" width="33%">

### 🔒 Fully Offline
Zero cloud dependency. Everything runs locally after the initial model download.

</td>
</tr>
</table>

---

## The Sound Map

The AI maps the emotional weight of each caption to a frequency range:

| Mood | Character |
|---|---|
| 🌿 Calm & still | Soft, grounding hum |
| 🌅 Neutral & scenic | Balanced, storytelling tone |
| ⚡ Vivid & energetic | Sharp, dynamic frequency |

> The result is a short film where you **hear what images feel like**, not just see them.
---

## How It Works

Each run of `main.py` does exactly one job and exits. This is intentional.

1. **Time-aware selection** — LLaVA 13B reads the current hour and day, picks a subreddit from 60+ visual communities, and logs it to `visited.txt` to prevent repeats.
2. **Image extraction** — Selenium opens Reddit, finds the top image post, and saves it to `assets/images/`.
3. **Vision captioning** — LLaVA 13B generates a five-word description of the image (e.g. *"foggy mountain at dawn"*).
4. **Frequency mapping** — The caption is fed into a strict prompt with `temperature=0.0` that outputs a single integer pitch value.
5. **Film synthesis** — MoviePy builds 2-second sine-wave clips with fade envelopes, overlays captions, and concatenates everything into a final MP4.
6. **Batch logic** — After 12 successful runs the system automatically renders `output.mp4`. A safe reset prevents image overflow.

```
Run 1–11  →  fetch one image  →  save  →  exit
Run 12    →  12/12 reached   →  build captions + audio + video  →  output.mp4
Run 13+   →  output exists   →  prompt to reset for next batch
```

---

## Quick Start

**1. Clone**
```bash
git clone https://github.com/yourusername/redditspeaks.git
cd redditspeaks
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Pull the vision model**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llava:13b
```

**4. Install Chrome**

| OS | Command |
|---|---|
| macOS | `brew install --cask google-chrome` |
| Linux | `sudo apt install google-chrome-stable` |
| Windows | Download from [google.com/chrome](https://google.com/chrome) |

**5. Run**
```bash
python main.py
```

Repeat until `12/12`. Your film lands at `assets/output/output.mp4`.

---

## Configuration

| Parameter | File | Default | Description |
|---|---|---|---|
| `SUBREDDITS` | `get_topic.py` | 60+ communities | The pool the AI picks from |
| `MAX_IMAGE_COUNT` | `main.py` | `12` | Images per video |
| `DURATION` | `main.py` | `2` seconds | Length of each frame |
| Pitch range | `get_audio_pitch.py` | 50 – 3000 Hz | Frequency ceiling/floor |
| Caption length | `get_caption.py` | ≤ 5 words | Description brevity |
| `retries` | `main.py` | `7` | Attempts before giving up |

---

## Tech Stack

<table>
<tr>
<td width="50%">

| Component | Technology |
|---|---|
| Language | Python 3.11+ |
| Vision Model | Ollama — LLaVA 13B |
| Web Scraping | Selenium + ChromeDriver |

</td>
<td width="50%">

| Component | Technology |
|---|---|
| Image Download | `requests` |
| Audio Synthesis | NumPy (sine waves) |
| Video Composition | MoviePy |

</td>
</tr>
</table>

---

## Project Structure

```
redditspeaks/
├── main.py                 # Pipeline orchestrator
├── get_topic.py            # Time-aware subreddit selection
├── get_post.py             # Reddit image extraction
├── get_caption.py          # Vision captioning (LLaVA)
├── get_audio_pitch.py      # Caption to frequency mapping
├── make_frame_audio.py     # Sine wave audio synthesis
├── image_to_base64.py      # Image encoding utility
├── modules.py              # Shared imports
├── requirements.txt
├── visited.txt             # Subreddit memory log
└── assets/
    ├── images/             # Downloaded Reddit images
    ├── audio/              # Generated audio clips
    └── output/             # Final output.mp4
```

---

## Limitations

- Reddit UI changes may break Selenium selectors without notice
- LLaVA 13B requires ~4.5 GB of local VRAM/RAM
- Audio is purely sine-based with no harmonic complexity yet
- Requires 12 sequential runs to produce a full video

---

## Roadmap

- [ ] Replace Selenium with PRAW (Reddit API) for reliability
- [ ] Harmonic and layered audio synthesis for richer soundscapes
- [ ] Sentiment aware audio modulation per image
- [ ] Scheduled autonomous daily generation via cron
- [ ] Lightweight web preview interface
- [ ] Visual transitions and beat synchronization

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `UnboundLocalError: driver` | Add `driver = None` at top of `get_post.py` |
| No image saved / login wall | Run once with visible browser and log in manually |
| LLaVA returns non-integer | Set `temperature=0.0` and enforce strict prompt |
| `ollama.generate` timeout | Run `ollama serve` in a separate terminal first |
| Video rendering fails | Run `pip install imageio-ffmpeg` |
| TextClip errors | Install ImageMagick |
| `visited.txt` not updating | Ensure `.strip()` is used when reading the file |

---

<div align="center">

**Every Reddit image has a sound. You've never heard it until now.**

<img src="https://img.shields.io/badge/Made%20with-passion-red?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Built%20during-100%20Days%20of%20Code-orange?style=for-the-badge"/>

</div>

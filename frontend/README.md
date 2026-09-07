# 🌍 Tourist & Local AI Speech Communicator

A two-way conversational bridge for tourists and locals that transcribes audio in real-time and displays large-format translated text on a face-to-face split-screen.

Powered by **AssemblyAI Universal-1 (Speech-to-Text)** and **AssemblyAI LeMUR (Translation & Intent Engine)**.

---

## 🚀 Features
- **Face-to-Face Split UI:** Top screen is inverted 180° for the local, while the bottom faces the tourist.
- **Universal Speech Recognition:** Multilingual audio transcription with automatic language detection.
- **Context-Aware Translation:** Powered by AssemblyAI LeMUR for natural conversational phrasing.
- **Push-to-Talk Recording:** Low-latency Web Audio API handling.

---

## 🛠️ Quick Start

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/your-username/tourist-translator-ai.git
cd tourist-translator-ai
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
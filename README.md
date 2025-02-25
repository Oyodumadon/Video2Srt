# Video2Srt
Script Python pour transcrire, traduire en français, et intégrer sous-titres/voix dans une vidéo.

## Prérequis
- Python 3.x
- FFmpeg
- eSpeak
- `whisper`, `deep-translator`

## Installation
```bash
python -m venv venv
source venv/bin/activate
pip install git+https://github.com/openai/whisper.git deep-translator
sudo pacman -S ffmpeg espeak

## Utilisation 
python Video2Srt.py

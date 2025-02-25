import whisper
from deep_translator import GoogleTranslator
import os
import subprocess

def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

# Demande le nom du fichier vidéo à l'utilisateur
video_file = input("Entrez le nom du fichier vidéo à transcrire (ex. video.mp4) : ")

# Vérifie si le fichier existe
if not os.path.exists(video_file):
    print(f"Erreur : Le fichier '{video_file}' n'existe pas. Vérifiez le nom ou le chemin.")
    exit(1)

# Transcription avec Whisper
print(f"Transcription de '{video_file}' en cours...")
model = whisper.load_model("medium")
result = model.transcribe(video_file, language="en", verbose=True)

# Nom du fichier SRT français basé sur le nom de la vidéo
output_srt = video_file.rsplit(".", 1)[0] + "_fr.srt"

# Écriture SRT français avec traduction
translator = GoogleTranslator(source="en", target="fr")
print("Traduction en français en cours...")
with open(output_srt, "w", encoding="utf-8") as f:
    for i, segment in enumerate(result["segments"], 1):
        start = segment["start"]
        end = segment["end"]
        text = translator.translate(segment["text"].strip())
        f.write(f"{i}\n")
        f.write(f"{format_timestamp(start)} --> {format_timestamp(end)}\n")
        f.write(f"{text}\n\n")

print(f"Fichier traduit généré : {output_srt}")

# Intégration des sous-titres dans la vidéo avec FFmpeg
output_video = video_file.rsplit(".", 1)[0] + "_subtitled.mp4"
print(f"Intégration des sous-titres dans '{output_video}' en cours...")
try:
    subprocess.run([
        "ffmpeg",
        "-i", video_file,              # Fichier vidéo d’entrée
        "-vf", f"subtitles={output_srt}",  # Filtre pour incruster le SRT
        "-c:v", "libx264",             # Codec vidéo (H.264)
        "-c:a", "copy",                # Copie l’audio sans réencodage
        "-y",                          # Écrase le fichier de sortie si existant
        output_video                   # Fichier vidéo de sortie
    ], check=True)
    print(f"Vidéo avec sous-titres générée : {output_video}")
except subprocess.CalledProcessError as e:
    print(f"Erreur lors de l'intégration avec FFmpeg : {e}")

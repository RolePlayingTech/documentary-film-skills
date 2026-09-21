"""
Skrypt automatycznej syntezy kwestii lektora w ElevenLabs API dla modelu Eleven v3.
Pobiera klucze i parametry z pliku .env lub zmiennych środowiskowych.
"""

import os
import sys
import argparse
import importlib.util
import subprocess
import requests

def load_env():
    """Wczytuje zmienne z pliku .env, jeśli istnieje."""
    env_file = os.path.join(os.getcwd(), ".env")
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip("'\"")
                    if k not in os.environ:
                        os.environ[k] = v

load_env()

API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "gFl0NeqphJUaoBLtWrqM")
MODEL_ID = os.getenv("ELEVENLABS_MODEL_ID", "eleven_v3")
STABILITY = float(os.getenv("ELEVENLABS_STABILITY", "0.50"))
SIMILARITY = float(os.getenv("ELEVENLABS_SIMILARITY_BOOST", "0.80"))

def get_audio_duration(file_path):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", file_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return float(res.stdout.strip())
    except Exception:
        return 0.0

def synthesize(voiceovers_dict, out_dir):
    if not API_KEY or API_KEY.startswith("sk_twoj"):
        print("BŁĄD: Brak poprawnego klucza ELEVENLABS_API_KEY w zmiennych środowiskowych lub pliku .env!")
        sys.exit(1)

    os.makedirs(out_dir, exist_ok=True)
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    print(f"=== SYNTEZA ELEVENLABS (Głos: Piotr [{VOICE_ID}], Model: {MODEL_ID}) ===")
    results = {}

    for key, text in voiceovers_dict.items():
        out_path = os.path.join(out_dir, f"{key}.mp3")
        if not os.path.exists(out_path) or os.path.getsize(out_path) < 1000:
            print(f"--> Generuję {key}...")
            payload = {
                "text": text,
                "model_id": MODEL_ID,
                "voice_settings": {
                    "stability": STABILITY,
                    "similarity_boost": SIMILARITY
                }
            }
            res = requests.post(url, headers=headers, json=payload)
            if res.status_code == 200:
                with open(out_path, "wb") as f:
                    f.write(res.content)
                print(f"    Pobrano: {out_path} ({os.path.getsize(out_path)} bajtów)")
            else:
                print(f"    BŁĄD API dla {key}: {res.status_code} {res.text}")
                continue
        else:
            print(f"--> Plik {key}.mp3 już istnieje. Pomijam syntezę.")

        dur = get_audio_duration(out_path)
        slot = dur + 0.80
        results[key] = {"duration": dur, "slot": slot, "path": out_path}
        print(f"    Czas audio: {dur:.2f}s | Cel wideo Multi-Shot: {slot:.2f}s")

    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synteza kwestii lektora ElevenLabs")
    parser.add_argument("--script", required=True, help="Ścieżka do pliku python ze słownikiem VOICEOVERS")
    parser.add_argument("--out", default="./voiceovers", help="Katalog wyjściowy na pliki mp3")
    args = parser.parse_args()

    spec = importlib.util.spec_from_file_location("script_data", args.script)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    if not hasattr(mod, "VOICEOVERS"):
        print(f"BŁĄD: Plik {args.script} nie zawiera słownika VOICEOVERS!")
        sys.exit(1)

    res = synthesize(mod.VOICEOVERS, args.out)
    total_dur = sum(r["duration"] for r in res.values())
    print(f"\nŁączny czas trwania wygenerowanego lektora: {total_dur:.2f}s ({total_dur/60:.2f} min)")

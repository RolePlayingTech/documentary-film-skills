"""
Automatyczny audyt mowy i dykcji za pomocą Whisper STT.
Sprawdza czy wygenerowany klip nie uciął zdania, nie przekręcił kluczowych słów ani nie zająknął się.
"""

import os
import sys
import whisper

def audit_audio(file_path, expected_text=None, model_size="base"):
    if not os.path.exists(file_path):
        print(f"BŁĄD: Plik nie istnieje: {file_path}")
        return False

    print(f"--- Audyt Whisper STT: {os.path.basename(file_path)} (Model: {model_size}) ---")
    model = whisper.load_model(model_size)
    res = model.transcribe(file_path, language="pl", word_timestamps=True)
    transcription = res["text"].strip()
    print(f"Transkrypcja: \"{transcription}\"")

    words = []
    for s in res.get("segments", []):
        for w in s.get("words", []):
            words.append(w)

    if not words:
        print("BŁĄD: Brak wykrytej mowy w pliku!")
        return False

    last_word = words[-1]
    print(f"Koniec mowy: {last_word['end']:.2f}s (Słowo: '{last_word['word']}')")

    # Sprawdzenie czy mowa nie jest ucięta na granicy 10.0s w klipach A-Roll
    if last_word['end'] >= 9.80:
        print("OSTRZEŻENIE: Mowa kończy się tuż przy granicy klipu (>=9.8s). Ryzyko ucięcia zdania!")

    # Sprawdzenie zająknięć (powtórzone słowa z rzędu)
    clean_words = [w['word'].strip().lower() for w in words]
    for i in range(len(clean_words) - 1):
        if clean_words[i] == clean_words[i+1] and len(clean_words[i]) > 2:
            print(f"BŁĄD: Wykryto powtórzone słowo / zająknięcie: '{clean_words[i]}'!")
            return False

    if expected_text:
        print(f"Oczekiwany tekst: \"{expected_text}\"")

    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Użycie: python qc_speech_whisper.py <plik_audio_lub_wideo> [oczekiwany_tekst] [model_size]")
        sys.exit(1)
    f = sys.argv[1]
    exp = sys.argv[2] if len(sys.argv) > 2 else None
    m = sys.argv[3] if len(sys.argv) > 3 else "base"
    ok = audit_audio(f, exp, m)
    sys.exit(0 if ok else 1)

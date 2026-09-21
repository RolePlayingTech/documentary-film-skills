---
name: documentary-editor-master
description: >-
  Use this skill to assemble, mix, and render final documentary master films in FFmpeg.
  It executes Multi-Shot B-roll assembly without video loops (matching duration to voiceover + 0.8s),
  normalizes audio to EBU R128 (-16 LUFS), extracts clean dialogs for Whisper STT, generates calibrated
  Karaoke ASS subtitles (-90ms anticipatory offset), applies dynamic sidechain ducking to background music,
  and renders dual emission masters (Clean Master and Subtitled Master).
---

# Documentary Editor Master

Ten skill instruuje agenta, jak przeprowadzić profesjonalny proces montażu, miksowania audio oraz finalnego renderingu minidokumentu w FFmpeg zgodnie ze standardem emisyjnym.

---

## 1. Reguła Multi-Shot dla B-Roll (Zakaz Pętli Wideo)

### ❌ Całkowity zakaz zapętlania (`-stream_loop`)
Zapętlony ruch kamery i powtarzające się motywy wyglądają sztucznie.

### ✅ Sekwencja wieloujęciowa dopasowana do głosu:
* **Gdy lektor trwa 10–18 s**: Montujemy scenę z **dwóch unikalnych ujęć** (Shot A + Shot B), np. po 6–9 sekund.
* **Gdy lektor trwa 19–27 s**: Montujemy scenę z **trzech unikalnych ujęć** (Shot A + Shot B + Shot C), np. po 7–9 sekund.
* **Łączny czas sekwencji**: Obraz przycinamy co do klatki pod czas:
  $$t_{\text{total}} = \text{lektor\_dur} + 0.80\,\text{s}$$

---

## 2. Miksowanie Audio w B-Roll (Priorytet Lektora)

W filtrze `amix`:
1. Strumień lektora (znormalizowany do -16 LUFS przez `loudnorm=I=-16:TP=-1.5:LRA=7`) musi być **wejściem pierwszym** (`[0:a]`).
2. Strumień ambientu z wideo (ściszony do `volume=0.08`) jest wejściem drugim.
3. Nigdy nie podawaj ambientu na wejście pierwsze przy `duration=first` – spowoduje to ucięcie lektora po 10 sekundach!

---

## 3. Dynamiczny Sidechain Ducking Muzyki

Muzyka tła nie może być płaska ani „pompować” szumów:
1. Podkład muzyczny zapętlamy i wstępnie normalizujemy (`loudnorm=I=-24:TP=-2:LRA=11`).
2. Nakładamy filtr `sidechaincompress` sterowany kanałem dialogowym:
   ```text
   [music_loop][dialogue]sidechaincompress=threshold=0.08:ratio=5:attack=100:release=1000[music_ducked]
   ```
3. W trakcie mowy Świadka lub Lektora muzyka łagodnie ustępuje miejsca głosowi (-5 do -7 dB), a w pauzach oddechu organicznie narasta, podbijając emocje.

---

## 4. Napisy Karaoke ASS (-90ms Offset)

1. Transkrypcję słowo-po-słowie (`word_timestamps=True`) wykonujemy Whisperem na **czystym kanale dialogowym** (`dialog_master.wav`), wyeksportowanym z surowego montażu PRZED dodaniem muzyki.
2. Zdarzenia `\k` w pliku `.ass` muszą posiadać kalibrowany offset wyprzedzający **-90ms**, aby podświetlenie słowa następowało idealnie w momencie uderzenia głoski w uchu widza.

---

## 5. Dwie Wersje Emisyjne Master

Końcowy proces tworzy dwa pliki wideo:
1. **Master Clean (`*_master_clean.mp4`)**:
   - Czysty obraz 1280x720 24fps (libx264, preset slow, CRF 17).
   - Audio ze zmiksowanym dialogiem i sidechain duckingiem muzyki.
   - Brak jakichkolwiek napisów ani logotypów.
2. **Master Subtitled (`*_master_napisy.mp4`)**:
   - Wersja z wtopionymi napisami Karaoke ASS (`ass='karaoke.ass'`).
   - Wypoziomowany dźwięk ze ścieżką muzyczną.

Szczegółowe przepisy na filtry FFmpeg: zobacz [ffmpeg_filter_recipes.md](./references/ffmpeg_filter_recipes.md).

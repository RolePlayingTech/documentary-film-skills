---
name: documentary-editor-master
description: >-
  Use this skill to assemble, mix, and render final master films in FFmpeg for both widescreen (16:9) and vertical (9:16) formats.
  It executes Multi-Shot B-roll assembly without video loops (matching duration to voiceover + 0.8s),
  normalizes audio to EBU R128 (-16 LUFS), generates calibrated Karaoke ASS subtitles (-90ms anticipatory offset),
  applies dynamic sidechain ducking to background music, manages Clickbait Hook Card overlays (0.0s-3.5s),
  and renders dual emission masters (Clean Master and Subtitled Master).
---

# Universal Film Editor Master (16:9 & 9:16)

Ten skill instruuje agenta, jak przeprowadzić profesjonalny proces montażu, miksowania audio oraz finalnego renderingu filmu w FFmpeg zgodnie ze standardem emisyjnym – zarówno w formacie **horyzontalnym 16:9 (1920×1080)**, jak i **wertykalnym 9:16 (1080×1920)**.

---

## 1. Reguła Multi-Shot dla B-Roll (Zakaz Pętli Wideo)

### ❌ Całkowity zakaz zapętlania (`-stream_loop`)
Zapętlony ruch kamery i powtarzające się motywy niszczą kinowy odbiór filmu.

### ✅ Sekwencja wieloujęciowa dopasowana do głosu lektora:
* **Gdy lektor trwa 10–18 s**: Montujemy scenę z **dwóch unikalnych ujęć** (Shot A + Shot B), np. po 5–9 sekund.
* **Gdy lektor trwa > 18 s**: Montujemy scenę z **trzech unikalnych ujęć** (Shot A + Shot B + Shot C).
* **Łączny czas sekwencji**: Obraz przycinamy co do klatki pod czas lektora:
  $$t_{\text{total}} = \text{lektor\_dur} + 0.80\,\text{s}$$

---

## 2. Dynamiczny Sidechain Ducking Muzyki

Muzyka tła nie może zagłuszać głosu ani być płasko wyciszona:
1. Podkład muzyczny zapętlamy i miksujemy z filtrem `sidechaincompress` sterowanym kanałem dialogowo-lektorskim.
2. Gdy mówi lektor lub aktor, muzyka łagodnie ustępuje miejsca (-5 do -7 dB), a w pauzach oddechu (0.5–1.5s) organicznie narasta, budując kinowe emocje.

---

## 3. Belka Wstępna / Clickbait Hook Card ($t = 0.0s .. 3.5s$)

Dla formatów social media (Shorts, Reels, TikTok) nakładamy na pierwsze 3.5 sekundy filmu stylizowaną belkę / kartę z haczykiem dramaturgicznym:
* Format: PNG 1080×1920 z przezroczystością (RGBA).
* Płynny fade-out: `fade=t=out:st=3.0:d=0.5:alpha=1`.

---

## 4. Precyzyjne Napisy Karaoke ASS (-90ms Offset)

1. **Kalibracja wyprzedzenia (-90ms)**: Znaczniki czasu słów przesuwamy o `-90ms`, aby podświetlenie słowa następowało idealnie w momencie uderzenia głoski w uchu widza.
2. **Układ dla 16:9**:
   - `PlayResX: 1920`, `PlayResY: 1080`, `Fontsize: 36`, `MarginV: 90`.
3. **Układ dla 9:16 (Smartfon)**:
   - `PlayResX: 1080`, `PlayResY: 1920`, `Fontsize: 54`, `MarginV: 340`.
   - Krótkie linie (3–6 słów na ekranie), aby nie zasłaniać dolnego interfejsu TikToka/Reels.

---

## 5. Dwie Wersje Emisyjne Master

Końcowy proces tworzy dwa pliki wideo:
1. **Master Clean (`*_master_clean.mp4`)**:
   - Skalowany filtrem Lanczos (1920×1080 dla 16:9 lub 1080×1920 dla 9:16), 24 fps, CRF 18, preset slow.
   - Czysty obraz z nałożonym podkładem muzycznym i duckingiem, bez napisów.
2. **Master Subtitled (`*_master_napisy.mp4`)**:
   - Wersja z wtopionymi napisami Karaoke ASS (`subtitles=*.ass`).

Szczegółowe formuły filtrów: zobacz [dual_format_assembly_guide.md](./references/dual_format_assembly_guide.md).

# Przewodnik Montażu Dual-Format (16:9 & 9:16) w FFmpeg

Dokumentacja techniczna dla automatycznego montażu, miksowania audio oraz renderingu wideo w dwóch standardach: horyzontalnym (16:9, 1920×1080) i wertykalnym (9:16, 1080×1920).

---

## 1. Architektura Filtrów FFmpeg dla Formatu 16:9 vs 9:16

### A. Skalowanie i Klatkaż (Filtr Lanczos)
* **Dla 16:9**: Surowy plik z Flow (1280×720) skalujemy do kinowego Full HD:
  ```text
  scale=1920:1080:flags=lanczos,fps=24,setsar=1
  ```
* **Dla 9:16**: Surowy plik pionowy z Flow (720×1280) skalujemy do pełnego formatu smartfonowego:
  ```text
  scale=1080:1920:flags=lanczos,fps=24,setsar=1
  ```

---

## 2. Montaż Multi-Shot dla B-Roll (Zero Pętli Wideo)

W scenach B-roll czas trwania narzuca lektor: $t_{\text{total}} = t_{\text{vo}} + 0.80\,\text{s}$.
Dzielimy scenę na równe fragmenty ujęć Shot A i Shot B (np. $t_{\text{sub}} = t_{\text{total}} / 2$):

```bash
ffmpeg -y \
  -i shot_a.mp4 \
  -i shot_b.mp4 \
  -i lektor.mp3 \
  -filter_complex "\
    [0:v]trim=0:7.200,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,fps=24[v0]; \
    [0:a]atrim=0:7.200,asetpts=PTS-STARTPTS,volume=0.08[a0]; \
    [1:v]trim=0:7.200,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,fps=24[v1]; \
    [1:a]atrim=0:7.200,asetpts=PTS-STARTPTS,volume=0.08[a1]; \
    [v0][v1]concat=n=2:v=1:a=0[v_cat]; \
    [a0][a1]concat=n=2:v=0:a=1[amb_cat]; \
    [2:a]loudnorm=I=-16:TP=-1.5:LRA=7,apad=whole_dur=14.400,aresample=48000[vo_proc]; \
    [vo_proc][amb_cat]amix=inputs=2:duration=first[a_mix]" \
  -map "[v_cat]" -map "[a_mix]" \
  -t 14.400 -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k scene_broll.mp4
```

---

## 3. Dynamiczny Sidechain Ducking Muzyki + Hook Alert Box

W finalnym procesie miksujemy ścieżkę lektorsko-dialogową z podkładem muzycznym, wyciszając muzykę o 5–7 dB pod mową:

```bash
ffmpeg -y \
  -i master_raw.mp4 \
  -stream_loop -1 -i background_music.mp3 \
  -loop 1 -t 3.5 -i hook_card_overlay.png \
  -filter_complex "\
    [1:a]volume=0.20,aresample=48000[music]; \
    [0:a]asplit=2[dia_main][dia_sc]; \
    [music][dia_sc]sidechaincompress=threshold=0.035:ratio=5:attack=40:release=350[ducked_music]; \
    [dia_main][ducked_music]amix=inputs=2:duration=first[a_out]; \
    [2:v]format=rgba,fade=t=out:st=3.0:d=0.5:alpha=1[hook_fade]; \
    [0:v][hook_fade]overlay=0:0:enable='between(t,0,3.5)'[v_hooked]" \
  -map "[v_hooked]" -map "[a_out]" \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a aac -b:a 256k master_clean.mp4
```

---

## 4. Stylizacja Napisów Karaoke ASS dla 16:9 vs 9:16

### Stylizacja dla Formatu 16:9 (Desktop / TV):
```ini
[Script Info]
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,36,&H00FFFFFF,&H0000D7FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3.0,1.5,2,80,80,90,1
```

### Stylizacja dla Formatu 9:16 (Smartfon / TikTok / Reels):
W formacie pionowym napisy muszą znajdować się **powyżej dolnego interfejsu aplikacji** (MarginV: 320–360) oraz mieć większą czcionkę (Fontsize: 50–54):
```ini
[Script Info]
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,54,&H00FFFFFF,&H0000D7FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4.5,2.0,2,40,40,340,1
```

### Wypalanie Napisów:
```bash
ffmpeg -y -i master_clean.mp4 -vf "subtitles=subtitles.ass" -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a copy master_napisy.mp4
```

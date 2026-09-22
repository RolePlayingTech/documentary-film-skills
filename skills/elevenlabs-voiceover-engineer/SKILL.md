---
name: elevenlabs-voiceover-engineer
description: >-
  Use this skill to synthesize, direct, and normalize voiceovers using ElevenLabs API for ANY film genre.
  It configures voice profiles, selects appropriate models ('eleven_v3', 'eleven_multilingual_v2', 'eleven_turbo_v2_5'),
  applies emotional direction tags ([thoughtful], [whispers], [ironic], [pause]), calculates exact multi-shot video slots
  (duration + 0.8s), extracts word timestamps for karaoke subtitles, and normalizes audio to EBU R128 (-16 LUFS).
---

# ElevenLabs Universal Voiceover Engineer

Ten skill instruuje agenta, jak zarządzać syntezą głosu, reżyserią emocjonalną oraz inżynierią dźwięku lektora w **dowolnym projekcie wideo**: dokumentach, filmach fabularnych, zwiastunach, formacie pionowym na social media czy narracjach sci-fi.

---

## 1. Konfiguracja Środowiska i Wybór Modeli

Wymagana zmienna środowiskowa:
* `ELEVENLABS_API_KEY` – klucz API z platformy ElevenLabs.

Dostępne modele:
1. **`eleven_v3`** (**Rekomendowany**): Najnowszy model wielojęzyczny ze wsparciem dla bezpośrednich tagów reżyserskich (`[thoughtful]`, `[ironic]`, `[whispers]`, `[pause]`, `[excited]`).
2. **`eleven_multilingual_v2`**: Klasyczny model o żelaznej stabilności intonacyjnej (dla chłodnych narracji encyklopedycznych i technicznych).
3. **`eleven_turbo_v2_5`**: Model ultra-szybki, dedykowany do krótkich form informacyjnych.

---

## 2. Reżyseria Emocjonalna i Formatowanie Tekstu

Aby lektor brzmiał jak profesjonalny aktor, a nie syntezator mowy:
1. **Tagi ekspresji**: Wplataj tagi emocjonalne w kluczowych momentach narracji:
   - `[whispers]` przy ujawnianiu sekretów i budowaniu mrocznego klimatu.
   - `[pause]` przed puentą i po mocnych faktach.
   - `[ironic]` przy absurdach i paradoksach.
   - `[thoughtful]` przy filozoficznych podsumowaniach.
2. **Żelazna reguła zapisu liczb i dat**:
   - Wszystkie liczby i daty **muszą być bezwzględnie zapisane słownie** (np. *„w tysiąc dziewięćset osiemdziesiątym dziewiątym roku”*, a nie *„w 1989 r.”*).
   - W języku polskim dopełniacz roku 2000 ma postać **`roku dwutysięcznego`** (zapis *„dwa tysiące roku”* jest błędny i powoduje halucynację lektora).

Więcej inspiracji i wskazówek: zobacz [universal_voice_styles.md](./references/universal_voice_styles.md).

---

## 3. Kalkulacja Czasowa Slotu Multi-Shot (Zakaz Pętli Wideo)

Wideo dopasowujemy precyzyjnie do wygenerowanego głosu, nigdy odwrotnie:
1. Mierzymy dokładny czas trwania audio: `vo_dur = ffprobe(mp3)`.
2. Obliczamy targetowy czas trwania sceny wideo:
   $$\text{target\_video\_dur} = \text{vo\_dur} + 0.80\,\text{s}$$
3. Bufor `+0.80s` gwarantuje naturalne wybrzmienie ostatniej głoski aktora przed cięciem montażowym.
4. Dzielimy scenę na:
   - **2 ujęcia (Shot A + Shot B)**, jeśli $\text{target\_video\_dur} \le 18\,\text{s}$.
   - **3 ujęcia (Shot A + Shot B + Shot C)**, jeśli $\text{target\_video\_dur} > 18\,\text{s}$.

---

## 4. Ekstrakcja Znaczników Czasu Słów do Napisów Karaoke

Do stworzenia precyzyjnie synchronizowanych napisów karaoke:
1. Skrypt syntezy pobiera znaczniki czasu słów bezpośrednio z API ElevenLabs (`with_timestamps=True`) lub poprzez transkrypcję modelem Whisper STT (`word_timestamps=True`).
2. Słowa zapisywane są do pliku JSON ze znacznikami `start` i `end` w sekundach, stanowiąc bazę dla formatu ASS Karaoke (`\k`).

---

## 5. Normalizacja Audio (EBU R128)

Każda ścieżka lektorska przed montażem musi przejść normalizację głośności:
```bash
ffmpeg -i raw_vo.mp3 -af "loudnorm=I=-16:TP=-1.5:LRA=7,aresample=48000" -c:a pcm_s16le normalized_vo.wav
```
Standard `-16 LUFS` zapewnia spójność głośności na YouTube, TikToku oraz platformach emisyjnych.

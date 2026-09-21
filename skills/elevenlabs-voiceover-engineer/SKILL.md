---
name: elevenlabs-voiceover-engineer
description: >-
  Use this skill to synthesize, normalize, and audit documentary voiceovers using ElevenLabs.
  It configures the official documentary voice profile Piotr v3 ('eleven_v3', ID: gFl0NeqphJUaoBLtWrqM),
  applies emotional direction tags ([thoughtful], [ironic], [pause], [whispers]), calculates exact audio durations,
  determines Multi-Shot B-roll target slots (duration + 0.8s), and normalizes audio to EBU R128 (-16 LUFS).
---

# ElevenLabs Voiceover Engineer

Ten skill instruuje agenta, jak zarządzać syntezą głosu lektora w filmach dokumentalnych za pomocą ElevenLabs API, modelu **Eleven v3** oraz oficjalnego profilu głosu **Piotr**.

---

## 1. Oficjalny Profil Lektora Dokumentalnego

* **Głos**: **Piotr** (Neutral and Mature Bard)
* **Voice ID**: `gFl0NeqphJUaoBLtWrqM`
* **Model ID**: `eleven_v3` (Eleven v3 ze wsparciem tagów ekspresji)
* **Voice Settings**:
  - `stability`: `0.50`
  - `similarity_boost`: `0.80`

Konfiguracja pobierana jest automatycznie ze zmiennych środowiskowych:
- `ELEVENLABS_API_KEY`
- `ELEVENLABS_VOICE_ID`
- `ELEVENLABS_MODEL_ID`

---

## 2. Reżyseria Emocjonalna: Tagi Ekspresji v3

Model Eleven v3 obsługuje naturalne znaczniki reżyserskie umieszczane bezpośrednio w tekście:
* `[thoughtful]` – głęboki, refleksyjny ton narratora analizującego historię.
* `[ironic]` – cięta, chłodna ironia przy opisie ludzkiej naiwności lub błędów decyzyjnych.
* `[whispers]` – przyciszony, intymny głos przy ujawnianiu tajemnic lub ponurych faktów.
* `[pause]` – naturalna, wymowna pauza budująca napięcie przed puentą.
* `[sighs]` – ciężki oddech lub westchnienie rezygnacji.

Więcej informacji i przykłady: zobacz [voice_profile_piotr_v3.md](./references/voice_profile_piotr_v3.md).

---

## 3. Żelazna Reguła Liczebników i Dat

Przed wysłaniem tekstu do API upewnij się, że:
1. Żadna liczba ani data nie jest zapisana cyframi.
2. Dopełniacz roku 2000 ma bezwzględnie postać: **`roku dwutysięcznego`** (np. *„w lutym roku dwutysięcznego”*, *„dziesiątego marca roku dwutysięcznego”*). Zapis *„dwa tysiące roku”* powoduje odczytanie go jako rok 2020!

---

## 4. Kalkulacja Slotu Multi-Shot dla B-Roll

Dla każdego wygenerowanego pliku MP3 lektora:
1. Pobieramy dokładny czas trwania: `vo_dur = ffprobe(mp3)`.
2. Obliczamy łączny czas slotu wideo:
   $$\text{target\_video\_dur} = \text{vo\_dur} + 0.80\,\text{s}$$
3. Dodatkowe 0.80 sekundy to bufor na wybrzmienie ostatniej głoski i miękkie cięcie montażowe.

---

## 5. Uruchomienie Skryptu Syntezy

Skrypt [synthesize_voiceovers.py](./scripts/synthesize_voiceovers.py) automatycznie pobiera słownik kwestii, weryfikuje istnienie plików na dysku, generuje brakujące partie i zwraca zestawienie czasów.

```bash
python scripts/synthesize_voiceovers.py --script path/to/script_data.py --out ./voiceovers
```

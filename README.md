# AI Documentary Film Production Skills Suite
### Profesjonalny Zestaw Skilli i Narzędzi Automatyzacji Produkcji Filmów Dokumentalnych dla Agentów AI

Repozytorium zawiera kompletny, przetestowany w warunkach produkcyjnych pakiet skilli dla agentów AI (**Google Antigravity**, **Codex**, **Claude Code**), kodyfikujący standard tworzenia kinowych minidokumentów historycznych i technologicznych.

---

## 🎬 Standard Produkcyjny

Pakiet opiera się na żelaznej metodologii produkcyjnej:
1. **Bezwzględny podział audio**:
   - **A-Roll (Świadek Dziejów)**: 100% natywne audio i doskonały lip-sync z modelu wideo (Google Flow Omni 1.1 Flash). Kategoryczny zakaz dubbingu lektorem na scenach z mówiącym bohaterem.
   - **B-Roll (Przebitki)**: Głęboki, refleksyjny głos lektora z **ElevenLabs Piotr v3** (`eleven_v3`, Voice ID: `gFl0NeqphJUaoBLtWrqM`) z tagami emocjonalnymi (`[thoughtful]`, `[ironic]`, `[pause]`).
2. **Multi-Shot B-Roll (Zero Pętli Wideo)**:
   - Całkowity zakaz zapętlania wideo (`-stream_loop`).
   - Sceny B-roll trwające dłużej niż pojedynczy klip montowane są z **2 do 4 unikalnych ujęć** (plan ogólny, detal, ruch maszyny), przyciętych dokładnie do $t = \text{lektor\_dur} + 0.8\text{s}$.
3. **Polszczyzna Dokumentalna i Odmiana Liczebników**:
   - Rygorystyczny budżet słów dla A-Roll: **maksymalnie 15–18 słów na 10 sekund**.
   - Liczby i daty zapisane w 100% słownie.
   - Bezwzględna poprawność roku 2000: **„w lutym roku dwutysięcznego”** / **„dziesiątego marca roku dwutysięcznego”** (eliminacja zniekształceń do roku 2020).
4. **Broadcast Audio & Dynamiczny Sidechain Ducking**:
   - Ścieżka dialogowa znormalizowana do standardu EBU R128 (`loudnorm=I=-16:TP=-1.5:LRA=7`).
   - Muzyka tła dynamicznie wycisza się o 5–7 dB (`sidechaincompress`) podczas mowy i organicznie narasta w pauzach oddechu.
5. **Napisy Karaoke ASS**:
   - Transkrypcja Whisper STT na czystym dialogu z kalibrowanym offsetem wyprzedzającym **-90ms** (`\k` tags).

---

## 📦 Skład Pakietu Skilli

| Skill | Katalog | Zadanie |
| :--- | :--- | :--- |
| **`documentary-screenplay-architect`** | [`skills/documentary-screenplay-architect`](./skills/documentary-screenplay-architect/SKILL.md) | Projektowanie 5-aktowych scenariuszy, budżet słów (15–18 słów/10s), reguły odmiany dat i liczb, zero klisz AI. |
| **`google-flow-director`** | [`skills/google-flow-director`](./skills/google-flow-director/SKILL.md) | Automatyzacja Google Flow (Playwright/CDP, Omni 1.1 Flash, Veo 2), kotwice wizerunkowe (`Początek`), prompt guard. |
| **`elevenlabs-voiceover-engineer`** | [`skills/elevenlabs-voiceover-engineer`](./skills/elevenlabs-voiceover-engineer/SKILL.md) | Synteza lektora Piotr v3 (`eleven_v3`), tagi emocjonalne, kalkulacja slotów multi-shot, normalizacja audio. |
| **`documentary-editor-master`** | [`skills/documentary-editor-master`](./skills/documentary-editor-master/SKILL.md) | Montaż multi-shot, łączenie osi czasu, sidechain ducking muzyki, generowanie napisów ASS Karaoke (-90ms), render dual master. |
| **`documentary-quality-guard`** | [`skills/documentary-quality-guard`](./skills/documentary-quality-guard/SKILL.md) | 5-etapowy audyt jakościowy (QC Gates): scenariusz, keyword guard, dykcja Whisper STT, inspekcja klatek, synchronizacja. |

---

## 🚀 Szybki Start i Konfiguracja

### 1. Klonowanie i instalacja
Skopiuj repozytorium do katalogu `.agents/skills` w swoim projekcie lub zainstaluj jako plugin w Antigravity IDE:
```bash
git clone https://github.com/RolePlayingTech/documentary-film-skills.git
```

### 2. Konfiguracja sekretów (.env)
Skopiuj plik szablonu i uzupełnij własnymi danymi dostępowymi:
```bash
cp .env.example .env
```

Edytuj plik `.env`:
```env
# Google Flow Credentials
GOOGLE_FLOW_EMAIL="twoj_email@gmail.com"
GOOGLE_FLOW_PASSWORD="twoje_haslo"
GOOGLE_CHROME_REMOTE_DEBUG_PORT="9222"

# ElevenLabs Credentials
ELEVENLABS_API_KEY="sk_twoj_klucz_api"
ELEVENLABS_VOICE_ID="gFl0NeqphJUaoBLtWrqM"
ELEVENLABS_MODEL_ID="eleven_v3"
```

> [!CAUTION]
> Plik `.env` zawiera poufne dane i jest wykluczony w `.gitignore`. **Nigdy nie publikuj ani nie commituj pliku `.env` do publicznych repozytoriów!**

### 3. Wymagania systemowe
* Python 3.10+
* FFmpeg (dodany do zmiennej środowiskowej `PATH`)
* Pakiety Python:
  ```bash
  pip install requests playwright openai-whisper opencv-python numpy
  playwright install chromium
  ```

---

## 🛠 Przykładowy Przepływ Pracy (End-to-End Workflow)

1. **Scenariusz**: Stwórz plik `script_data.py` na podstawie szablonu [script_data_template.py](./skills/documentary-screenplay-architect/examples/script_data_template.py).
2. **Lektor**: Wygeneruj kwestie lektora ElevenLabs:
   ```bash
   python skills/elevenlabs-voiceover-engineer/scripts/synthesize_voiceovers.py --script script_data.py --out ./voiceovers
   ```
3. **Generowanie wideo**: Za pomocą `google-flow-director` wygeneruj surówki A-Roll i B-Roll w Google Flow.
4. **Kontrola jakości surówek**: Zweryfikuj wymiary i brak zająknięć:
   ```bash
   python skills/google-flow-director/scripts/inspect_flow_clip.py ./raw/s01_aroll_raw.mp4 ./qc_frames
   python skills/documentary-quality-guard/scripts/qc_speech_whisper.py ./raw/s01_aroll_raw.mp4
   ```
5. **Montaż i Napisy**: Zmontuj sekwencje multi-shot i wyrenderuj wersje Master:
   ```bash
   python skills/documentary-editor-master/scripts/assemble_multishot.py ./voiceovers/vo_s02.mp3 ./part_s02.mp4 ./raw/s02_a.mp4 ./raw/s02_b.mp4
   python skills/documentary-editor-master/scripts/generate_karaoke_ass.py ./dialog_transcription.json ./subtitles.srt ./karaoke.ass
   python skills/documentary-editor-master/scripts/render_dual_masters.py ./master_raw.mp4 ./music.mp3 ./karaoke.ass 314.0 ./master_clean.mp4 ./master_napisy.mp4
   ```

---

## 📜 Licencja
MIT License © 2026 RolePlayingTech.

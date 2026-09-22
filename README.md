# AI Film & Documentary Production Skills Suite
### Profesjonalny Zestaw Skilli i Narzędzi Automatyzacji Produkcji Filmów dla Agentów AI

Repozytorium zawiera uniwersalny, przetestowany w warunkach produkcyjnych pakiet skilli dla agentów AI (**Google Antigravity**, **Codex**, **Claude Code**), kodyfikujący standard tworzenia kinowych filmów, minidokumentów oraz formatów wertykalnych na social media (TikTok, Reels, Shorts).

---

## 🎬 Kluczowe Możliwości Pakietu

1. **Uniwersalne Style i Gatunki Filmowe**:
   - Filmy dokumentalne i historyczne (Świadek Dziejów, rekonstrukcje, kroniki).
   - Kino Sci-Fi i Cyberpunk (neonowe metropolie, HUD-y, technologia przyszłości).
   - Reklamy produktowe i tech-minimalizm (studio render look, dynamiczne światło).
   - Thriller, Noir i Kryminał (mroczne zaułki, deszcz, kontrasty).
   - High Fantasy i Epika (zamki, magia, krajobrazy).
   - Animacja i Stylized 3D.

2. **Obsługa Formatu Poziomego (16:9) oraz Pionowego (9:16)**:
   - **Natywne 16:9**: Format horyzontalny (1280×720 -> Full HD 1920×1080) na YouTube i ekrany TV.
   - **Natywne 9:16**: Format wertykalny bezpośrednio z Google Flow (`crop_9_16`, 720×1280 -> 1080×1920 Lanczos) bez sztucznych pasów, rozmyć czy przycinania.

3. **Tryby Generowania w Google Flow**:
   - **Z Grafiką Referencyjną (Image-to-Video / Kotwica `Start Frame`)**: Gwarancja 100% tożsamości twarzy bohatera, ubioru oraz spójności rekwizytów.
   - **Bez Grafiki Referencyjnej (Pure Text-to-Video)**: Automatyczne czyszczenie slotu Start Frame, dające pełną swobodę wyobraźni modelowi w ujęciach krajobrazowych i ogólnych.
   - **Safety Policy Guard**: Automatyczne omijanie słów blokowanych przez filtry Google Flow (zamiana słów egzekucyjnych i drastycznych na bezpieczne odpowiedniki kinowe).

4. **Reżyseria Głosu ElevenLabs (Universal Voiceover)**:
   - Wykorzystanie modelu **Eleven v3** (`eleven_v3`) ze znacznikami emocjonalnymi (`[whispers]`, `[ironic]`, `[thoughtful]`, `[pause]`, `[excited]`).
   - Automatyczna kalkulacja długości slotów montażowych ($t_{\text{total}} = t_{\text{vo}} + 0.8\text{s}$).
   - Normalizacja emisyjna EBU R128 (`loudnorm=I=-16:TP=-1.5:LRA=7`).

5. **Zasada Multi-Shot dla B-Roll (Zero Pętli Wideo)**:
   - Kategoryczny zakaz zapętlania wideo (`-stream_loop`). Dłuższe wypowiedzi lektora dzielone są na 2 lub 3 unikalne ujęcia (np. po 5–8 sekund).

6. **Montaż, Sidechain Ducking i Napisy Karaoke ASS**:
   - Płynny, dynamiczny sidechain ducking muzyki pod dialogami i lektorem (-5 do -7 dB).
   - Belka wstępna / Clickbait Hook Card na początku filmu ($t = 0..3.5\text{s}$) z płynnym zanikaniem.
   - Precyzyjnie kalibrowane napisy Karaoke ASS z wyprzedzeniem **-90ms** i układem zoptymalizowanym pod telefony (MarginV 340, krótkie linie) lub monitory (MarginV 90).

---

## 📦 Skład Pakietu Skilli

| Skill | Katalog | Zadanie |
| :--- | :--- | :--- |
| **`google-flow-director`** | [`skills/google-flow-director`](./skills/google-flow-director/SKILL.md) | Uniwersalna automatyzacja Google Flow (16:9 i 9:16, Image-to-Video z kotwicami, Pure Text-to-Video, omijanie filtrów bezpieczeństwa, CDP). |
| **`elevenlabs-voiceover-engineer`** | [`skills/elevenlabs-voiceover-engineer`](./skills/elevenlabs-voiceover-engineer/SKILL.md) | Reżyseria głosu ElevenLabs (Eleven v3, tagi emocjonalne, dobór profili dla różnych gatunków, kalkulacja multi-shot, normalizacja EBU R128). |
| **`documentary-editor-master`** | [`skills/documentary-editor-master`](./skills/documentary-editor-master/SKILL.md) | Montaż dual-format (16:9 & 9:16) w FFmpeg, łączenie multi-shot, sidechain ducking, nakładanie belek hook, napisy Karaoke ASS (-90ms). |
| **`documentary-screenplay-architect`** | [`skills/documentary-screenplay-architect`](./skills/documentary-screenplay-architect/SKILL.md) | Projektowanie scenariuszy dla dowolnych tematów, budżet słów dla A-roll (14–16 słów/10s), reguły zapisu liczb i dat słownie, zero AI-klisz. |
| **`documentary-quality-guard`** | [`skills/documentary-quality-guard`](./skills/documentary-quality-guard/SKILL.md) | 5-etapowy audyt jakościowy (QC Gates): scenariusz, weryfikacja słów kluczowych, dykcja Whisper STT, inspekcja klatek glitch-hunt, synchronizacja. |

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
# Google Flow Credentials & Chrome Debugging
GOOGLE_FLOW_EMAIL="twoj_email@gmail.com"
GOOGLE_FLOW_PASSWORD="twoje_haslo"
GOOGLE_CHROME_REMOTE_DEBUG_PORT="9222"

# ElevenLabs Credentials
ELEVENLABS_API_KEY="sk_twoj_klucz_api"
ELEVENLABS_VOICE_ID="gFl0NeqphJUaoBLtWrqM"
ELEVENLABS_MODEL_ID="eleven_v3"
```

### 3. Wymagania systemowe
* Python 3.10+
* FFmpeg (w zmiennej `PATH`)
* Pakiety Python:
  ```bash
  pip install requests playwright openai-whisper opencv-python numpy
  playwright install chromium
  ```

---

## 🛠 Uniwersalny Przepływ Pracy dla Dowolnego Filmu

1. **Nakreślenie Koncepcji**:
   Wystarczy określić agentowi styl filmu (np. *„Dynamiczny pionowy short 9:16 o tajemnicach głębin oceanicznych w stylu thrillera”* lub *„Monumentalny zwiastun sci-fi 16:9”*).
2. **Generowanie Głosu**:
   `elevenlabs-voiceover-engineer` syntetyzuje kwestie z tagami ekspresji i oblicza dokładne czasy trwania slotów wideo.
3. **Generowanie Wideo w Google Flow**:
   `google-flow-director` przełącza odpowiedni format (16:9 / 9:16), podpina ewentualne kotwice postaci lub czyści slot dla ujęć ogólnych, filtruje słowa zakazane i pobiera surówki.
4. **Automatyczny Montaż i Napisy**:
   `documentary-editor-master` scala ujęcia multi-shot, nakłada dynamicznie duckowany podkład muzyczny, generuje precyzyjnie zsynchronizowane napisy karaoke (-90ms) i renderuje gotowe pliki Clean i Subtitled Master.

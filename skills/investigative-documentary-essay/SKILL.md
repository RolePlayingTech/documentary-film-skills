---
name: investigative-documentary-essay
description: >-
  Use this skill to produce high-production-value investigative documentary essays and video podcasts
  in 16:9 widescreen format (1080p 30fps). It coordinates three visual layers: authentic historical
  archival research, cinematic reconstructions generated in Google Flow (Omni 1.1 Flash), and 10-second
  choreographed HTML/JavaScript motion graphics (Playwright frame rendering). It enforces zero video repeats,
  multi-shot B-roll assembly without loops, calm acoustic audio mixing (-16 LUFS with -0.035 volume sidechain ducking),
  and calibrated Whisper karaoke subtitles.
---

# Investigative Documentary Essay & Podcast Director

Ten skill instruuje agenta AI, jak produkować magnetyzujące, profesjonalne **eseje dokumentalne i podcasty wideo** (np. historie manipulacji marketingowych, zakulisowe śledztwa naukowe, biografie przemysłowe, afery korporacyjne i analizy zjawisk cywilizacyjnych) w klasycznym formacie horyzontalnym 16:9 (1920×1080, 30 kl./s).

W przeciwieństwie do formatu ze Świadkiem Dziejów (gdzie kamera skupia się na gadającej głowie w studio), styl **Investigative Documentary Essay** opiera się na **trójwarstwowym montażu faktograficznym**:
1. **Autentyczne dowody z epoki (Archival Evidence)**: Oryginalne plakaty, etykiety produktów, szyldy, wycinki prasowe i portrety pobrane z wiarygodnych archiwów cyfrowych.
2. **Kinowe rekonstrukcje klimatyczne (OmniFlash B-Roll)**: Żywe, fotorealistyczne sceny tła (ulice, wnętrza, fabryki, laboratoria, postacie w akcji) generowane w Google Flow (Omni 1.1 Flash).
3. **10-sekundowe animacje analityczne (Motion Graphics JS/HTML)**: Dynamiczne plansze infograficzne renderowane w Playwright z autorską choreografią *Centered-to-Left Slide & Staggered Dossier*.

---

## 1. Żelazne Zasady Formatu

1. **Brak „gadającej głowy” (Czysta narracja lektorska)**:
   - Całość narracji prowadzi oficjalny lektor **Piotr v3 (`eleven_v3`)** z ElevenLabs, wykorzystujący bogate tagi ekspresji (`[intrigued]`, `[slightly ironic]`, `[serious]`, `[lower voice]`, `[thoughtful]`).
   - Normalizacja głosu lektora do standardu emisyjnego EBU R128 (`-16 LUFS`, True Peak `-1.5 dB`).
2. **Kategoryczny zakaz powtórzeń ujęć (Zero Video Repeats)**:
   - **Żaden klip wideo ani plansza animowana nie może pojawić się w filmie dwukrotnie**.
   - W 7–8 minutowym dokumencie montujemy około **45–55 unikalnych ujęć** (24 sceny OmniFlash + 15 animacji HTML + 12 plansz archiwalnych).
3. **Zakaz pętli wideo (`-stream_loop`)**:
   - Nigdy nie zapętlamy pojedynczego ujęcia pod dłuższy głos lektora. Każde cięcie montażowe trwa 5.5–10.0 sekund i przechodzi w kolejne, unikalne ujęcie.
4. **Dyskretny, szlachetny podkład muzyczny**:
   - Zero agresywnego sound designu (*whooshe*, przerysowane uderzenia kinowe, sztuczne trzaski).
   - W tle płynie spokojna, elegancka muzyka akustyczna (np. motyw fortepianowo-smyczkowy `Modal Motif.mp3`) ustawiona na bardzo cichym poziomie (`volume=0.035`) z sidechain duckingiem pod głosem lektora.
5. **Długość i rytm animacji (10.0 sekund)**:
   - Każda plansza infograficzna trwa dokładnie **10.0 sekund** (300 klatek przy 30 kl./s), dając widzowi czas na rejestrację plakatu, animację przesunięcia i spokojne przeczytanie faktów.

---

## 2. Architektura Wizualna: Matryca Decyzyjna

Przed przystąpieniem do produkcji agent dzieli każdy wątek scenariusza według ścisłej zasady:

| Warstwa | Co zawiera? | Źródło | Przykłady |
| :--- | :--- | :--- | :--- |
| **Autentyczny Dowód** | Twarde fakty, które widz musi zobaczyć na własne oczy, by uwierzyć | **Internet / Archiwa Cyfrowe** | Plakat Mackiewicza *„Cukier krzepi”* (1931), reklama prasowa Camela z lekarzem (1946), etykieta butelki Radithora z radem, nekrolog Ebena Byersa w *Wall Street Journal* (1932), szyld emaliowany *Bayer Aspirin & Heroin*. |
| **Klimat & Rekonstrukcja** | Sceny żyjącego świata, ruch, emocje, postacie, tło historyczne | **Google Flow (Omni 1.1 Flash)** | Tłum na ulicy Warszawy lat 30., konsylium lekarzy w dymie tytoniowym, matka podająca dziecku syrop łyżeczką, robotnicy rafinerii przekręcający zawór, nowoczesne laboratorium cleanroom, ludzie zapatrzeni w smartfony. |
| **Śledztwo & Analiza** | Lupa inspekcyjna, schematy techniczne, statystyki, paralela Wczoraj vs Dziś | **Motion Graphics HTML/JS** | Analiza manipulacji hasłem reklamowym, przekrój cylindra silnika z licznikiem ofiar, 3 pytania ochronne sceptycyzmu, porównanie Radithora z biohackingiem. |

Szczegółowa matryca: [`references/flow_vs_archive_matrix.md`](./references/flow_vs_archive_matrix.md).

---

## 3. Wyszukiwanie Materiałów Archiwalnych w Internecie

Widz wybaczy modelowi AI drobne niedoskonałości tła, ale natychmiast odrzuci film, jeśli historyczny plakat lub nagłówek prasowy zostanie wygenerowany sztucznie przez AI. Prawdziwe dowody **muszą pochodzić z autentycznych źródeł**.

### Kryteria doboru materiałów:
1. **Wysoka rozdzielczość i czytelność**: Minimum 1000px na krótszym boku (rekomendowane 1600×1200+), pozwalająca na najazd lupą inspekcyjną w 1080p bez pikselizacji.
2. **Brak współczesnych znaków wodnych**: Bezwzględny zakaz grafik z napisami *Getty Images*, *Alamy*, *Shutterstock*.
3. **Autentyczność historyczna**: Oryginalne skany z epoki, patenty, wycinki gazetowe, fotografie muzealne lub aukcyjne.

### Sprawdzone repozytoria i techniki wyszukiwania:
* **Polona (Biblioteka Narodowa)**: Polskie plakaty międzywojenne, afisze, czasopisma (np. *„Wiadomości Literackie”*, kampania Związku Cukrowników).
* **Wikimedia Commons**: Archiwum domeny publicznej w pełnej rozdzielczości (kategorie: *Vintage advertising*, *History of medicine*, *1920s in the United States*).
* **Library of Congress (LOC)**: Amerykańskie plakaty, rejestry patentowe, zdjęcia archiwalne stacji benzynowych i fabryk.
* **Precyzyjny Google Search**:
  - `"Cukier krzepi" plakat Mackiewicz resolution:large`
  - `"More Doctors Smoke Camels" 1946 high resolution filetype:jpg`
  - `"Radithor" original bottle museum`
  - `"The Radium Water Worked Fine" Eben Byers headline 1932`

Pełny poradnik researchu: [`references/archival_research_guide.md`](./references/archival_research_guide.md).

---

## 4. Reżyseria Google Flow (Omni 1.1 Flash)

Sceny filmowe generujemy wyłącznie na modelu **Omni 1.1 Flash** (Veo 2 jest przestarzały i ma mniejszą stabilność fizyki).

### Żelazne reguły promptowania:
1. **Brak gadających postaci (zakaz A-Roll)**: Postacie na ekranie nie powinny mówić prosto do kamery. Mają wykonywać naturalne czynności życiowe (praca, badanie, spacer, palenie, narada).
2. **Format i kadrowanie**: Zawsze natywne 16:9 (`1280×720`, 24 kl./s, 10.00s).
3. **Struktura promptu kinowego**:
   ```text
   Cinematic [rok/epoka] [lokacja], [oświetlenie i atmosfera]. [Konkretne postacie z detalami stroju z epoki] [konkretna fizyczna akcja]. Authentic historical documentary lighting, shallow depth of field, 35mm film grain, 24fps.
   ```
4. **Safety Policy Guard**: Omijanie słów blokowanych (np. zamiast *poison gas* -> *dense industrial chemical vapor*; zamiast *dying agonizing death* -> *grim medical records on hospital desk*).

---

## 5. Choreografia Motion Graphics (10.0s Centered-to-Left Slide)

Każda plansza analityczna w filmie jest samodzielną stroną HTML renderowaną klatka po klatce przez Playwright do formatu MP4 (1920×1080, 30 kl./s, CRF 18).

### Rygor czasowy osi czasu (Timeline):
* **`0.0s – 1.4s` [Wycentrowana ekspozycja]**: Oryginalny plakat/dokument znajduje się w **dokładnym centrum ekranu** (`transform: translateX(510px) scale(1.05)`). Wzrok widza skupia się w 100% na autentycznym dokumencie.
* **`1.4s – 2.8s` [Kinowy ślizg]**: Płynny przesuw na lewą stronę kadru (`easeInOutCubic`) do pozycji docelowej (`translateX(0px) scale(1.0)`).
* **`2.8s – 3.4s` [Tytuł i metadane]**: Wyjazd plakietki z epoką (`badge-tag`) oraz mocnego, prowokacyjnego nagłówka (`main-title`).
* **`3.7s – 5.2s` [Kluczowa statystyka]**: Pojawienie się karty kluczowej z płynnym roll-upem licznika (np. *„0 do 15 OFIAR”* lub *„0 do 113 597 LEKARZY”*).
* **`5.2s – 6.2s` [Kafelki śledcze & cytat]**: Kaskadowe wyjeżdżanie szczegółów manipulacji i puenty.
* **`6.2s – 10.0s` [Komfortowe okno lektury]**: Prawie 4 sekundy stabilnego kadru z subtelnym, „oddychającym” pulsem celownika lupy inspekcyjnej na kluczowym słowie plakatu.

Szczegółowy kod szablonów i matematyka przesunięć: [`references/motion_graphics_choreography.md`](./references/motion_graphics_choreography.md).

---

## 6. Procedura Montażu i Renderowania Mastera

1. **Przygotowanie surówek**:
   - Zsyntetyzuj audio aktów lektora w ElevenLabs (`eleven_v3`, Piotr, znormalizowane do -16 LUFS).
   - Wygeneruj unikalne klipy OmniFlash w `flow_clips/`.
   - Zrenderuj plansze HTML w `motion_graphics_v2/` skryptem [`render_motion_graphics.py`](./scripts/render_motion_graphics.py).
   - Zrenderuj plansze archiwalne skryptem [`render_archival_showcase.py`](./scripts/render_archival_showcase.py).
2. **Kompilacja aktu (Act Assembly)**:
   - Każde ujęcie standaryzujemy do 1920×1080 30fps (`scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080`).
   - Łączymy ujęcia listą concat i miksujemy z audio lektora oraz podkładem muzycznym (`volume=0.035`, `afade=t=in`, `afade=t=out`).
3. **Generowanie Mastera i Wypalanie Napisów Karaoke**:
   - Eksportujemy czysty Master: `SZARLATANI_NAUKI_MASTER_V4_16X9.mp4`.
   - Wypalamy napisy Whisper z kalibracją `-90ms` i czytelnym stylem dokumentalnym (MarginV 38, czarny półprzezroczysty box): `SZARLATANI_NAUKI_MASTER_V4_16X9_NAPISY.mp4`.

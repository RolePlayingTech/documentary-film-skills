# Uniwersalny Przewodnik po Stylach i Reżyserii Głosu ElevenLabs

Ten dokument przedstawia zasady doboru głosu, modeli oraz reżyserii emocjonalnej w ElevenLabs dla różnorodnych gatunków filmowych i formatów wideo.

---

## 1. Wybór Modeli ElevenLabs

| Model | Zastosowanie | Zalety | Obsługa tagów ekspresji |
| :--- | :--- | :--- | :--- |
| **`eleven_v3`** (Eleven Multilingual v3) | Fabuła, dokument, dramat, thriller, kino autorskie | Niezrównana dynamika emocjonalna, naturalne oddechy i pauzy | **TAK** (np. `[whispers]`, `[ironic]`) |
| **`eleven_multilingual_v2`** | Spokojne audiobooki, encyklopedia, instruktaże, e-learning | Niezwykle stabilna intonacja, zerowy dryf tempa | NIE (jednolity ton) |
| **`eleven_turbo_v2_5`** | Szybkie narracje social-media, wiadomości, podcasty | Bardzo szybki czas odpowiedzi i wysoka klarowność | Ograniczona |

---

## 2. Reżyseria Emocjonalna w Modelu Eleven v3

Model `eleven_v3` interpretuje znaczniki emocjonalne umieszczone w tekście, co pozwala precyzyjnie modulować ton aktora:

* `[thoughtful]` – głęboki, analityczny ton, idealny do odkrywania tajemnic lub podsumowywania faktów.
* `[ironic]` – cięta, chłodna ironia, znakomita przy absurdach historii i paradoksach.
* `[whispers]` – intymny, mroczny szept budujący suspens w kryminałach i thrillerach.
* `[pause]` – wymowna pauza dramaturgiczna (0.5–1.0s) przed kluczowym słowem lub puentą.
* `[excited]` – podbicie energii i entuzjazmu, idealne do filmów akcji i wstępów reklamowych.
* `[sighs]` – ciężkie westchnienie wyrażające rezygnację lub zmęczenie bohatera.
* `[chuckles]` – lekki, powściągliwy uśmieszek w głosie podkreślający element humorystyczny.

---

## 3. Dobór Głosu dla Różnych Stylów Filmowych

### A. Klasyczny Dokument i Historia
* **Charakter**: Dojrzały, ciepły, barytonowy, budzący zaufanie autorytet.
* **Rekomendowany profil**: **Piotr** (Voice ID: `gFl0NeqphJUaoBLtWrqM`) lub dojrzały lektor historyczny.
* **Stylistyka tekstu**: Spokojny rytm, obrazowe porównania, subtelne tagi `[thoughtful]` i `[ironic]`.

### B. Sci-Fi / Cyberpunk / AI Narrator
* **Charakter**: Chłodny, precyzyjny, nieco odhumanizowany lub syntetyczny asystent pokładowy.
* **Rekomendowane ustawienia**: Wyższy `stability` (0.75–0.85), niski `similarity_boost` (0.50).
* **Stylistyka tekstu**: Krótkie, bezosobowe frazy techniczne, surowa modulacja.

### C. Dynamiczne Social Media / YouTube Shorts / TikTok
* **Charakter**: Młody, energetyczny, przyciągający uwagę od pierwszych milisekund.
* **Rekomendowane ustawienia**: Niższy `stability` (0.35–0.45) dla dynamicznej melodii głosu.
* **Stylistyka tekstu**: Mocny hook w pierwszych 3 sekundach, tempo około 150–170 słów na minutę.

### D. Thriller / Horror / Mystery
* **Charakter**: Cichy, niski, chropowaty, pełen napięcia.
* **Rekomendowane ustawienia**: Użycie tagów `[whispers]` i częstych `[pause]`.
* **Stylistyka tekstu**: Niedopowiedzenia, krótkie pytania retoryczne.

---

## 4. Zasada Multi-Shot i Czas Trwania

Lektor jest kręgosłupem czasowym sceny B-roll:
1. Mierzymy precyzyjną długość audio: `vo_dur = ffprobe(mp3)`.
2. Wyznaczamy długość sceny wideo:
   $$t_{\text{total}} = \text{vo\_dur} + 0.80\,\text{s}$$
3. Dzielimy $t_{\text{total}}$ na 2 ujęcia (jeśli $t < 18\,\text{s}$) lub 3 ujęcia (jeśli $t \ge 18\,\text{s}$), nigdy nie zapętlając pojedynczego klipu!

---
name: documentary-screenplay-architect
description: >-
  Use this skill to design, format, and audit documentary film screenplays.
  It enforces the 5-act structure, the strict A-Roll (talking witness with 15-18 words/10s limit)
  versus B-Roll (ElevenLabs Piotr v3 narrator) audio split, tactile humanized storytelling without AI clichés,
  and grammatically correct Polish numeral and date inflections (e.g., 'roku dwutysięcznego', never 'dwa tysiące roku').
---

# Documentary Screenplay Architect

Ten skill instruuje agenta, jak tworzyć profesjonalne, angażujące i wolne od błędów scenariusze minidokumentów historycznych, technologicznych i naukowych w formacie:
**Świadek Dziejów (A-Roll 10s z Google Flow) vs Lektor B-Roll (ElevenLabs Piotr v3)**.

---

## Żelazne Reguły Architektury Scenariusza

### 1. Bezwzględny Podział Scen: A-Roll vs B-Roll
* **Sceny A-Roll (Sceny nieparzyste: Świadek Dziejów, bohaterowie)**:
  - Postać zwraca się wprost do kamery lub rozmawia w duecie.
  - **Dźwięk**: 100% natywne audio z modelu Google Flow (Omni 1.1 Flash).
  - **Kategoryczny zakaz**: Nigdy nie nakładaj lektora ElevenLabs na sceny ze Świadkiem!
  - **Budżet słów**: Maksymalnie **15–18 słów** na 10-sekundowe ujęcie. Wypowiedź musi kończyć się w 7.5–8.5 sekundy, zostawiając minimum 1.5 sekundy naturalnej pauzy aktora przed montażowym cięciem.
* **Sceny B-Roll (Sceny parzyste: przebitki, archiwa, detale, krajobrazy)**:
  - Obraz bez widocznej mówiącej twarzy.
  - **Dźwięk**: Lektor ElevenLabs z oficjalnym profilem **Piotr v3** (`eleven_v3`, Voice ID: `gFl0NeqphJUaoBLtWrqM`).
  - **Zasada Multi-Shot**: Zakaz pętli wideo (`-stream_loop`). Jeśli lektor trwa > 10 s, scenę montujemy z 2–4 unikalnych ujęć B-roll (np. Shot A + Shot B + Shot C).

---

## 2. Złota Zasada Języka: Zero AI-Bełkotu i Prawidłowe Daty

### Zakaz pustosłowia AI
Bezwzględnie eliminuj zwroty-klisze:
- ❌ *„Warto zauważyć, że...”*, *„Stanowi to kluczowy element...”*, *„W dobie transformacji cyfrowej...”*, *„Nie tylko... ale również...”*.
- ✅ Zastępuj je namacalnym, soczystym konkretem (np. zamiast *„Superkomputer zużywa gigawaty mocy”* -> *„To pojedyncze pomieszczenie pije tyle prądu, co stotysięczne miasto”*).

### Zasada Liczebników i Dat w Polszczyźnie
Wszystkie liczby, daty i procenty w promptach dialogowych oraz tekstach lektora **muszą być zapisane w 100% słownie**!
* **Dopełniacz roku 2000**:
  - ❌ BŁĄD KARDYNALNY: *„w dwa tysiące roku”*, *„dziesiątego marca dwa tysiące roku”* (powoduje, że lektor mówi *„2020 roku”* lub *„dwa tysiące do roku”*!).
  - ✅ FORMA WZORCOWA: **„w lutym roku dwutysięcznego”**, **„dziesiątego marca roku dwutysięcznego”**.
* **Lata dziewięćdziesiąte**:
  - ✅ *„w tysiąc dziewięćset dziewięćdziesiątym piątym roku”* lub *„w roku tysiąc dziewięćset dziewięćdziesiątym piątym”*.
* Szczegółowy poradnik odmiany: zobacz [numeral_and_date_rules_pl.md](./references/numeral_and_date_rules_pl.md).

---

## 3. Struktura Dramaturgiczna 5 Aktów

1. **Akt I: Inciting Incident (Sceny 01–04)**: Prowokacja, otwarcie w centrum wydarzeń, zderzenie tezy z wątpliwością Świadka.
2. **Akt II: Mechanizm Zjawiska (Sceny 05–08)**: Zrozumienie sedna problemu, anatomia procesu, unikalne przykłady.
3. **Akt III: Punkt Kulminacyjny / Zwrot (Sceny 09–12)**: Kulminacja, bezpośrednie starcie argumentów, symboliczny upadek lub przełom.
4. **Akt IV: Upadek i Konsekwencje (Sceny 13–15)**: Twarde liczby, zgliszcza po katastrofie lub cena zwycięstwa.
5. **Akt V: Filozoficzna Puenta i Epilog (Sceny 16–17)**: Ponadczasowa lekcja dla współczesności, domknięcie klamry kompozycyjnej.

Szczegółowy podręcznik dramaturgii: zobacz [rules_and_dramaturgy.md](./references/rules_and_dramaturgy.md).

---

## 4. Format Danych Scenariusza

Scenariusz przygotowuj jako słownik Python lub plik JSON:
- Zobacz szablon struktury: [screenplay_template.json](./examples/screenplay_template.json).
- Zobacz gotowy plik konfiguracyjny: [script_data_template.py](./examples/script_data_template.py).

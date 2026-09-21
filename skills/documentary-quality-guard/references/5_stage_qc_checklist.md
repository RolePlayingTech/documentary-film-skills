# Checklista 5 Bramek Kontroli Jakości (Quality Control Gates)

Każda produkcja filmowa musi przejść poniższą procedurę przed finalną dystrybucją.

---

## Bramka 1: Audyt Merytoryczny i Dramaturgiczny Scenariusza
* [ ] **Weryfikacja faktów (Fact-Checking)**: Wszystkie daty, nazwiska, nazwy instytucji i traktatów zweryfikowane w minimum dwóch źródłach.
* [ ] **Rygor czasu A-Roll**: Żadna kwestia mówiona postaci w ujęciu 10-sekundowym nie przekracza 15–18 słów.
* [ ] **Reguła liczb i dat**: Wypowiedzi nie zawierają żadnych cyfr arabskich.
* [ ] **Reguła roku 2000**: Dopełniacz roku 2000 ma bezwzględnie postać: *„roku dwutysięcznego”* (NIGDY *„dwa tysiące roku”*).
* [ ] **Zero AI-bełkotu**: Brak pustych klisz językowych; zastosowano soczyste, namacalne metafory.

---

## Bramka 2: Weryfikacja Pobierania z Google Flow
* [ ] **Keyword Guard**: Karta wideo zawiera co najmniej 3 unikalne słowa kluczowe z promptu.
* [ ] **Parametry wideo**: Dokładnie 1280x720, 24 fps, czas trwania 10.00 sekund.

---

## Bramka 3: Audyt Mowy i Dykcji (Whisper STT)
* [ ] Transkrypcja klipu A-Roll nie wykazuje uciętego zdania na granicy 10.0s.
* [ ] Brak zająknięć, powtórzeń słów i obcych głosów w tle.
* [ ] Wypowiedź lektora nie zawiera zniekształceń fonetycznych przy liczbach i datach.

---

## Bramka 4: Wizualna Inspekcja Artefaktów (Visual Glitch Hunt)
* [ ] **Tożsamość Świadka**: Rysy twarzy, zarost, wiek i strój są zgodne z kotwicą referencyjną `swiadek_dziejow.jpg`.
* [ ] **Anatomia**: Brak deformacji dłoni (np. 6 palców, zrośnięte palce) i twarzy.
* [ ] **Geometria rekwizytów**: Brak pływających elementów scenografii, spójna perspektywa.

---

## Bramka 5: Ostateczny Audyt Zmontowanego Mastera
* [ ] **Weryfikacja osi czasu**: Brak zduplikowanych ujęć i przerw w dźwięku.
* [ ] **Napisy Karaoke**: Podświetlenie słów wyprzedza foniczny początek głoski o dokładnie **-90ms**.
* [ ] **Sidechain Ducking**: Muzyka płynnie przycisza się o 5–7 dB podczas mowy i narasta w pauzach oddechu.
* [ ] **Wersje końcowe**: Wygenerowano obie wersje emisyjne (`*_master_clean.mp4` oraz `*_master_napisy.mp4`).

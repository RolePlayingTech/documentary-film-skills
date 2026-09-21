---
name: google-flow-director
description: >-
  Use this skill to automate, direct, and verify video generation in Google Flow (Omni 1.1 Flash and Veo 2).
  It manages browser automation (Playwright/CDP), visual character anchors ('Początek' / Start Frame slot),
  16:9 cinematic aspect ratios, prompt formatting with quoted Polish dialogues, keyword verification guards,
  and video clip parameter validation (1280x720, 24fps, 10.00s).
---

# Google Flow Director

Ten skill instruuje agenta, jak bezawaryjnie sterować generatorem wideo Google Flow (model Omni 1.1 Flash oraz Veo 2), zarządzać tożsamością wizualną postaci, wysyłać prompty i pobierać gotowe surówki.

---

## 1. Wymagania i Konfiguracja Środowiska

Do automatyzacji Google Flow wymagane są zmienne z pliku `.env`:
* `GOOGLE_FLOW_EMAIL` – email do konta Google.
* `GOOGLE_FLOW_PASSWORD` – hasło do konta Google.
* `GOOGLE_CHROME_REMOTE_DEBUG_PORT` – port zdalnego debugowania (domyślnie `9222`).

Zalecana metoda połączenia:
Uruchomienie przeglądarki Chrome z aktywną sesją Google:
```bash
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\ChromeProfile"
```
Skrypt [flow_client.py](./scripts/flow_client.py) podłącza się do aktywnej sesji przez Chrome DevTools Protocol (CDP), co omija blokady anty-botowe i 2FA.

---

## 2. Standard Konfiguracji Projektu Flow

Każdy projekt dokumentalny musi mieć ustawione parametry:
1. **Model**: **Omni 1.1 Flash** (dla A-Roll z mową i lip-syncem) lub **Veo 2** (dla ujęć kinowych B-Roll).
2. **Format kadru**: **16:9** (Widescreen 1280x720).
3. **Czas trwania**: 10.00 sekund (240 klatek przy 24 fps).

---

## 3. Żelazna Reguła Kotwicy Wizualnej (`Początek` / Start Frame)

Aby twarz Świadka Dziejów nie zmieniała się między scenami (tzw. dryf postaci AI):
1. **Bezwzględny obowiązek**: Każde ujęcie A-Roll ze Świadkiem musi mieć podpiętą klatkę referencyjną do slotu **`Początek`** (Start Frame).
2. Plik kotwicy (`swiadek_dziejow.jpg`) wgrywamy do zasobów projektu i wybieramy przez picker klatek.
3. Kategoryczny zakaz generowania scen dialogowych z samego opisu tekstowego!

---

## 4. Wzorzec Promptowania A-Roll

W prompcie wideo dla Omni Flash kwestia dialogowa **musi być ujęta w cudzysłów i oznaczona jako język polski**:

```text
16:9 cinematic medium shot in an industrial loft in 1999. On the right stands the Charismatic Witness (mature 45yo man, salt-and-pepper beard, simple linen shirt, reference anchor face). He speaks in Polish: "Treść wypowiedzi do osiemnastu słów zapisana w cudzysłowie." with natural expressive Polish lip-sync and authority. Fixed camera with subtle slow push-in, edge-to-edge 16:9, authentic 35mm film look.
```

Więcej gotowych wzorców promptów: zobacz [prompt_patterns.md](./references/prompt_patterns.md).

---

## 5. Procedura Pobierania i Bramka Kontrolna (Keyword Guard)

1. **Keyword Guard**: Przed kliknięciem pobierania skrypt sprawdza okno szczegółów karty wideo – musi ono zawierać minimum 3 unikalne słowa kluczowe ze zadanego promptu.
2. **Weryfikacja parametrów**: Po pobraniu plik jest sprawdzany skryptem [inspect_flow_clip.py](./scripts/inspect_flow_clip.py):
   - Wymiary: dokładnie 1280x720
   - FPS: 24.0 fps
   - Czas trwania: dokładnie 10.00 s (min. 240 klatek)
   - Ekstrakcja 3 klatek inspekcyjnych (1s, 5s, 9s) do audytu glitchy.

Szczegółowy przewodnik po selektorach UI: zobacz [flow_selectors_guide.md](./references/flow_selectors_guide.md).

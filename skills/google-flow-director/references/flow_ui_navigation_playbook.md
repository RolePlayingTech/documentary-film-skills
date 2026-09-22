# Przewodnik po Nawigacji i Automatyzacji Interfejsu Google Flow (VideoFX)

Kompletny, techniczny manual poruszania się po interfejsie Google Flow (Omni 1.1 Flash & Veo 2) przy użyciu Playwright i Chrome DevTools Protocol (CDP).

---

## 1. Architektura i Konfiguracja Połączenia CDP

Google Flow wymaga zalogowanego konta Google i posiada zaawansowane mechanizmy Cloudflare/Bot-detection. Z tego względu automatyzacja opiera się na **podłączeniu do uruchomionej przeglądarki Chrome z aktywną sesją użytkownika**.

### Uruchomienie Chrome z portem debugowania (Windows):
```powershell
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\ChromeProfile"
```
Adres projektu w Google Flow:
`https://flow.google.com/project/<project-id>`

### Połączenie Playwright przez CDP:
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    context = browser.contexts[0]
    # Wyszukanie karty z Flow
    page = next((pg for pg in context.pages if "flow.google.com" in pg.url or "labs.google/fx" in pg.url), context.pages[0])
```

---

## 2. Sterowanie Formatem Obrazu: Poziom (16:9) vs Pion (9:16)

Google Flow domyślnie tworzy klipy w formacie 16:9 (`1280×720`). Aby wygenerować natywne wideo pionowe 9:16 (`720×1280`) na telefony (TikTok, YouTube Shorts, Instagram Reels), należy przełączyć tryb w menu ustawień dolnego paska.

### Selektory i Procedura:
1. **Trigger Ustawień**: Przycisk na prawym krańcu paska wprowadzania promptu:
   - Selektor: `button.settings-trigger-button, button[aria-label='Settings trigger']`
   - Tekst na przycisku zawiera aktualny stan, np. `Video • 720p • 10s • 16:9 x1` lub `... 9:16 x1`.
2. **Weryfikacja i Przełączenie**:
   ```python
   def set_aspect_ratio(page, target="9:16"):
       page.keyboard.press("Escape")
       btn = page.locator("button.settings-trigger-button, button[aria-label='Settings trigger']").first
       txt = btn.inner_text().strip()
       
       # Jeśli format nie odpowiada oczekiwanemu
       if target not in txt and target.replace(":", "_") not in txt:
           btn.click(force=True)
           time.sleep(1)
           # Kliknij przycisk formatu w menu podręcznym
           opt = page.locator(f"button:has-text('{target}'), [role='button']:has-text('{target}')").first
           if opt.is_visible():
               opt.click(force=True)
               time.sleep(1)
           page.keyboard.press("Escape")
           time.sleep(0.5)
   ```

---

## 3. Generowanie z Grafikami Referencyjnymi (Image-to-Video / Kotwice)

Wykorzystywane, gdy film wymaga:
- **Spójności postaci**: Ta sama twarz, ubiór i cechy bohatera w kolejnych scenach.
- **Wierności rekwizytów lub lokacji**: Konkretne wnętrze, mapa, budynek czy artefakt.

### Procedura Przypinania do slotu Start (Początek):
1. **Otwarcie pickera**:
   - Selektor: `button:has-text('Start'), [role='button']:has-text('Start')` (wybieramy `.last`, aby celować w dolny pasek tworzenia).
2. **Wyszukanie zasobu w projekcie**:
   - Pole wyszukiwania: `input[placeholder*='Search assets'], input[placeholder*='Szukaj']`
   - Wpisujemy nazwę pliku lub jej prefix i czekamy 1.5–2 sekundy na przefiltrowanie siatki.
3. **Wybór kafelka i dodanie do promptu**:
   - Kafelek zasobu: `button.asset-item:has-text('<nazwa>')` lub `button.asset-item` (pierwszy wynik).
   - Kliknięcie w kafelek otwiera boczny panel szczegółów.
   - W panelu klikamy: `button.detail-add-to-prompt-btn, button:has-text('Add to prompt'), button:has-text('Dodaj do promptu')`.
4. **Zamknięcie szuflady**:
   - Wysyłamy klawisz `Escape` (`page.keyboard.press('Escape')`), aby powrócić do widoku głównego.

---

## 4. Generowanie bez Grafik Referencyjnych (Pure Text-to-Video)

Wykorzystywane dla:
- Abstrakcyjnych krajobrazów, ujęć natury, szerokich panoram miejskich, dynamicznych ujęć akcji, ujęć makro, stylizacji sci-fi/fantasy, gdzie model ma pełną swobodę wyobraźni.

### ⚠️ Krytyczna zasada: Czysty Slot Start Frame!
Jeśli w slocie `Start` pozostała miniatura z poprzedniej sceny, model **bezwzględnie potraktuje ją jako klatkę wyjściową**! Spowoduje to nałożenie niepożądanej postaci lub stylu na nowy prompt.

### Procedura Usuwania Poprzedniej Kotwicy:
```python
def clear_start_anchor(page):
    remove_btn = page.locator(".mat-mdc-chip-remove, button[aria-label*='Remove'], [role='button'][aria-label*='remove'], button:has-text('close')").first
    if remove_btn.is_visible():
        remove_btn.click(force=True)
        time.sleep(1)
```

---

## 5. Wprowadzanie Promptu i Uruchomienie Generacji

Interfejs Google Flow korzysta z edytora `div[contenteditable='true']`, a nie klasycznego `textarea`.

### Prawidłowe wpisywanie:
Metoda `.fill()` w Playwright może nie wywołać zdarzeń klawiatury dla `contenteditable`. Należy stosować:
```python
prompt_input = page.locator("div[contenteditable='true']").first
prompt_input.click(force=True)
time.sleep(0.2)
# Wyczyszczenie pola
page.keyboard.press("Control+A")
page.keyboard.press("Backspace")
time.sleep(0.2)
# Wpisanie tekstu z naturalnym opóźnieniem
page.keyboard.type(prompt_text, delay=5)
time.sleep(1)

# Kliknięcie strzałki zatwierdzenia
submit_btn = page.locator("button:has-text('arrow_forward')").first
submit_btn.click(force=True)
```

---

## 6. Monitorowanie Postępu i Obsługa Błędów Polityki Bezpieczeństwa

Czas generacji 10-sekundowego klipu wynosi zazwyczaj **35–50 sekund**.

### Cykl Życia Karty:
1. **Inicjalizacja (0–10s)**: Karta pojawia się na płótnie z ikoną ładowania.
2. **Rendering (10–45s)**: Na karcie widoczny jest wskaźnik procentowy: `text=/%/` (np. `4%`, `18%`, `33%`, `100%`).
3. **Zakończenie**: Po osiągnięciu 100% wskaźnik procentowy znika, a karta staje się aktywnym wideo.

### 🚫 Tabela Słów Zakazanych (Filtry Bezpieczeństwa Google Flow) i Bezpieczne Odpowiedniki:
Google Flow automatycznie blokuje generacje, jeśli prompt zawiera słowa kojarzące się z przemocą, śmiercią, egzekucją czy bronią:

| Słowo zakazane (Policy Violation) | Bezpieczny kinowy zamiennik |
| :--- | :--- |
| `gallows` / `hanging` / `szubienica` | `timber magistrate platform`, `historic town pillory` |
| `executioner` / `kat` | `solemn bailiff`, `court official in medieval garb` |
| `corpse` / `dead body` / `trup` | `mummified historical figure`, `ancient relic on display` |
| `burning pyre` / `stos` | `central stone judicial pillar with lanterns and glowing embers` |
| `bloody sword` / `blood` | `ceremonial steel blade reflecting warm candlelight` |
| `severed fingers` / `mutilation` | `official stripping of ceremonial rings and emblems` |

W przypadku natrafienia na błąd:
Karta wyświetla komunikat: `Failed: This generation might violate our policies`.
Skrypt automatyzacji powinien natychmiast wykryć ten selektor (`text=/violate our policies|Failed/i`) i przerwać oczekiwanie, sygnalizując konieczność zmiany słownictwa.

---

## 7. Pobieranie Gotowego Klipu i Integracja z CDP

W trybie CDP przeglądarka Chrome pobiera pliki do domyślnego folderu pobierania użytkownika (`~/Downloads/`).
Plik z Flow jest spakowany jako archiwum `.zip` zawierające właściwe wideo `.mp4`.

### Stabilny Mechanizm Przechwytywania:
1. Przed kliknięciem zapamiętujemy najnowszy plik ZIP w `~/Downloads/`.
2. Klikamy przycisk pobierania w Flow:
   `button[aria-label*='Download'], button:has-text('download')`
3. Oczekujemy w pętli (do 30 sekund) na pojawienie się nowego pliku ZIP o rozmiarze > 100 KB.
4. Rozpakowujemy archiwum i wyodrębniamy `.mp4` do folderu docelowego.
5. Weryfikujemy parametry techniczne (OpenCV/FFprobe):
   - Dla 16:9: dokładnie **1280×720**, 24.00 fps, min. 200 klatek.
   - Dla 9:16: dokładnie **720×1280**, 24.00 fps, min. 200 klatek.

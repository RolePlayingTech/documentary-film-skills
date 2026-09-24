# Architektura i Choreografia Motion Graphics (10.0s Centered-to-Left)

Tradycyjne programy montażowe (After Effects, Premiere) wymagają wielogodzinnego ręcznego ustawiania klatek kluczowych i są trudne do zautomatyzowania przez agentów AI. 

W tym standardzie każda plansza infograficzna jest **samodzielną aplikacją internetową (HTML5/CSS3/JavaScript)** renderowaną w Playwright klatka po klatce (300 klatek przy 30 fps = dokładnie 10.00 sekund) bezpośrednio do potoku FFmpeg.

Gwarantuje to:
* **Idealną ostrość wektorową typografii** w rozdzielczości Full HD (1920×1080) i 4K.
* **100% determinizm czasowy**: funkcja `window.renderAtMs(ms)` pozwala wyrenderować dowolny moment bez utraty synchronizacji z głosem lektora.
* **Zaawansowane efekty inspekcyjne**: celowniki optyczne, lupy powiększające detale, liczniki cyfrowe, animacje wektorowe SVG.

---

## 1. Matematyka Przesunięcia Centered-to-Left

Kluczowy błąd początkujących twórców polega na wyświetlaniu plakatu od razu po lewej stronie ekranu. Sprawia to, że wzrok widza błądzi po pustej prawej stronie kadru. 

W autorskiej choreografii **Centered-to-Left**:
1. Plakat pojawia się **na samym środku ekranu** w delikatnym powiększeniu.
2. Gdy widz zarejestruje oryginalny dokument, następuje kinowy ślizg w lewo.
3. W zwolnionej przestrzeni po prawej stronie kaskadowo wyjeżdżają kafelki śledcze.

### Obliczenia CSS Transform dla kadru 1920×1080:
* **Szerokość sceny roboczej (`.stage`)**: `1740px` (marginesy boczne po `90px`).
* **Szerokość lewego boksu plakatowego (`.poster-box`)**: `720px`.
* Domyślny środek geometryczny lewego boksu w układzie Flexbox wynosi:
  $$\text{Center}_{\text{default}} = 90\text{px} + \frac{720\text{px}}{2} = 450\text{px}$$
* Środek ekranu wynosi dokładnie:
  $$\text{Center}_{\text{screen}} = \frac{1920\text{px}}{2} = 960\text{px}$$
* Wymagane przesunięcie w osi X, aby plakat znalazł się idealnie w centrum ekranu:
  $$\Delta X = 960\text{px} - 450\text{px} = 510\text{px}$$

Dlatego początkowy stan transformacji plakatu wynosi:
`transform: translateX(510px) scale(1.05);`

---

## 2. Żelazna Oś Czasu (Pacing Timeline 10.0s)

| Czas (ms) | Faza | Co widzi widz? | Transformacja i parametry |
| :--- | :--- | :--- | :--- |
| **`0 – 1400 ms`** | **Faza 1: Autentyczność** | Plakat na środku ekranu. Widz skupia się na oryginalnym dokumencie. | `translateX(510px) scale(1.05)` |
| **`1400 – 2800 ms`** | **Faza 2: Kinowy Ślizg** | Płynny ruch w lewo z krzywą wygładzania `easeInOutCubic`. | Od `510px` do `0px`, skala od `1.05` do `1.00`. |
| **`2800 – 3400 ms`** | **Faza 3A: Identyfikacja** | Wyjazd plakietki z epoką (`badge-tag`) i głównego nagłówka (`main-title`). | `opacity: 0 -> 1`, `translateX(30px -> 0px)`. |
| **`3700 – 5200 ms`** | **Faza 3B: Skala Zjawiska** | Wjazd hero-karty i dynamiczny roll-up licznika numerycznego. | Od `0` do `15 OFIAR` lub `0` do `113 597 LEKARZY`. |
| **`5200 – 6200 ms`** | **Faza 3C: Detale i Puenta** | Staggered rollout kafelków faktograficznych i dolnej belki z cytatem. | Opóźnienia kaskadowe po `300-500ms`. |
| **`6200 – 10000 ms`** | **Faza 4: Czas na Refleksję** | Prawie 4 sekundy spokojnego okna lektury z subtelnym „oddychaniem” celownika lupy. | Lupa: `sin(t) * 5px`, pełna stabilność tekstu. |

---

## 3. Matematyczne Krzywe Easingu (Funkcje w JS)

Do deterministycznego renderowania stosujemy czysty kod JavaScript bez zewnętrznych bibliotek (zero zależności):

```javascript
// Płynny start i płynne hamowanie (dla przesunięcia głównego boksu)
function easeInOutCubic(t) {
  return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
}

// Dynamiczny wjazd i miękkie lądowanie (dla kafelków i napisów)
function easeOutCubic(t) {
  return 1 - Math.pow(1 - t, 3);
}
```

---

## 4. Implementacja Lupy Inspekcyjnej (Reticle / Crosshair)

Aby podkreślić konkretne słowo na plakacie (np. napis *„Cukier”*, *„Heroin”*, strefę *„T-Zone”* lub słowo *„Ethyl”*), na plakat nakładamy warstwę lupy:

```html
<div class="poster-box" id="poster-box">
  <img src="plakat.jpg" class="poster-img">
  
  <!-- Lupa inspekcyjna -->
  <div class="loupe" id="loupe">
    <svg class="loupe-crosshair" viewBox="0 0 100 100">
      <circle cx="50" cy="50" r="46" fill="none" stroke="#f59e0b" stroke-width="2.5" stroke-dasharray="6,4"/>
      <line x1="50" y1="10" x2="50" y2="35" stroke="#f59e0b" stroke-width="2"/>
      <line x1="50" y1="65" x2="50" y2="90" stroke="#f59e0b" stroke-width="2"/>
      <line x1="10" y1="50" x2="35" y2="50" stroke="#f59e0b" stroke-width="2"/>
      <line x1="65" y1="50" x2="90" y2="50" stroke="#f59e0b" stroke-width="2"/>
    </svg>
    <div class="loupe-tag">ANALIZA SLOGANU</div>
  </div>
</div>
```

W funkcji `renderAtMs(ms)` lupa może delikatnie przesuwać się wzdłuż badanego hasła:
```javascript
if (ms > 400) {
  loupe.style.opacity = '1';
  let curY = 380;
  if (ms > 1400) {
    const lProg = Math.min(1, (ms - 1400) / 1800);
    curY = 380 + (500 - 380) * easeInOutCubic(lProg);
  }
  // Subtelne kinowe oddychanie po zakończeniu wjazdu
  if (ms > 6000) {
    curY += Math.sin((ms - 6000) / 500) * 4;
  }
  loupe.style.top = `${curY}px`;
}
```

---

## 5. Renderowanie Klatka po Klatce do FFmpeg

Do renderingu stosujemy Playwright w trybie headless, który steruje wirtualnym czasem i przekazuje klatki JPEG bezpośrednio do strumienia `stdin` FFmpeg:

```python
ffmpeg_cmd = [
    "ffmpeg", "-y",
    "-f", "image2pipe",
    "-vcodec", "mjpeg",
    "-r", "30",
    "-i", "-",
    "-c:v", "libx264",
    "-preset", "fast",
    "-crf", "18",
    "-pix_fmt", "yuv420p",
    output_mp4
]
proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.goto(html_file_url)
    
    total_frames = 300 # 10.0s @ 30fps
    for f in range(total_frames):
        t_ms = f * (1000.0 / 30.0)
        page.evaluate(f"window.renderAtMs({t_ms})")
        jpeg_bytes = page.screenshot(type="jpeg", quality=95)
        proc.stdin.write(jpeg_bytes)

proc.stdin.close()
proc.wait()
```
Taka metoda eliminuje jakiekolwiek przycięcia, gwarantuje idealne 30.00 kl./s i wagę pliku rzędu 1–2 MB przy bezstratnej jakości tekstu.

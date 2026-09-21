# Przewodnik po Selektorach UI Google Flow (Playwright / DOM)

Ten dokument zawiera mapę selektorów DOM interfejsu Google Flow (VideoFX), niezbędną do stabilnej automatyzacji bez polegania na współrzędnych ekranu.

---

## 1. Wybór Formatów i Modeli
* **Przełącznik Aspect Ratio 16:9**:
  `button:has-text('16:9'), [aria-label*='16:9']`
* **Wybór Modelu Wideo (Omni 1.1 Flash / Veo 2)**:
  `button:has-text('Omni 1.1 Flash'), button:has-text('Veo 2')`
* **Przełącznik trybu Wideo**:
  `button:has-text('Wideo'), button:has-text('Video')`

---

## 2. Zarządzanie Kotwicami Wizerunkowymi (Początek / Start Frame)
* **Przycisk slotu Początek**:
  `button:has-text('Początek'), button:has-text('Start')`
* **Przycisk dodania klatki (plus)**:
  `button:has(mat-icon:has-text('add'))`
* **Wyszukiwarka w oknie wyboru zasobów**:
  `input[placeholder*='Szukaj'], input[placeholder*='Search']`
* **Usunięcie klatki z promptu**:
  `button:has(mat-icon:has-text('close')), [aria-label*='Remove frame']`

---

## 3. Pole Promptu i Zatwierdzanie
* **Pole tekstowe promptu**:
  `textarea[placeholder*='Prompt'], textarea, [contenteditable='true']`
* **Przycisk wysyłki (Generuj / Strzałka)**:
  `button:has(mat-icon:has-text('arrow_forward')), button:has-text('Utwórz')`

---

## 4. Karty Wyników i Pobieranie
* **Karty wygenerowanych ujęć**:
  `.video-card, [role='article'], .generation-card`
* **Przycisk menu pobierania**:
  `button:has(mat-icon:has-text('download')), [aria-label*='Pobierz'], [aria-label*='Download']`
* **Szczegóły karty (Keyword Guard)**:
  `.prompt-text, .card-details, .modal-prompt-content`

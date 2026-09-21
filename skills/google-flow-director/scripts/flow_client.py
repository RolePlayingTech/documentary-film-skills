"""
Klient automatyzacji Google Flow przez Playwright / CDP.
Obsługuje podłączenie do aktywnej sesji Chrome, przypinanie kotwic wizerunkowych,
wysyłanie promptów, oczekiwanie na zakończenie generacji i pobieranie gotowych klipów.
"""

import os
import sys
import time
import subprocess
from playwright.sync_api import sync_playwright

CDP_PORT = os.getenv("GOOGLE_CHROME_REMOTE_DEBUG_PORT", "9222")

def get_flow_page(playwright):
    """Podłącza się do uruchomionego Chrome przez port CDP."""
    endpoint = f"http://127.0.0.1:{CDP_PORT}"
    try:
        browser = playwright.chromium.connect_over_cdp(endpoint)
        context = browser.contexts[0]
        # Znajdź kartę z Google Flow / VideoFX
        for page in context.pages:
            if "labs.google/fx" in page.url or "flow" in page.url:
                return page
        # Jeśli nie znaleziono, zwróć pierwszą aktywną
        return context.pages[0] if context.pages else context.new_page()
    except Exception as e:
        print(f"Błąd połączenia z CDP na porcie {CDP_PORT}: {e}")
        print("Upewnij się, że Chrome jest uruchomiony z flagą --remote-debugging-port=9222")
        return None

def clear_anchor(page):
    """Usuwa wcześniej przypiętą kotwicę z prompt boxa."""
    close_btns = page.locator("button:has(mat-icon:has-text('close')), button:has(mat-icon:has-text('cancel')), [aria-label*='Remove frame']")
    for _ in range(2):
        cnt = close_btns.count()
        for i in range(cnt):
            try:
                close_btns.nth(i).click(force=True)
                time.sleep(0.3)
            except Exception:
                pass
        time.sleep(0.3)

def set_start_anchor(page, anchor_name):
    """Przypina klatkę referencyjną do slotu Początek (Start Frame)."""
    page.keyboard.press("Escape")
    time.sleep(0.3)
    clear_anchor(page)

    start_btn = page.locator("button:has-text('Początek'), button:has-text('Start')").first
    if not start_btn.is_visible():
        add_btn = page.locator("button:has(mat-icon:has-text('add'))").last
        if add_btn.is_visible():
            add_btn.click(force=True)
            time.sleep(0.8)
        start_btn = page.locator("button:has-text('Początek'), button:has-text('Start')").first

    if not start_btn.is_visible():
        print(f"Nie znaleziono przycisku wyboru Początek dla {anchor_name}")
        return False

    start_btn.click(force=True)
    time.sleep(1.2)

    # Wyszukaj kotwicę w pickerze
    search_inp = page.locator("input[placeholder*='Szukaj'], input[placeholder*='Search']").first
    if search_inp.is_visible():
        clean_name = anchor_name.split(".")[0][:14]
        search_inp.fill(clean_name)
        time.sleep(1.0)

    item = page.locator(f"button:has-text('{anchor_name}'), [role='option']:has-text('{anchor_name}'), .asset-item").first
    if item.is_visible():
        item.click(force=True)
        time.sleep(1.0)
        print(f"Przypięto kotwicę: {anchor_name}")
        return True
    return False

def submit_prompt(page, prompt_text):
    """Wpisuje prompt i zatwierdza generowanie."""
    textarea = page.locator("textarea[placeholder*='Prompt'], textarea, [contenteditable='true']").first
    textarea.click()
    page.keyboard.press("Control+A")
    page.keyboard.press("Backspace")
    time.sleep(0.3)

    textarea.fill(prompt_text)
    time.sleep(0.5)

    submit_btn = page.locator("button:has(mat-icon:has-text('arrow_forward')), button:has-text('Utwórz'), button:has-text('Generate')").first
    if submit_btn.is_visible():
        submit_btn.click(force=True)
        print("Prompt wysłany do kolejki Flow.")
        return True
    return False

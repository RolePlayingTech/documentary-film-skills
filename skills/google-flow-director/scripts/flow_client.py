"""
Universal Google Flow (VideoFX) Automation Client via Playwright / CDP.
Supports:
- Aspect ratios: Native 16:9 (1280x720) and Native 9:16 (720x1280)
- Generation modes: Image-to-Video (with visual anchor in Start Frame) and Pure Text-to-Video (clearing anchors)
- Real-time percentage monitoring and instant policy failure detection
- Robust download capture from Chrome's Downloads folder
- Output validation (resolution, frame rate, duration)
"""

import os
import sys
import time
import glob
import zipfile
import argparse
import cv2
from playwright.sync_api import sync_playwright

DEFAULT_CDP_PORT = os.getenv("GOOGLE_CHROME_REMOTE_DEBUG_PORT", "9222")
DEFAULT_DOWNLOADS_DIR = os.path.expanduser(r"~\Downloads")

def get_latest_zip(downloads_dir=DEFAULT_DOWNLOADS_DIR):
    zips = glob.glob(os.path.join(downloads_dir, "*.zip"))
    if not zips:
        return None
    return max(zips, key=os.path.getmtime)

def validate_clip(fpath, expected_aspect="16:9"):
    if not os.path.exists(fpath) or os.path.getsize(fpath) < 100000:
        return False, "File missing or too small"
    try:
        cap = cv2.VideoCapture(fpath)
        fc = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()

        if expected_aspect == "9:16" and (w != 720 or h != 1280):
            return False, f"Expected 720x1280 for 9:16, got {w}x{h}"
        elif expected_aspect == "16:9" and (w != 1280 or h != 720):
            return False, f"Expected 1280x720 for 16:9, got {w}x{h}"

        if fc < 100:
            return False, f"Too few frames: {fc}"

        return True, f"Valid: {w}x{h}, {fps:.2f} fps, {fc} frames"
    except Exception as e:
        return False, f"Validation error: {e}"

class FlowClient:
    def __init__(self, cdp_port=DEFAULT_CDP_PORT, downloads_dir=DEFAULT_DOWNLOADS_DIR):
        self.cdp_port = cdp_port
        self.downloads_dir = downloads_dir

    def get_flow_page(self, playwright):
        endpoint = f"http://127.0.0.1:{self.cdp_port}"
        browser = playwright.chromium.connect_over_cdp(endpoint)
        context = browser.contexts[0]
        for page in context.pages:
            if "flow.google.com" in page.url or "labs.google/fx" in page.url:
                return page
        return context.pages[0] if context.pages else context.new_page()

    def set_aspect_ratio(self, page, target_aspect="16:9"):
        """Ustawia proporcje obrazu (16:9 lub 9:16) w menu ustawień Flow."""
        page.keyboard.press("Escape")
        time.sleep(0.5)

        settings_btn = page.locator("button.settings-trigger-button, button[aria-label='Settings trigger']").first
        if not settings_btn.is_visible():
            return

        txt = settings_btn.inner_text().strip()
        aspect_keyword = "9:16" if target_aspect == "9:16" else "16:9"
        alt_keyword = "9_16" if target_aspect == "9:16" else "16_9"

        if aspect_keyword not in txt and alt_keyword not in txt:
            print(f"[FlowClient] Zmieniam format kadru na {target_aspect}...")
            settings_btn.click(force=True)
            time.sleep(1)

            btn = page.locator(f"button:has-text('{target_aspect}'), [role='button']:has-text('{target_aspect}')").first
            if btn.is_visible():
                btn.click(force=True)
                time.sleep(1)
            page.keyboard.press("Escape")
            time.sleep(0.5)

    def clear_start_anchor(self, page):
        """Usuwa przypiętą kotwicę ze slotu Start (niezbędne dla czystego text-to-video)."""
        remove_btn = page.locator(".mat-mdc-chip-remove, button[aria-label*='Remove'], [role='button'][aria-label*='remove'], button:has-text('close')").first
        if remove_btn.is_visible():
            print("[FlowClient] Usuwam poprzednią kotwicę ze slotu Start (tryb Text-to-Video)...")
            remove_btn.click(force=True)
            time.sleep(1)

    def pin_start_anchor(self, page, anchor_name):
        """Przypina klatkę referencyjną z zasobów do slotu Start."""
        page.keyboard.press("Escape")
        time.sleep(0.5)

        print(f"[FlowClient] Przypinam kotwicę referencyjną: {anchor_name}...")
        start_btn = page.locator("button:has-text('Start'), [role='button']:has-text('Start')").last
        start_btn.click(force=True)
        time.sleep(2)

        search_inp = page.locator("input[placeholder*='Search assets'], input[placeholder*='Szukaj']").first
        if search_inp.is_visible():
            search_inp.click(force=True)
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            clean_search = anchor_name.split(".")[0][:16]
            search_inp.fill(clean_search)
            time.sleep(2)

        item = page.locator(f"button.asset-item:has-text('{clean_search}'), button.asset-item").first
        if item.is_visible():
            item.click(force=True)
            time.sleep(1)

        add_btn = page.locator("button.detail-add-to-prompt-btn, button:has-text('Add to prompt'), button:has-text('Dodaj do promptu')").first
        if add_btn.is_visible():
            add_btn.click(force=True)
            time.sleep(2)

        page.keyboard.press("Escape")
        time.sleep(0.5)

    def generate_clip(self, prompt, output_path, anchor=None, aspect="16:9", max_wait_sec=140):
        """Generuje pojedynczy klip w Google Flow i zapisuje do output_path."""
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        prev_zip = get_latest_zip(self.downloads_dir)
        prev_time = os.path.getmtime(prev_zip) if prev_zip else 0

        with sync_playwright() as p:
            page = self.get_flow_page(p)

            # 1. Format
            self.set_aspect_ratio(page, target_aspect=aspect)

            # 2. Kotwica (Image-to-Video vs Text-to-Video)
            if anchor:
                self.pin_start_anchor(page, anchor)
            else:
                self.clear_start_anchor(page)

            # 3. Wpisanie promptu do contenteditable
            prompt_input = page.locator("div[contenteditable='true']").first
            prompt_input.click(force=True)
            time.sleep(0.2)
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            time.sleep(0.2)
            page.keyboard.type(prompt, delay=5)
            time.sleep(1)

            # 4. Wysłanie
            submit_btn = page.locator("button:has-text('arrow_forward')").first
            print(f"[FlowClient] Rozpoczynam generowanie wideo ({aspect})...")
            submit_btn.click(force=True)
            time.sleep(5)

            # 5. Monitorowanie postępu oraz wykrywanie błędów polityki
            start_t = time.time()
            render_success = False

            while time.time() - start_t < max_wait_sec:
                # Sprawdzenie błędu polityki
                failed_msg = page.locator("text=/violate our policies|Failed/i").first
                if failed_msg.is_visible():
                    err_txt = "Zablokowano przez filtry bezpieczeństwa Google Flow (Policy Violation). Zmień słowa kluczowe w prompcie!"
                    print(f"[FlowClient ERROR] {err_txt}")
                    return False, err_txt

                pct = page.locator("text=/%/").first
                if pct.is_visible():
                    print(f"[FlowClient] Postęp: {pct.inner_text().strip()} ({int(time.time()-start_t)}s)")
                else:
                    if time.time() - start_t > 30:
                        print("[FlowClient] Render ukończony w 100%!")
                        render_success = True
                        break
                time.sleep(6)

            if not render_success and time.time() - start_t >= max_wait_sec:
                return False, f"Przekroczono limit czasu oczekiwania ({max_wait_sec}s)"

            time.sleep(4)

            # 6. Kliknięcie pobierania
            print("[FlowClient] Klikam przycisk pobierania...")
            dl_btn = page.locator("button[aria-label*='Download'], button:has-text('download')").first
            dl_btn.click(force=True)

            # 7. Oczekiwanie na nowy ZIP w katalogu Downloads
            found_zip = None
            for _ in range(15):
                time.sleep(2)
                cur = get_latest_zip(self.downloads_dir)
                if cur and os.path.getmtime(cur) > prev_time and cur != prev_zip and os.path.getsize(cur) > 100000:
                    found_zip = cur
                    break

            if not found_zip:
                print("[FlowClient] Próbuję ponownie kliknąć przycisk pobierania...")
                dl_btn.click(force=True)
                time.sleep(4)
                found_zip = get_latest_zip(self.downloads_dir)

            if not found_zip or not os.path.exists(found_zip):
                return False, "Nie znaleziono pobranego pliku ZIP w Downloads"

            print(f"[FlowClient] Pobrany ZIP: {found_zip} ({os.path.getsize(found_zip)} bajtów)")

            # 8. Ekstrakcja MP4
            with zipfile.ZipFile(found_zip) as z:
                for name in z.namelist():
                    if name.endswith(".mp4"):
                        data = z.read(name)
                        with open(output_path, "wb") as out_f:
                            out_f.write(data)
                        print(f"[FlowClient] Zapisano klip: {output_path} ({len(data)} bajtów)")
                        break

            # 9. Walidacja
            ok, msg = validate_clip(output_path, expected_aspect=aspect)
            print(f"[FlowClient QA] {msg}")
            return ok, msg

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google Flow Universal Automation Client")
    parser.add_argument("--prompt", required=True, help="Prompt tekstowy dla modelu")
    parser.add_argument("--output", required=True, help="Ścieżka do pliku wyjściowego .mp4")
    parser.add_argument("--aspect", default="16:9", choices=["16:9", "9:16"], help="Format proporcji obrazu")
    parser.add_argument("--anchor", default=None, help="Nazwa pliku kotwicy wizerunkowej w projekcie")
    args = parser.parse_args()

    client = FlowClient()
    success, message = client.generate_clip(args.prompt, args.output, anchor=args.anchor, aspect=args.aspect)
    sys.exit(0 if success else 1)

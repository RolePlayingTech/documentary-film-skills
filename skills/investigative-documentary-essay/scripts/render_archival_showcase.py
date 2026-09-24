#!/usr/bin/env python3
"""
Archival Showcase Generator (Playwright + FFmpeg)
Part of 'investigative-documentary-essay' skill for AI Film Production.

Generates cinematic archival showcase video clips (e.g. 6.0s or 10.0s) from raw historical images,
adding subtle Ken Burns floating zoom (1.00 -> 1.05), ambient backdrop grid, and an animated
Lower-Third archival chyron with document title, metadata, and collection signature.
"""

import os
import sys
import argparse
import subprocess
import urllib.parse
import json
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "templates", "template_archival_showcase.html"))

DEFAULT_FPS = 30
DEFAULT_DURATION = 6.0
DEFAULT_WIDTH = 1920
DEFAULT_HEIGHT = 1080
DEFAULT_ACCENT = "#f59e0b"

def render_showcase(image_path: str, output_path: str, title: str, desc: str, tag: str = "DOKUMENT ARCHIWALNY",
                    accent: str = DEFAULT_ACCENT, duration: float = DEFAULT_DURATION,
                    fps: int = DEFAULT_FPS, width: int = DEFAULT_WIDTH, height: int = DEFAULT_HEIGHT) -> bool:
    """
    Renders an archival showcase clip using template_archival_showcase.html.
    """
    img_abs = os.path.abspath(image_path)
    if not os.path.exists(img_abs):
        print(f"[ERROR] Image file not found: {img_abs}")
        return False

    if not os.path.exists(TEMPLATE_PATH):
        print(f"[ERROR] Showcase template not found: {TEMPLATE_PATH}")
        return False

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    total_frames = int(fps * duration)
    frame_interval_ms = 1000.0 / fps

    params = {
        "img": f"file:///{img_abs.replace(os.sep, '/')}",
        "title": title,
        "desc": desc,
        "tag": tag,
        "accent": accent,
        "dur": str(duration)
    }
    query_str = urllib.parse.urlencode(params)
    template_url = f"file:///{TEMPLATE_PATH.replace(os.sep, '/')}?{query_str}"

    print(f"\n[SHOWCASE] {os.path.basename(image_path)} -> {os.path.basename(output_path)}")
    print(f"           Title: '{title}' | Tag: '{tag}' | Duration: {duration:.2f}s")

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "image2pipe",
        "-vcodec", "mjpeg",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        output_path
    ]

    ffmpeg_proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": width, "height": height})
            page.goto(template_url)
            page.wait_for_timeout(350)

            for frame_idx in range(total_frames):
                t_ms = frame_idx * frame_interval_ms
                page.evaluate(f"window.renderAtMs ? window.renderAtMs({t_ms}) : null")
                frame_bytes = page.screenshot(type="jpeg", quality=95)
                ffmpeg_proc.stdin.write(frame_bytes)

            browser.close()

        ffmpeg_proc.stdin.close()
        ffmpeg_proc.wait()

        if ffmpeg_proc.returncode != 0:
            err = ffmpeg_proc.stderr.read().decode('utf-8', errors='replace')
            print(f"[ERROR] FFmpeg failed:\n{err}")
            return False

        print(f"[SUCCESS] Saved: {output_path} ({os.path.getsize(output_path)} bytes)")
        return True

    except Exception as e:
        print(f"[FATAL] Failed to render showcase: {e}")
        if ffmpeg_proc and ffmpeg_proc.poll() is None:
            ffmpeg_proc.kill()
        return False

def main():
    parser = argparse.ArgumentParser(description="Render Archival Showcase Video with Kinetic Chyron")
    parser.add_argument("-i", "--image", help="Path to input archival image")
    parser.add_argument("-o", "--output", help="Path to output .mp4 file")
    parser.add_argument("--title", default="Dokument Archiwalny", help="Chyron title")
    parser.add_argument("--desc", default="Zbiory Historyczne", help="Chyron description/provenance")
    parser.add_argument("--tag", default="DOKUMENT ARCHIWALNY", help="Chyron badge category tag")
    parser.add_argument("--accent", default=DEFAULT_ACCENT, help="Accent color (hex, e.g. #f59e0b)")
    parser.add_argument("-d", "--duration", type=float, default=DEFAULT_DURATION, help="Duration in seconds (default: 6.0)")
    parser.add_argument("--fps", type=int, default=DEFAULT_FPS, help="FPS (default: 30)")
    parser.add_argument("--manifest", help="JSON manifest for batch rendering multiple showcases")

    args = parser.parse_args()

    if args.manifest:
        manifest_path = os.path.abspath(args.manifest)
        if not os.path.exists(manifest_path):
            print(f"[ERROR] Manifest not found: {manifest_path}")
            sys.exit(1)

        with open(manifest_path, "r", encoding="utf-8") as f:
            items = json.load(f)

        print(f"Batch rendering {len(items)} archival showcases from manifest...")
        failures = 0
        for item in items:
            ok = render_showcase(
                image_path=item["image"],
                output_path=item["output"],
                title=item.get("title", "Dokument Archiwalny"),
                desc=item.get("desc", ""),
                tag=item.get("tag", "DOKUMENT ARCHIWALNY"),
                accent=item.get("accent", DEFAULT_ACCENT),
                duration=float(item.get("duration", DEFAULT_DURATION)),
                fps=args.fps
            )
            if not ok:
                failures += 1

        print(f"\n[DONE] Manifest render complete. Success: {len(items) - failures}/{len(items)}")
        sys.exit(0 if failures == 0 else 1)

    elif args.image and args.output:
        ok = render_showcase(
            image_path=args.image,
            output_path=args.output,
            title=args.title,
            desc=args.desc,
            tag=args.tag,
            accent=args.accent,
            duration=args.duration,
            fps=args.fps
        )
        sys.exit(0 if ok else 1)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()

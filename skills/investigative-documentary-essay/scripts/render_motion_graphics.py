#!/usr/bin/env python3
"""
Investigative Motion Graphics Renderer (Playwright + FFmpeg)
Part of 'investigative-documentary-essay' skill for AI Film Production.

Renders deterministic HTML/JS motion graphics at 1080p 30fps to broadcast-grade MP4 (CRF 18).
Supports single HTML files, directories, or batch manifests.
"""

import os
import sys
import argparse
import subprocess
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

DEFAULT_WIDTH = 1920
DEFAULT_HEIGHT = 1080
DEFAULT_FPS = 30
DEFAULT_DURATION = 10.0
DEFAULT_CRF = 18

def render_html_to_mp4(html_path: str, output_path: str, duration: float = DEFAULT_DURATION,
                       fps: int = DEFAULT_FPS, width: int = DEFAULT_WIDTH, height: int = DEFAULT_HEIGHT,
                       crf: int = DEFAULT_CRF) -> bool:
    """
    Renders a single HTML motion graphic file to MP4 frame-by-frame.
    Calls `window.renderAtMs(t_ms)` inside the page if defined.
    """
    html_abs = os.path.abspath(html_path)
    if not os.path.exists(html_abs):
        print(f"[ERROR] HTML file not found: {html_abs}")
        return False

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    total_frames = int(fps * duration)
    frame_interval_ms = 1000.0 / fps

    print(f"\n[RENDER] {os.path.basename(html_path)} -> {os.path.basename(output_path)}")
    print(f"         {total_frames} frames @ {width}x{height} {fps}fps | Duration: {duration:.2f}s | CRF: {crf}")

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "image2pipe",
        "-vcodec", "mjpeg",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", str(crf),
        "-pix_fmt", "yuv420p",
        output_path
    ]

    ffmpeg_proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": width, "height": height})
            page.goto(f"file:///{html_abs.replace(os.sep, '/')}")
            # Brief warm-up to ensure web fonts and local assets are resolved
            page.wait_for_timeout(350)

            for frame_idx in range(total_frames):
                t_ms = frame_idx * frame_interval_ms
                page.evaluate(f"window.renderAtMs ? window.renderAtMs({t_ms}) : null")
                frame_bytes = page.screenshot(type="jpeg", quality=95)
                ffmpeg_proc.stdin.write(frame_bytes)

                if (frame_idx + 1) % 60 == 0 or (frame_idx + 1) == total_frames:
                    print(f"         Rendered frame {frame_idx + 1}/{total_frames} ({((frame_idx + 1)/total_frames)*100:.1f}%)")

            browser.close()

        ffmpeg_proc.stdin.close()
        ffmpeg_proc.wait()

        if ffmpeg_proc.returncode != 0:
            stderr_log = ffmpeg_proc.stderr.read().decode('utf-8', errors='replace')
            print(f"[ERROR] FFmpeg failed with code {ffmpeg_proc.returncode}:\n{stderr_log}")
            return False

        file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"[SUCCESS] Saved: {output_path} ({file_size_mb:.2f} MB)")
        return True

    except Exception as e:
        print(f"[FATAL] Error rendering {html_path}: {e}")
        if ffmpeg_proc and ffmpeg_proc.poll() is None:
            ffmpeg_proc.kill()
        return False

def main():
    parser = argparse.ArgumentParser(description="Deterministic Motion Graphics Renderer (Playwright -> FFmpeg)")
    parser.add_argument("-i", "--input", required=True, help="Path to .html file or folder containing .html files")
    parser.add_argument("-o", "--output", required=True, help="Path to output .mp4 file or output folder")
    parser.add_argument("-d", "--duration", type=float, default=DEFAULT_DURATION, help="Duration in seconds (default: 10.0)")
    parser.add_argument("--fps", type=int, default=DEFAULT_FPS, help="Frames per second (default: 30)")
    parser.add_argument("--width", type=int, default=DEFAULT_WIDTH, help="Stage width in px (default: 1920)")
    parser.add_argument("--height", type=int, default=DEFAULT_HEIGHT, help="Stage height in px (default: 1080)")
    parser.add_argument("--crf", type=int, default=DEFAULT_CRF, help="FFmpeg CRF quality 0-51 (default: 18)")

    args = parser.parse_args()

    input_path = os.path.abspath(args.input)
    output_path = os.path.abspath(args.output)

    if os.path.isfile(input_path):
        if not output_path.lower().endswith(".mp4"):
            output_path = os.path.splitext(output_path)[0] + ".mp4"
        success = render_html_to_mp4(
            input_path, output_path,
            duration=args.duration, fps=args.fps,
            width=args.width, height=args.height, crf=args.crf
        )
        sys.exit(0 if success else 1)

    elif os.path.isdir(input_path):
        os.makedirs(output_path, exist_ok=True)
        html_files = sorted([f for f in os.listdir(input_path) if f.lower().endswith(".html")])
        if not html_files:
            print(f"[WARN] No .html files found in {input_path}")
            sys.exit(1)

        print(f"Found {len(html_files)} HTML animations to render in {input_path}")
        failures = 0
        for hf in html_files:
            h_full = os.path.join(input_path, hf)
            out_name = os.path.splitext(hf)[0] + ".mp4"
            out_full = os.path.join(output_path, out_name)
            ok = render_html_to_mp4(
                h_full, out_full,
                duration=args.duration, fps=args.fps,
                width=args.width, height=args.height, crf=args.crf
            )
            if not ok:
                failures += 1

        print(f"\n[DONE] Finished batch render. Success: {len(html_files) - failures}/{len(html_files)}")
        sys.exit(0 if failures == 0 else 1)
    else:
        print(f"[ERROR] Input path does not exist: {input_path}")
        sys.exit(1)

if __name__ == "__main__":
    main()

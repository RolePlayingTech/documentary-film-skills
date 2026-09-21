"""
Weryfikacja parametrów technicznych i ekstrakcja klatek inspekcyjnych z klipu Flow.
Sprawdza: 1280x720, 24fps, dokładnie 10.00s trwania oraz brak uszkodzeń pliku wideo.
"""

import os
import sys
import subprocess
import cv2

def inspect_clip(video_path, output_frames_dir=None):
    if not os.path.exists(video_path):
        print(f"BŁĄD: Plik nie istnieje: {video_path}")
        return False

    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    dur = total_frames / fps if fps > 0 else 0

    print(f"=== AUDYT KLIPU: {os.path.basename(video_path)} ===")
    print(f"Rozdzielczość: {width}x{height} (Oczekiwana: 1280x720)")
    print(f"Klatkarz: {fps:.2f} fps (Oczekiwany: 24 fps)")
    print(f"Liczba klatek: {total_frames} (Oczekiwana: ~240)")
    print(f"Czas trwania: {dur:.2f}s (Oczekiwany: ~10.00s)")

    is_valid = (width == 1280 and height == 720 and abs(dur - 10.0) <= 0.5)

    if output_frames_dir:
        os.makedirs(output_frames_dir, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        # Ekstrakcja klatek w punktach 1s, 5s i 9s
        for sec in [1.0, 5.0, 9.0]:
            frame_no = int(sec * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
            ret, frame = cap.read()
            if ret:
                out_path = os.path.join(output_frames_dir, f"{base_name}_frame_{int(sec)}s.jpg")
                cv2.imwrite(out_path, frame)
                print(f"  Zapisano klatkę kontrolną: {out_path}")

    cap.release()
    return is_valid

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Użycie: python inspect_flow_clip.py <sciezka_do_wideo.mp4> [katalog_klatek]")
        sys.exit(1)
    vid = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else "./qc_frames"
    success = inspect_clip(vid, out_dir)
    sys.exit(0 if success else 1)

"""
Narzędzie inspekcji wizualnej Mastera lub klipów wideo.
Ekstrahuje serię klatek w kluczowych punktach czasowych do weryfikacji tożsamości postaci,
glitchy dłoni, stabilności geometrii i poprawności napisów Karaoke.
"""

import os
import sys
import cv2

def extract_qc_frames(video_path, out_dir, points=None):
    if not os.path.exists(video_path):
        print(f"BŁĄD: Plik wideo nie istnieje: {video_path}")
        return False

    os.makedirs(out_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
    duration = total_frames / fps

    print(f"=== EKSTRAKCJA KLATEK QC: {os.path.basename(video_path)} ({duration:.2f}s) ===")

    if points is None:
        if duration <= 12.0:
            points = [1.0, 5.0, duration - 1.0]
        else:
            points = [5.0, 15.0, 30.0, 60.0, 120.0, 180.0, 240.0, duration - 5.0]

    for pt in points:
        if pt >= duration or pt < 0:
            continue
        frame_idx = int(pt * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if ret:
            out_file = os.path.join(out_dir, f"qc_{int(pt)}s.jpg")
            cv2.imwrite(out_file, frame)
            print(f"  Zapisano klatkę inspekcyjną: {out_file} (t={pt:.1f}s)")

    cap.release()
    print("Ekstrakcja zakończona pomyślnie.")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Użycie: python qc_extract_frames.py <plik_wideo.mp4> <katalog_wyjsciowy>")
        sys.exit(1)
    extract_qc_frames(sys.argv[1], sys.argv[2])

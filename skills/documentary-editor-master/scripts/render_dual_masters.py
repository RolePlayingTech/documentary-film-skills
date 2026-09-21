"""
Renderowanie dwóch emisyjnych wersji Mastera:
1. Clean Master: Czyste wideo bez napisów ze zmiksowaną muzyką tła i sidechain duckingiem.
2. Subtitled Master: Wersja z wtopionymi napisami Karaoke ASS i duckingiem muzyki.
"""

import os
import sys
import subprocess

def render_dual(raw_master, music_file, ass_file, total_duration, out_clean, out_subtitled):
    if not os.path.exists(raw_master):
        raise FileNotFoundError(f"Brak surowego mastera: {raw_master}")
    if not os.path.exists(music_file):
        raise FileNotFoundError(f"Brak pliku muzyki: {music_file}")

    print(f"=== RENDEROWANIE DUAL MASTER ({total_duration:.2f}s) ===")

    # 1. Clean Master
    print(f"--> Renderowanie Clean Master: {out_clean}")
    filter_clean = (
        f"[1:a]loudnorm=I=-24:TP=-2:LRA=11,aloop=loop=-1:size=2e+09,atrim=0:{total_duration:.3f}[music_loop];"
        f"[music_loop][0:a]sidechaincompress=threshold=0.08:ratio=5:attack=100:release=1000[music_ducked];"
        f"[0:a][music_ducked]amix=inputs=2:duration=first:dropout_transition=2:normalize=0[aout]"
    )
    cmd_clean = [
        "ffmpeg", "-y",
        "-i", raw_master,
        "-i", music_file,
        "-filter_complex", filter_clean,
        "-map", "0:v", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", "-r", "24",
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
        "-t", f"{total_duration:.3f}",
        out_clean
    ]
    subprocess.run(cmd_clean, check=True)

    # 2. Subtitled Master
    print(f"--> Renderowanie Subtitled Master: {out_subtitled}")
    ass_escaped = ass_file.replace("\\", "/").replace(":", "\\:")
    filter_sub = (
        f"[0:v]ass='{ass_escaped}'[v_burned];"
        f"[1:a]loudnorm=I=-24:TP=-2:LRA=11,aloop=loop=-1:size=2e+09,atrim=0:{total_duration:.3f}[music_loop];"
        f"[music_loop][0:a]sidechaincompress=threshold=0.08:ratio=5:attack=100:release=1000[music_ducked];"
        f"[0:a][music_ducked]amix=inputs=2:duration=first:dropout_transition=2:normalize=0[aout]"
    )
    cmd_sub = [
        "ffmpeg", "-y",
        "-i", raw_master,
        "-i", music_file,
        "-filter_complex", filter_sub,
        "-map", "[v_burned]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", "-r", "24",
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
        "-t", f"{total_duration:.3f}",
        out_subtitled
    ]
    subprocess.run(cmd_sub, check=True)
    print("Obydwie wersje emisyjne zostały wyrenderowane pomyślnie!")

if __name__ == "__main__":
    if len(sys.argv) < 7:
        print("Użycie: python render_dual_masters.py <raw_master.mp4> <music.mp3> <karaoke.ass> <duration_sec> <out_clean.mp4> <out_sub.mp4>")
        sys.exit(1)
    render_dual(sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), sys.argv[5], sys.argv[6])

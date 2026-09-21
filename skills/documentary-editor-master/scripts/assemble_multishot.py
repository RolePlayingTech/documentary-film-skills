"""
Narzędzie montażu scen B-Roll w sekwencje Multi-Shot bez sztucznych pętli wideo.
Dzieli czas trwania głosu lektora (+ 0.8s) na N unikalnych ujęć B-roll i miksuje audio.
"""

import os
import sys
import subprocess

def get_duration(filepath):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", filepath
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return float(res.stdout.strip())

def assemble_broll_scene(vo_file, shot_files, output_file):
    if not os.path.exists(vo_file):
        raise FileNotFoundError(f"Brak pliku VO: {vo_file}")
    for s in shot_files:
        if not os.path.exists(s):
            raise FileNotFoundError(f"Brak pliku ujęcia B-roll: {s}")

    vo_dur = get_duration(vo_file)
    t_total = vo_dur + 0.80
    n_shots = len(shot_files)

    shot_dur = t_total / float(n_shots)
    durations = [shot_dur] * (n_shots - 1)
    durations.append(t_total - sum(durations))

    print(f"Montaż B-Roll: VO={vo_dur:.2f}s, Razem={t_total:.2f}s, Liczba ujęć: {n_shots}")

    inputs = ["-i", vo_file]
    for s in shot_files:
        inputs.extend(["-i", s])

    filter_parts = []
    v_concat = ""
    a_concat = ""

    for i in range(n_shots):
        in_idx = i + 1
        d = durations[i]
        filter_parts.append(f"[{in_idx}:v]trim=0:{d:.3f},setpts=PTS-STARTPTS,scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1[v{i}]")
        filter_parts.append(f"[{in_idx}:a]atrim=0:{d:.3f},asetpts=PTS-STARTPTS,volume=0.08[a{i}]")
        v_concat += f"[v{i}]"
        a_concat += f"[a{i}]"

    filter_parts.append(f"{v_concat}concat=n={n_shots}:v=1:a=0[vout]")
    filter_parts.append(f"{a_concat}concat=n={n_shots}:v=0:a=1[ambient_concat]")
    filter_parts.append(f"[0:a]loudnorm=I=-16:TP=-1.5:LRA=7,apad=whole_dur={t_total:.3f}[lektor_padded]")
    filter_parts.append(f"[lektor_padded][ambient_concat]amix=inputs=2:duration=first:dropout_transition=2:normalize=0[aout]")

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", ";".join(filter_parts),
        "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "24",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
        "-t", f"{t_total:.3f}",
        output_file
    ]
    subprocess.run(cmd, check=True)
    print(f"Wygenerowano zmontowaną scenę B-roll: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Użycie: python assemble_multishot.py <vo.mp3> <output.mp4> <shot1.mp4> <shot2.mp4> [shot3.mp4...]")
        sys.exit(1)
    vo = sys.argv[1]
    out = sys.argv[2]
    shots = sys.argv[3:]
    assemble_broll_scene(vo, shots, out)

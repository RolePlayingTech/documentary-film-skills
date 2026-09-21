"""
Generator napisów dynamicznych Karaoke ASS z kalibrowanym offsetem wyprzedzającym (-90ms).
Pobiera transkrypcję JSON z Whisper STT (word_timestamps=True) i tworzy pliki .srt oraz .ass.
"""

import os
import sys
import json

OFFSET = -0.090  # 90ms kalibracji wyprzedzającej percepcji wzrokowej

def fmt_srt(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int(round((sec - int(sec)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def fmt_ass(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int(round((sec - int(sec)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h:01d}:{m:02d}:{s:02d}.{cs:02d}"

def build_subtitles(whisper_json_path, srt_out_path, ass_out_path, corrections=None):
    with open(whisper_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if corrections is None:
        corrections = {}

    all_words = []
    for seg in data.get("segments", []):
        for w in seg.get("words", []):
            txt = w["word"].strip()
            if not txt:
                continue
            for k, v in corrections.items():
                if txt.lower() == k.lower():
                    txt = v
            all_words.append({
                "word": txt,
                "start": float(w["start"]),
                "end": float(w["end"])
            })

    # Wygładzenie nakładających się czasów słów
    for i in range(len(all_words) - 1):
        if all_words[i]["end"] > all_words[i+1]["start"]:
            mid = (all_words[i]["end"] + all_words[i+1]["start"]) / 2.0
            if mid > all_words[i]["start"] + 0.05:
                all_words[i]["end"] = mid
                all_words[i+1]["start"] = mid

    # Zapis standardowego SRT
    with open(srt_out_path, "w", encoding="utf-8") as f:
        idx = 1
        for seg in data.get("segments", []):
            st = fmt_srt(seg["start"])
            en = fmt_srt(seg["end"])
            txt = seg["text"].strip()
            for k, v in corrections.items():
                txt = txt.replace(k, v).replace(k.lower(), v)
            if txt:
                f.write(f"{idx}\n{st} --> {en}\n{txt}\n\n")
                idx += 1

    # Podział słów na naturalne linijki karaoke (maks 5-6 słów lub koniec zdania)
    chunks = []
    cur_chunk = []
    for w in all_words:
        cur_chunk.append(w)
        ends_sentence = any(w["word"].endswith(p) for p in [".", "!", "?", ":", ";"])
        chunk_too_long = len(cur_chunk) >= 5
        chunk_dur = cur_chunk[-1]["end"] - cur_chunk[0]["start"]
        if (ends_sentence and len(cur_chunk) >= 2) or chunk_too_long or chunk_dur >= 3.5:
            chunks.append(cur_chunk)
            cur_chunk = []
    if cur_chunk:
        chunks.append(cur_chunk)

    ass_header = (
        "[Script Info]\n"
        "Title: Documentary Master Karaoke\n"
        "ScriptType: v4.00+\n"
        "WrapStyle: 0\n"
        "ScaledBorderAndShadow: yes\n"
        "YCbCr Matrix: TV.709\n"
        "PlayResX: 1280\n"
        "PlayResY: 720\n\n"
        "[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
        "Style: Default,Arial,38,&H00FFFFFF,&H0000D7FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3.0,1.5,2,40,40,48,1\n\n"
        "[Events]\n"
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    )

    with open(ass_out_path, "w", encoding="utf-8") as f:
        f.write(ass_header)
        for chunk in chunks:
            c_start = max(0.0, chunk[0]["start"] + OFFSET)
            c_end = max(c_start + 0.5, chunk[-1]["end"] + 0.10)

            k_parts = []
            for w in chunk:
                w_start = max(0.0, w["start"] + OFFSET)
                w_end = max(w_start + 0.10, w["end"] + OFFSET)
                dur_cs = int(round((w_end - w_start) * 100))
                if dur_cs < 5:
                    dur_cs = 5
                k_parts.append(f"{{\\k{dur_cs}}}{w['word']}")

            line_text = " ".join(k_parts)
            f.write(f"Dialogue: 0,{fmt_ass(c_start)},{fmt_ass(c_end)},Default,,0,0,0,,{line_text}\n")

    print(f"Wygenerowano SRT: {srt_out_path}")
    print(f"Wygenerowano ASS Karaoke (-90ms): {ass_out_path}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Użycie: python generate_karaoke_ass.py <transcription.json> <output.srt> <output.ass>")
        sys.exit(1)
    build_subtitles(sys.argv[1], sys.argv[2], sys.argv[3])

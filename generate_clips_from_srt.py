import re
import csv

def srt_time_to_seconds(t):
    h, m, s_ms = t.split(':')
    s, ms = s_ms.split(',')
    return int(h)*3600 + int(m)*60 + int(s) + int(ms)/1000

def seconds_to_srt_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def extract_srt_blocks(srt_text):
    pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)\n(?=\d+\n|\Z)', re.DOTALL)
    blocks = pattern.findall(srt_text)
    parsed_blocks = []
    for idx, start, end, text in blocks:
        clean_text = text.replace('\n', ' ').strip()
        parsed_blocks.append({
            "index": int(idx),
            "start": start,
            "end": end,
            "start_sec": srt_time_to_seconds(start),
            "end_sec": srt_time_to_seconds(end),
            "text": clean_text
        })
    return parsed_blocks

def generate_clips(blocks, min_duration=10):
    clips = []
    current = {"start": None, "end": None, "text": "", "duration": 0}

    for block in blocks:
        if current["start"] is None:
            current["start"] = block["start_sec"]

        current["end"] = block["end_sec"]
        current["text"] += " " + block["text"]
        current["duration"] = current["end"] - current["start"]

        if current["duration"] >= min_duration:
            clips.append({
                "start_time": seconds_to_srt_time(current["start"]),
                "end_time": seconds_to_srt_time(current["end"]),
                "duration_sec": round(current["duration"], 2),
                "text": current["text"].strip()
            })
            current = {"start": None, "end": None, "text": "", "duration": 0}

    return clips

# --- Main script ---

srt_file = "input.srt"  # Rename to match your file
output_csv = "clips_output.csv"

with open(srt_file, "r", encoding="utf-8") as f:
    srt_data = f.read()

blocks = extract_srt_blocks(srt_data)
clips = generate_clips(blocks)

with open(output_csv, "w", newline='', encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["start_time", "end_time", "duration_sec", "text"])
    writer.writeheader()
    for clip in clips:
        writer.writerow(clip)

print(f"✅ {len(clips)} clips written to {output_csv}")

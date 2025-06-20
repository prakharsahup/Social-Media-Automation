import pandas as pd
from moviepy.editor import VideoFileClip
import os

# ---- Config ----
csv_path = "clips_output.csv"
video_file = "mainInput.mp4"  # Using mainInput.mp4 as specified
output_folder = "reel_clips"
os.makedirs(output_folder, exist_ok=True)

# ---- Load Timestamps ----
df = pd.read_csv(csv_path)

# ---- Cut the Clips ----
for idx, row in df.iterrows():
    try:
        start = sum(x * int(t) for x, t in zip([3600, 60, 1], row['start_time'].replace(',', ':').split(':')))
        end = sum(x * int(t) for x, t in zip([3600, 60, 1], row['end_time'].replace(',', ':').split(':')))
        output_path = os.path.join(output_folder, f"reel_{idx+1:03d}.mp4")

        with VideoFileClip(video_file).subclip(start, end) as clip:
            clip.write_videofile(output_path, codec="libx264", audio_codec="aac", threads=4)
    except Exception as e:
        print(f"❌ Error processing clip {idx+1}: {e}")

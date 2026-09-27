import os
import subprocess
import numpy as np
from scipy.io import wavfile

# --- Configuration ---
VIDEO_FILE = "stream_vod.mp4"
OUTPUT_DIR = "clips"
CONTEXT_BEFORE = 15  # Seconds to include before the spike (the setup)
CONTEXT_AFTER = 10   # Seconds to include after the spike (the reaction)
THRESHOLD_PERCENTILE = 98  # Scans for the top 2% loudest audio moments

def extract_audio(video_path, audio_path):
    print("1/3: Extracting audio for analysis (this takes a minute)...")
    # Forces mono, 16kHz audio so it processes incredibly fast without crashing RAM
    subprocess.run([
        "ffmpeg", "-i", video_path, 
        "-vn", "-ac", "1", "-ar", "16000", "-y", audio_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def find_loud_spikes(audio_path):
    print("2/3: Analyzing volume to find the funny moments...")
    sample_rate, data = wavfile.read(audio_path)
    
    # Calculate RMS volume in 1-second chunks
    chunk_size = sample_rate 
    num_chunks = len(data) // chunk_size
    
    volumes = []
    for i in range(num_chunks):
        chunk = data[i*chunk_size : (i+1)*chunk_size]
        # Cast to int64 to prevent overflow when squaring audio data
        rms = np.sqrt(np.mean(np.square(chunk.astype(np.int64))))
        volumes.append(rms)
        
    threshold = np.percentile(volumes, THRESHOLD_PERCENTILE)
    loud_seconds = [i for i, vol in enumerate(volumes) if vol > threshold]
    
    # Group loud spikes that happen close together
    clips = []
    if not loud_seconds:
        return clips
        
    current_start = loud_seconds[0]
    current_end = loud_seconds[0]
    
    for sec in loud_seconds[1:]:
        if sec - current_end <= 30: # If spikes are within 30s, group them into one continuous clip
            current_end = sec
        else:
            clips.append((current_start, current_end))
            current_start = sec
            current_end = sec
    clips.append((current_start, current_end))
    
    return clips

def cut_clips(video_path, clips, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    print(f"3/3: Found {len(clips)} major events. Clipping now...")
    
    for i, (start, end) in enumerate(clips):
        clip_start = max(0, start - CONTEXT_BEFORE)
        clip_end = end + CONTEXT_AFTER
        duration = clip_end - clip_start
        
        out_file = os.path.join(out_dir, f"clip_{i+1}.mp4")
        
        # Fast stream-copy without re-encoding
        subprocess.run([
            "ffmpeg", "-ss", str(clip_start), "-i", video_path, 
            "-t", str(duration), "-c", "copy", "-y", out_file
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print(f" -> Saved {out_file}")

if __name__ == "__main__":
    temp_audio = "temp_audio.wav"
    try:
        extract_audio(VIDEO_FILE, temp_audio)
        loud_clips = find_loud_spikes(temp_audio)
        cut_clips(VIDEO_FILE, loud_clips, OUTPUT_DIR)
        print("Done! You can now review the rough cuts in your clips folder.")
    finally:
        if os.path.exists(temp_audio):
            os.remove(temp_audio)
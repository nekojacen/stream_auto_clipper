# AutoClipper for Stream VODs

AutoClipper is a lightweight Python script that automatically scans your stream VODs for loud, high-energy moments and cuts them into bite-sized clips for easy editing. 

## The Problem with VODs
If you stream on Twitch or record long gaming sessions, you already know the biggest bottleneck in content creation: **the scrub.** 

Finding the best moments in a 2-hour or 4-hour VOD is a massive time sink. You either have to rely on chat clipping (which misses things), write down timestamps while trying to focus on a game, or manually watch your entire stream back in your video editor just to find a few minutes of usable footage. 

AutoClipper was built to solve this exact problem. Instead of watching the video, AutoClipper "listens" to it. By isolating the audio track and mathematically scanning for volume spikes—like jump scares, uncontrollable laughter, or high-energy reactions—it pinpoints exactly where the action happens. It then automatically slices out those segments with a built-in buffer for the setup and the reaction, handing you a folder full of raw highlights ready for the editing timeline.

## Who is this for?
* **Streamers & VTubers:** Quickly convert last night's stream into a folder of highlights without spending your whole morning reviewing footage. 
* **Let's Players:** Isolate the loudest, most energetic parts of a recording session to build out a structured 15-to-30-minute main channel video.
* **Video Editors:** Speed up your workflow when a client hands you a massive unedited file by running a quick pass to find the hype moments.

## Design Philosophy
1. **Speed over everything:** By down-mixing the audio to mono 16kHz for the analysis phase, the script can process hours of video in seconds without crashing your RAM. 
2. **No quality loss:** AutoClipper uses `ffmpeg` stream-copying for the final cuts. It doesn't re-encode your video, meaning the output clips retain the exact same visual quality as your original VOD.
3. **Workflow compatible:** This isn't meant to replace a video editor. It's designed to feed into one. The clips generated are rough cuts that you can drag directly into your editor to add your subtitles, zooms, and custom branding. 

## How It Works
1. **Audio Extraction:** Extracts a low-res, mono audio track from your video for lightning-fast analysis.
2. **Volume Analysis:** Calculates the RMS volume in 1-second chunks and isolates the loudest moments (by default, the top 2% loudest peaks). 
3. **Smart Clipping:** Groups spikes that happen close together and uses `ffmpeg` to fast-copy the video with a customizable buffer before and after the action.

## Prerequisites
To run `autoclipper.py`, you need Python 3 installed, along with a few packages and a system dependency.

### 1. Install FFmpeg
The script relies heavily on FFmpeg for audio extraction and video cutting. It must be installed and added to your system's PATH.
* **Windows:** `winget install Gyan.FFmpeg` (or download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/))
* **macOS:** `brew install ffmpeg`
* **Linux:** `sudo apt install ffmpeg`

### 2. Install Python Packages
Install the required scientific computing libraries:
`pip install numpy scipy`



## Place your downloaded stream video in the same folder as autoclipper.py and name it stream_vod.mp4 (or update the script's configuration to match your filename).
Run the script:

`python autoclipper.py`

Check the newly created clips/ folder for your rough cuts!

Configuration
You can easily tweak how the clipper behaves by modifying the variables at the top of autoclipper.py:

Python
# --- Configuration ---
VIDEO_FILE = "stream_vod.mp4"  # The name of your input video file

OUTPUT_DIR = "clips"           # The folder where clips will be saved

CONTEXT_BEFORE = 15            # Seconds to include before the loud spike (the setup)

CONTEXT_AFTER = 10             # Seconds to include after the loud spike (the reaction)

THRESHOLD_PERCENTILE = 98      # Scans for the top 2% loudest audio moments. Lower this number to get MORE clips, raise it to get FEWER.


# --- Tips for Best Results ---
Microphone Routing: Because AutoClipper relies on volume thresholds, it works best when your audio levels are clean. If you use virtual audio mixers to separate audio tracks, ensuring your microphone peaks higher than your desktop/game audio will yield the most accurate, reaction-focused cuts.

Editing: These clips are "rough cuts" meant to save you time hunting for moments. Drop them directly into your timeline to add your visual effects, text, and formatting.

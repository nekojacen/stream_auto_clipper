# AutoClipper for Stream VODs

AutoClipper is a lightweight Python script that automatically scans your stream VODs for loud, high-energy moments (like screams, laughs, or intense gameplay) and cuts them into bite-sized clips for easy editing. 

Instead of scrubbing through hours of footage, this script analyzes the audio waveform and uses `ffmpeg` to extract the best moments instantly without re-encoding the video.

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

```bash
pip install numpy scipy

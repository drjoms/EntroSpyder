import subprocess
import hashlib
import time
import os

# --- CONFIGURATION ---
# VIDEO SETTINGS
VIDEO_CMD = ["v4l2-ctl", "-d", "/dev/video0", "--stream-mmap", "--stream-count=10", "--stream-to=-"]
# We use 10 frames to get a larger, more stable sample of entropy
NUM_FRAMES = 10 
FRAME_SIZE = 614400 # 640x480 YUYV

# AUDIO SETTINGS
# We capture 5 seconds of audio to ensure we have enough "chaos"
AUDIO_CMD = ["arecord", "-f", "cd", "-t", "raw", "-r", "44100", "-c", "2", "-d", "5"]

# DESTINATION
TEMP_FILE = "ent_test_buffer.bin"

def run_stress_test():
    print("🕷️  EntroSpyder: Initiating Multi-Source Stress Test...")
    print("📸 Capturing Video Frames...")
    print("🎤 Capturing Audio Stream...")

    # 1. CAPTURE VIDEO
    # We run the video command and capture the output of 10 frames
    video_proc = subprocess.Popen(VIDEO_CMD, stdout=subprocess.PIPE)
    video_data = video_proc.stdout.read(FRAME_SIZE * NUM_FRAMES)
    video_proc.wait()

    # 2. CAPTURE AUDIO
    # We run arecord for 5 seconds
    audio_proc = subprocess.Popen(AUDIO_CMD, stdout=subprocess.PIPE)
    audio_data = audio_proc.stdout.read()
    audio_proc.wait()

    if not video_data or not audio_data:
        print("❌ Error: Capture failed. Check your hardware connections.")
        return

    print(f"✅ Capture Complete.")
    print(f"📊 Stats: Video={len(video_data)} bytes | Audio={len(audio_data)} bytes")

    # 3. THE MIXER (The XOR Logic)
    # To compare them, they MUST be the same length. 
    # We will use the audio data as the "base" and XOR it with the video data.
    # We cycle the video data if it's shorter than the audio.
    
    print("🧪 Mixing Sources (XORing Video + Audio)...")
    
    # We create a combined buffer of the actual length of the audio
    # This ensures we are testing the 'Mixed' entropy
    mixed_buffer = bytearray(audio_data)
    
    for i in range(len(audio_data)):
        # XOR the audio byte with a byte from the video (looping the video)
        video_byte = video_data[i % len(video_data)]
        mixed_buffer[i] = mixed_buffer[i] ^ video_byte

    # 4. THE VALIDATION (Running 'ent')
    print("🕵️ Running Entropy Analysis...")
    
    with open(TEMP_FILE, "wb") as f:
        f.write(mixed_buffer)

    try:
        result = subprocess.run(['ent', TEMP_FILE], capture_output=True, text=True)
        print("\n" + "="*40)
        print("📊 FINAL ENTROPY REPORT (MIXED SOURCES)")
        print("="*40)
        print(result.stdout)
        print("="*40)

        # Automated Verdict
        # We parse the entropy line
        for line in result.stdout.split('\n'):
            if "Entropy =" in line:
                entropy_val = float(line.split('=')[1].split()[0])
                
                if entropy_val > 7.95:
                    print("🚀 VERDICT: GOD TIER. The mix is pure chaos. Ready for Production.")
                elif entropy_val > 7.8:
                    print("✅ VERDICT: HIGH QUALITY. Very strong entropy. Ready for use.")
                else:
                    print("⚠️ VERDICT: WEAK. The mix is still too structured. Check your sources.")
                break

    except FileNotFoundError:
        print("❌ Error: 'ent' not found. Install it: sudo apt install ent")
    finally:
        if os.path.exists(TEMP_FILE):
            os.remove(TEMP_FILE)

if __name__ == "__main__":
    run_stress_test()


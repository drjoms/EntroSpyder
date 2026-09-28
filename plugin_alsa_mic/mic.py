import subprocess
import hashlib
import socket
import time

# --- CONFIGURATION ---
# -f cd: 16-bit Little End Endian, 44100Hz, Stereo (Standard CD quality)
# -t raw: No headers, just the raw PCM samples
# -r 44100: Sample rate
# -c 2: 2 channels (stereo)
ARECORD_CMD = ["arecord", "-f", "cd", "-t", "raw", "-r", "44100", "-c", "2"]

ENGINE_IP = "127.0.0.1"
ENGINE_PORT = 9999
# We'll use a chunk size that represents a small slice of time
# 44100 samples * 2 channels * 2 bytes (16-bit) = 176,400 bytes per second
CHUNK_SIZE = 176400 

def run_audio_plugin():
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Start the arecord process
    # We use stdout=PIPE so we can read the raw bytes directly into Python
    process = subprocess.Popen(ARECORD_CMD, stdout=subprocess.PIPE)

    print("🎤 EntroSpyder Audio Plugin: ACTIVE (High-Speed Audio Capture)")

    try:
        while True:
            # 1. CAPTURE: Read a chunk of raw PCM data from the pipe
            audio_bytes = process.stdout.read(CHUNK_SIZE)

            if not audio_bytes:
                break

            # 2. DISTILL: Hash the audio noise
            # This turns the acoustic chaos into a 64-byte seed
            digest = hashlib.blake2b(audio_bytes, digest_size=64).digest()

            # 3. BLAST: Send via UDP
            # We add a simple header so the Engine knows this is audio
            # [ID: 0x02][Type: AUDIO (0x02)][Payload: 64 bytes]
            header = b'\x02\x02' 
            sock.sendto(header + digest, (ENGINE_IP, ENGINE_PORT))

            # Small sleep to match real-time (approx 1 second chunks)
            # You can lower this for higher frequency updates
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Audio Plugin stopped.")
    finally:
        process.terminate()
        process.wait()

if __name__ == "__main__":
    run_audio_plugin()


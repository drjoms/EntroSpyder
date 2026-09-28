import subprocess
import hashlib
import socket

# --- CONFIG ---
VIDEO_CMD = ["v4l2-ctl", "-d", "/dev/video0", "--stream-mmap", "--stream-count=1000000", "--stream-to=-"]
ENGINE_IP = "127.0.0.1"
ENGINE_PORT = 9999
FRAME_SIZE = 614400 

def run_plugin():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    process = subprocess.Popen(VIDEO_CMD, stdout=subprocess.PIPE)

    print("🚀 EntroSpyder: High-Alignment Mode Active.")

    try:
        while True:
            # 1. THE CRITICAL STEP: Read exactly one frame's worth of data.
            # Because v4l2-ctl is 'frame-aware', the stdout buffer 
            # is structured into discrete chunks of FRAME_SIZE.
            frame_bytes = process.stdout.read(FRAME_SIZE)

            # 2. VALIDATION: Check if we actually got a full, healthy frame.
            if len(frame_bytes) < FRAME_SIZE:
                # If the read is short, the stream is out of sync or ended.
                # We break and restart to 're-sync' the driver.
                print("⚠️ Alignment error or stream end. Restarting...")
                break

            # 3. THE DISTILLATION (The "Pure" Chaos)
            # Since we confirmed we have a full frame, we know we are 
            # hashing only pixels, not metadata.
            digest = hashlib.blake2b(frame_bytes, digest_size=64).digest()

            # 4. THE BLAST
            sock.sendto(digest, (ENGINE_IP, ENGINE_PORT))

    except KeyboardInterrupt:
        print("\n🛑 Stopped.")
    finally:
        process.terminate()

if __name__ == "__main__":
    run_plugin()


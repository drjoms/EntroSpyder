import subprocess
import hashlib
import socket
import time
import io

# --- CONFIG ---
VIDEO_CMD = ["v4l2-ctl", "-d", "/dev/video0", "--stream-mmap", "--stream-count=1000000", "--stream-to=-"]
ENGINE_IP = "127.0.0.1"
ENGINE_PORT = 9999
FRAME_SIZE = 614400 

# --- DEBUG CONFIG ---
DEBUG_MODE = True
DEBUG_INTERVAL = 10  # Run 'ent' every 10 hashes
entropy_buffer = []

def run_ent_check(data_buffer):
    """Runs the 'ent' utility on a buffer of bytes."""
    if not data_buffer:
        return

    # Convert our list of bytes into one continuous byte-string
    combined_data = b"".join(data_buffer)
    
    print("\n--- 🕵️ ENTROPY DEBUG REPORT ---")
    try:
        # We pipe the combined data into 'ent' via stdin
        process = subprocess.Popen(['ent'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(input=combined_data)
        
        if stdout:
            print(stdout.decode())
        if stderr:
            print(f"Error: {stderr.decode()}")
    except FileNotFoundError:
        print("❌ Error: 'ent' not found. Please install it (sudo apt install ent).")
    print("-------------------------------\n")

def run_plugin():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Start the long-running v4l2-ctl process
    process = subprocess.Popen(VIDEO_CMD, stdout=subprocess.PIPE)

    print(f"🚀 EntroSpyder Plugin: ACTIVE (High-Speed Mode)")
    print(f"📡 Targeting Engine at {ENGINE_IP}:{ENGINE_PORT}")

    try:
        while True:
            # 1. READ: Get the raw pixels from the pipe
            frame_bytes = process.stdout.read(FRAME_SIZE)

            if not frame_bytes or len(frame_bytes) < FRAME_SIZE:
                print("⚠️ Stream ended or interrupted.")
                break

            # 2. DISTILL: BLAKE2b (Raw Binary)
            digest = hashlib.blake2b(frame_bytes, digest_size=64).digest()

            # 3. BLAST: Send to Engine
            sock.sendto(digest, (ENGINE_IP, ENGINE_PORT))

            # 4. DEBUG: Collect for the periodic ent check
            if DEBUG_MODE:
                entropy_buffer.append(digest)
                
                if len(entropy_buffer) >= DEBUG_INTERVAL:
                    run_ent_check(entropy_buffer)
                    entropy_buffer.clear() # Reset buffer after check

    except KeyboardInterrupt:
        print("\n🛑 Plugin stopped by user.")
    finally:
        process.terminate()
        process.wait()

if __name__ == "__main__":
    run_plugin()


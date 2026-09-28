import socket
import hashlib
import time
import os

# --- CONFIGURATION ---
ENGINE_IP = "127.0.0.1"  # Change to your PC's IP
ENGINE_PORT = 9999
# In production, use the real v4l2-ctl command to feed the data
# For now, we simulate a 614,400 byte frame
FRAME_SIZE = 614400 

def run_plugin():
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    print(f"🚀 EntroSpyder Plugin Started. Blasting to {ENGINE_IP}:{ENGINE_PORT}")

    try:
        while True:
            # 1. SIMULATE CAPTURE (In production, use v4l2-ctl pipe)
            # We use os.urandom to simulate the chaotic sensor noise
            frame = os.urandom(FRAME_SIZE)

            # 2. DISTILL (BLAKE2b in RAW BINARY mode)
            # This is the "No-Tax" way. No hex conversion.
            digest = hashlib.blake2b(frame, digest_size=64).digest()

            # 3. BLAST (UDP)
            # We send the 64 bytes as a single packet
            sock.sendto(digest, (ENGINE_IP, ENGINE_PORT))

            # Small sleep to prevent 100% CPU usage during testing
            # Adjust this to simulate your real FPS
            time.sleep(0.03) 

    except KeyboardInterrupt:
        print("\n🛑 Plugin stopped.")

if __name__ == "__main__":
    run_plugin()


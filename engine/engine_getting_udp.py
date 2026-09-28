import socket

# --- CONFIGURATION ---
LISTEN_IP = "0.0.0.0"  # Listen on all available interfaces
LISTEN_PORT = 9999

def run_engine():
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((LISTEN_IP, LISTEN_PORT))

    print(f"🛰️  EntroSpyder Engine Listening on {LISTEN_IP}:{LISTEN_PORT}")
    print("Waiting for entropy blasts...\n")

    count = 0
    try:
        while True:
            # 1. RECEIVE (Wait for the 64-byte blast)
            data, addr = sock.recvfrom(1024) # Buffer size 1024 is plenty for 64 bytes
            
            count += 1
            
            # 2. PROCESS (For now, we just print the count and the first few bytes)
            # In production, this is where your XOR and Bucket logic goes.
            print(f"[{count}] Received {len(data)} bytes from {addr}")
            print(f"    Raw Hex Preview: {data.hex()[:32]}...") 

    except KeyboardInterrupt:
        print("\n🛑 Engine stopped.")

if __name__ == "__main__":
    run_engine()


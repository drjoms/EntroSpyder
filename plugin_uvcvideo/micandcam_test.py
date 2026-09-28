import socket

# --- CONFIG ---
LISTEN_IP = "0.0.0.0"
LISTEN_PORT = 9999

# Buffers to hold the latest hashes from each source
# We use a dictionary to map ID -> latest_hash
latest_hashes = {
    1: None, # Video
    2: None  # Audio
}

def run_engine():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((LISTEN_IP, LISTEN_PORT))

    print(f"🛰️  EntroSpyder Engine: LISTENING on {LISTEN_IP}:{LISTEN_PORT}")

    try:
        while True:
            # 1. RECEIVE the packet
            packet, addr = sock.recvfrom(1024)

            if len(packet) < 66:
                continue # Skip malformed packets

            # 2. PARSE the Envelope
            plugin_id = packet[0]
            data_type = packet[1]
            incoming_hash = packet[2:]

            # 3. UPDATE the latest hash for that source
            latest_hashes[plugin_id] = incoming_hash
            
            print(f"📥 Received Type {data_type} from ID {plugin_id}")

            # 4. THE MIXING LOGIC (The "Entropy Boost")
            # If we have both a video hash and an audio hash, XOR them!
            if latest_hashes[1] and latest_hashes[2]:
                # This is the "Super-Hash"
                master_seed = bytes(a ^ b for a, b in zip(latest_hashes[1], latest_hashes[2]))
                
                # For debugging, let'            # Print the result
                print(f"✨ MASTER SEED GENERATED: {master_seed.hex()[:32]}...")
                # In production, this is what goes to your Monte Carlo engine.

    except KeyboardInterrupt:
        print("\n🛑 Engine stopped.")

if __name__ == "__main__":
    run_engine()


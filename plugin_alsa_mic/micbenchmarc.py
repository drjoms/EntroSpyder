import subprocess
import hashlib
import io

# --- CONFIG ---
# Using the exact same settings as your plugin to ensure consistency
ARECORD_CMD = ["arecord", "-f", "cd", "-t", "raw", "-r", "44100", "-c", "2"]
FRAME_SIZE = 1764000 # 1 second of audio

def run_benchmark():
    print("🧪 Starting Mic Entropy Stress Test...")

    # 1. Capture a chunk of audio
    process = subprocess.Popen(ARECORD_CMD, stdout=subprocess.PIPE)
    audio_bytes = process.stdout.read(FRAME_SIZE)
    process.terminate()

    if not audio_bytes:
        print("❌ Error: Could not capture audio.")
        return

    # 2. Hash it (to simulate your actual pipeline)
    digest = hashlib.blake2b(audio_bytes, digest_size=64).digest()

    # 3. Run ENT on the digest
    # We use a temporary file because 'ent' is a bit picky about pipes
    with open("temp_entropy.bin", "wb") as f:
        f.write(digest)

    print("\n--- 📊 MICROPHONE RELIABILITY REPORT ---")
    try:
        result = subprocess.run(['ent', 'temp_entropy.bin'], capture_output=True, text=True)
        print(result.stdout)
        
        # --- THE "SMART" ANALYSIS ---
        # We parse the output to give you a "Verdict"
        output = result.stdout
        
        # Check Entropy Density
        # We look for the line: "Entropy = X.XXXXXX bits per byte"
        try:
            entropy_line = [line for line in output.split('\n') if "Entropy =" in line][0]
            entropy_val = float(entropy_line.split('=')[1].split()[0])
            
            if entropy_val > 7.9:
                print("✅ VERDICT: HIGH-DENSITY CHAOS. This mic is a goldmine.")
            elif entropy_val > 7.5:
                print("⚠️ VERDICT: MODERATE CHAOS. Good for mixing, but don't rely on it alone.")
            else:
                print("❌ VERDICT: WEAK/STRUCTURED. This source is too predictable (likely electrical hum).")
        except:
            print("❌ Error: Could not parse entropy value.")

    except FileNotFoundError:
        print("❌ Error: 'ent' not found. Install it with 'sudo apt install ent'")
    finally:
        import os
        if os.path.exists("temp_entropy.bin"):
            os.remove("temp_entropy.bin")

if __name__ == "__main__":
    run_benchmark()


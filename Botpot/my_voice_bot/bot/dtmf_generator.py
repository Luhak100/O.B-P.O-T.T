import numpy as np
import wave

def generate_dtmf_tone(frequencies, duration=0.5, sample_rate=8000):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    tone = np.sin(2 * np.pi * frequencies[0] * t) + np.sin(2 * np.pi * frequencies[1] * t)
    tone = (tone * 32767).astype(np.int16)  # Scale to 16-bit
    return tone

def save_wave(filename, tone, sample_rate=8000):
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(tone.tobytes())

# Example: Generate tone for key '1' (697 Hz + 1209 Hz)
tone = generate_dtmf_tone([697, 1209])
save_wave('dtmf_tone_1.wav', tone)
print("DTMF tone saved as dtmf_tone_1.wav")
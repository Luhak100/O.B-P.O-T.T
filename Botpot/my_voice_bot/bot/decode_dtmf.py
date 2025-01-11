import dtmf
import wave

def decode_dtmf_from_audio(audio_file):
    # Open the WAV audio file
    with wave.open(audio_file, 'rb') as wav_file:
        samples = wav_file.readframes(wav_file.getnframes())
        # Decode the DTMF tones from the audio samples
        tone = dtmf.decode(samples)
        print(f"Decoded DTMF tone: {tone}")

# Replace with your audio file path
audio_file = "path_to_your_audio_file.wav"
decode_dtmf_from_audio(audio_file)
import time
from agora.rtc import RtcEngine, AudioMixingErrorCode
from pydtmf import DTMFDecoder

# Initialize the Agora RtcEngine
rtc_engine = RtcEngine.create('57d09e5be4ad4091baa4d20d11ee484c')
rtc_engine.join_channel('007eJxTYLgrdLmh3Xz9F7FHN78dPvL8UHnQC3Wfk+GMvdoXLWvzdfUUGEzNUwwsU02TUk0SU0wMLA2TEhNNUowMUgwNU1NNLEyS9a40pTcEMjJceXmJhZEBAkF8fgbnjMTiVJfUktSiotS85FQGBgCTDyZV', 'testChannel', None, 0)

# Initialize the DTMF Decoder
decoder = DTMFDecoder(sample_rate=8000)

def play_audio_segment(rtc_engine, audio_file_path):
    """
    Plays an audio file segment through the Agora channel.
    """
    result = rtc_engine.start_audio_mixing(audio_file_path, loopback=False, replace_microphone=False, cycle=1)
    if result != AudioMixingErrorCode.AUDIO_MIXING_ERROR_OK:
        print(f"Error playing audio: {result}")
        return False

    # Wait for the segment to finish playing
    while rtc_engine.get_audio_mixing_duration() > rtc_engine.get_audio_mixing_current_position():
        time.sleep(1)
    rtc_engine.stop_audio_mixing()
    return True

def listen_for_dtmf(rtc_engine, timeout=10):
    """
    Listens for DTMF tones within a given timeout period.
    """
    print("Waiting for DTMF input...")
    end_time = time.time() + timeout

    while time.time() < end_time:
        frame = rtc_engine.get_audio_frame()  # Get an audio frame (simulated function)
        if frame:
            dtmf_tone = decoder.decode(frame.samples)
            if dtmf_tone:
                print(f"Detected DTMF tone: {dtmf_tone}")
                return dtmf_tone

    print("No DTMF input detected.")
    return None

# Define the flow
def interactive_flow():
    # Play the first segment
    play_audio_segment(rtc_engine, 'intro1.wav')

    # Play the second segment
    play_audio_segment(rtc_engine, 'intro2.wav')

 # Play the options segment
    play_audio_segment(rtc_engine, 'optionns1.wav')

    # Wait for DTMF input
    tone = listen_for_dtmf(rtc_engine, timeout=10)

    if tone == '1':
        # Fraudulent transaction
        play_audio_segment(rtc_engine, 'if1.wav')
    elif tone == '2':
        # Authorized transaction
        play_audio_segment(rtc_engine, 'if2.wav')
    else:
        play_audio_segment(rtc_engine, 'tryagain.wav')

# Run the flow
interactive_flow()

# Leave the channel and clean up
rtc_engine.leave_channel()
rtc_engine.destroy()

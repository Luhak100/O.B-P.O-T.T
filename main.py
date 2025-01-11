from bot.agora_service import VoiceBotService
from agora.rtc.agora_service import AgoraServiceConfig, RTCConnConfig, AgoraService
from agora.rtc.audio_frame_observer import AudioFrame, IAudioFrameObserver
from agora.rtc.audio_pcm_data_sender import PcmAudioFrame
from agora.rtc.local_user import LocalUser
from agora.rtc.local_user_observer import IRTCLocalUserObserver
from agora.rtc.rtc_connection import RTCConnection, RTCConnInfo
from agora.rtc.rtc_connection_observer import IRTCConnectionObserver
from pyee import AsyncIOEventEmitter


# Replace these with your actual values
APP_ID = "57d09e5be4ad4091baa4d20d11ee484c"
TOKEN = "007eJxTYLgrdLmh3Xz9F7FHN78dPvL8UHnQC3Wfk+GMvdoXLWvzdfUUGEzNUwwsU02TUk0SU0wMLA2TEhNNUowMUgwNU1NNLEyS9a40pTcEMjJceXmJhZEBAkF8fgbnjMTiVJfUktSiotS85FQGBgCTDyZV"  # Replace with None if tokens are not enabled
CHANNEL_NAME = "dtmf-test-channel"

class CustomAudioFrameObserver(IAudioFrameObserver):
    def on_audio_frame(self, audio_frame: AudioFrame):
        # Custom logic to handle the audio frame
        print("Received audio frame:", audio_frame)

class CustomLocalUserObserver(IRTCLocalUserObserver):
    def on_user_joined(self, uid: int):
        print(f"User {uid} has joined the channel")

def main():
    # Initialize the bot service
    bot = VoiceBotService(app_id=APP_ID, token=TOKEN, channel_name=CHANNEL_NAME)
    
    # Initialize AgoraService for RTC functionality (this is for more advanced RTC setup)
    rtc_config = RTCConnConfig(channel_profile=1, scenario=1)  # Set appropriate values for your use case
    agora_service = AgoraService(AgoraServiceConfig(APP_ID, channel_name=CHANNEL_NAME, token=TOKEN))

    # Set up the local user
    local_user = LocalUser()
    local_user.set_role(1)  # Set role as broadcaster or audience, depending on your need
    local_user.add_observer(CustomLocalUserObserver())  # Observe user events

    # Optionally, create a RTC connection
    rtc_connection = RTCConnection(config=rtc_config)
    rtc_connection.add_observer(IRTCConnectionObserver())  # Observe connection events

    # You could also observe and process audio frames if needed
    audio_frame_observer = CustomAudioFrameObserver()
    rtc_connection.add_audio_frame_observer(audio_frame_observer)

    # Start the bot (this part will start the bot, and RTC setup will run in parallel)
    bot.start()

if __name__ == "__main__":
    main()

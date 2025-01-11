import asyncio
from agora.rtc.agora_service import RTCConnConfig, AgoraService, RTCConnection
from agora.rtc.types import ClientRoleType, ChannelProfileType
from pyee import AsyncIOEventEmitter
from asyncio import Future
import logging

logger = logging.getLogger(__name__)

class Channel:
    def __init__(self, rtc: "RtcEngine", options: "RtcOptions") -> None:
        self.loop = asyncio.get_event_loop()
        self.emitter = AsyncIOEventEmitter(self.loop)
        self.connection_state = 0
        self.options = options
        self.remote_users = dict()
        self.rtc = rtc
        self.chat = Chat(self)  # Ensure Chat class is defined somewhere
        self.channelId = options.channel_name
        self.uid = options.uid
        self.enable_pcm_dump = options.enable_pcm_dump
        self.token = options.build_token(rtc.appid, rtc.appcert) if rtc.appcert else ""
        conn_config = RTCConnConfig(
            client_role_type=ClientRoleType.CLIENT_ROLE_BROADCASTER,
            channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,
        )
        self.connection = self.rtc.agora_service.create_rtc_connection(conn_config)

        self.channel_event_observer = ChannelEventObserver(
            self.emitter,
            options=options,
        )
        self.connection.register_observer(self.channel_event_observer)

        self.local_user = self.connection.get_local_user()
        self.local_user.set_playback_audio_frame_before_mixing_parameters(
            options.channels, options.sample_rate
        )
        self.local_user.register_local_user_observer(self.channel_event_observer)
        self.local_user.register_audio_frame_observer(self.channel_event_observer)

        self.media_node_factory = self.rtc.agora_service.create_media_node_factory()
        self.audio_pcm_data_sender = self.media_node_factory.create_audio_pcm_data_sender()
        self.audio_track = self.rtc.agora_service.create_custom_audio_track_pcm(
            self.audio_pcm_data_sender
        )
        self.audio_track.set_enabled(1)
        self.local_user.publish_audio(self.audio_track)

        self.stream_id = self.connection.create_data_stream(False, False)
        self.received_chunks = {}
        self.waiting_message = None
        self.msg_id = ""
        self.msg_index = ""

        self.on("user_joined", lambda agora_rtc_conn, user_id: self.remote_users.update({user_id: True}))
        self.on("user_left", lambda agora_rtc_conn, user_id, reason: self.remote_users.pop(user_id, None))

    async def connect(self) -> None:
        if self.connection_state == 3:
            return

        future = Future()

        def callback(agora_rtc_conn: RTCConnection, conn_info: RTCConnInfo, reason):
            logger.info(f"Connection state changed: {conn_info.state}")
            if conn_info.state == 3:  # Connection successful
                future.set_result(None)
            elif conn_info.state == 5:  # Connection failed
                future.set_exception(Exception(f"Connection failed with state: {conn_info.state}"))

        self.on("connection_state_changed", callback)
        logger.info(f"Connecting to channel {self.channelId} with token {self.token}")
        self.connection.connect(self.token, self.channelId, f"{self.uid}")

        if self.enable_pcm_dump:
            agora_parameter = self.connection.get_agora_parameter()
            agora_parameter.set_parameters("{\"che.audio.frame_dump\":{\"location\":\"all\",\"action\":\"start\",\"max_size_bytes\":\"120000000\",\"uuid\":\"123456789\",\"duration\":\"1200000\"}}")

        try:
            await future
        except Exception as e:
            raise Exception(f"Failed to connect to channel {self.channelId}: {str(e)}") from e
        finally:
            self.off("connection_state_changed", callback)

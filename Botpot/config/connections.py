class ChannelEventObserver(
    IRTCConnectionObserver, IRTCLocalUserObserver, IAudioFrameObserver
):
    def __init__(self, event_emitter: AsyncIOEventEmitter, options: RtcOptions) -> None:
        self.loop = asyncio.get_event_loop()
        self.emitter = event_emitter
        self.audio_streams = dict[int, AudioStream]()
        self.options = options

    def emit_event(self, event_name: str, *args):
        """Helper function to emit events."""
        self.loop.call_soon_threadsafe(self.emitter.emit, event_name, *args)

    def on_connected(
        self, agora_rtc_conn: RTCConnection, conn_info: RTCConnInfo, reason
    ):
        logger.info(f"Connected to RTC: {agora_rtc_conn} {conn_info} {reason}")
        self.emit_event("connection_state_changed", agora_rtc_conn, conn_info, reason)

    def on_disconnected(
        self, agora_rtc_conn: RTCConnection, conn_info: RTCConnInfo, reason
    ):
        logger.info(f"Disconnected from RTC: {agora_rtc_conn} {conn_info} {reason}")
        self.emit_event("connection_state_changed", agora_rtc_conn, conn_info, reason)

    def on_connecting(
        self, agora_rtc_conn: RTCConnection, conn_info: RTCConnInfo, reason
    ):
        logger.info(f"Connecting to RTC: {agora_rtc_conn} {conn_info} {reason}")
        self.emit_event("connection_state_changed", agora_rtc_conn, conn_info, reason)

    def on_connection_failure(self, agora_rtc_conn, conn_info, reason):
        logger.error(f"Connection failure: {agora_rtc_conn} {conn_info} {reason}")
        self.emit_event("connection_state_changed", agora_rtc_conn, conn_info, reason)

    def on_user_joined(self, agora_rtc_conn: RTCConnection, user_id):
        logger.info(f"User joined: {agora_rtc_conn} {user_id}")
        self.emit_event("user_joined", agora_rtc_conn, user_id)

    def on_user_left(self, agora_rtc_conn: RTCConnection, user_id, reason):
        logger.info(f"User left: {agora_rtc_conn} {user_id} {reason}")
        self.emit_event("user_left", agora_rtc_conn, user_id, reason)

    def handle_received_chunk(self, json_chunk):
        chunk = json.loads(json_chunk)
        msg_id = chunk["msg_id"]
        part_idx = chunk["part_idx"]
        total_parts = chunk["total_parts"]
        if msg_id not in self.received_chunks:
            self.received_chunks[msg_id] = {"parts": {}, "total_parts": total_parts}
        if (
            part_idx not in self.received_chunks[msg_id]["parts"]
            and 0 <= part_idx < total_parts
        ):
            self.received_chunks[msg_id]["parts"][part_idx] = chunk
            if len(self.received_chunks[msg_id]["parts"]) == total_parts:
                # all parts received, now recomposing original message and get rid it from dict
                sorted_parts = sorted(
                    self.received_chunks[msg_id]["parts"].values(),
                    key=lambda c: c["part_idx"],
                )
                full_message = "".join(part["content"] for part in sorted_parts)
                del self.received_chunks[msg_id]
                return full_message, msg_id
        return (None, None)

    def on_stream_message(
        self, agora_local_user: LocalUser, user_id, stream_id, data, length
    ):
        # logger.info(f"Stream message", agora_local_user, user_id, stream_id, length)
        (reassembled_message, msg_id) = self.handle_received_chunk(data)
        if reassembled_message is not None:
            logger.info(f"Reassembled message: {msg_id} {reassembled_message}")

    def on_audio_subscribe_state_changed(
        self,
        agora_local_user,
        channel,
        user_id,
        old_state,
        new_state,
        elapse_since_last_state,
    ):
        logger.info(
            f"Audio subscribe state changed: {user_id} {new_state} {elapse_since_last_state}"
        )
        self.emit_event(
            "audio_subscribe_state_changed",
            agora_local_user,
            channel,
            user_id,
            old_state,
            new_state,
            elapse_since_last_state,
        )

    def on_playback_audio_frame_before_mixing(
        self, agora_local_user: LocalUser, channelId, uid, frame: AudioFrame
    ):
        audio_frame = PcmAudioFrame()
        audio_frame.samples_per_channel = frame.samples_per_channel
        audio_frame.bytes_per_sample = frame.bytes_per_sample
        audio_frame.number_of_channels = frame.channels
        audio_frame.sample_rate = self.options.sample_rate
        audio_frame.data = frame.buffer

        self.loop.call_soon_threadsafe(
            self.audio_streams[uid].queue.put_nowait, audio_frame
        )
        return 0

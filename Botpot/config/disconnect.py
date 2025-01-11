async def disconnect(self) -> None:
    """
    Disconnects the channel.
    """
    if self.connection_state == 1:
        return

    disconnected_future = asyncio.Future[None]()

    def callback(agora_rtc_conn: RTCConnection, conn_info: RTCConnInfo, reason):
        self.off("connection_state_changed", callback)
        if conn_info.state == 1:
            disconnected_future.set_result(None)

    self.on("connection_state_changed", callback)
    self.connection.disconnect()
    await disconnected_future

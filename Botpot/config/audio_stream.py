async def subscribe_audio(self, uid: int) -> None:
    """
    Subscribes to the audio of a user.

    Parameters:
        uid: The user ID to subscribe to.
    """
    future = asyncio.Future()

    def callback(
        agora_local_user,
        channel,
        user_id,
        old_state,
        new_state,
        elapse_since_last_state,
    ):
        if new_state == 3:  # Successfully subscribed
            future.set_result(None)

    self.on("audio_subscribe_state_changed", callback)
    self.local_user.subscribe_audio(uid)

    try:
        await future
    except Exception as e:
        raise Exception(
            f"Audio subscription failed for user {uid}: {str(e)}"
        ) from e
    finally:
        self.off("audio_subscribe_state_changed", callback)

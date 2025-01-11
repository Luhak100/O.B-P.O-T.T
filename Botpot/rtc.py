import asyncio
from rtc import RtcEngine  # Import the RtcEngine class from rtc.py

async def main():
    appid = "<Your app Id>"  # Replace with your Agora App ID
    channelId = "demo"  # Replace with your desired channel ID
    uid = "123"  # Replace with your unique user ID

    rtc_engine = RtcEngine(appid)
    channel = await rtc_engine.connect(channelId, uid)

    # Keep the script running to listen for events
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())

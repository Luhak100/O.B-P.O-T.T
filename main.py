from bot.agora_service import VoiceBotService
from config.settings import APP_ID, TOKEN, CHANNEL_NAME

# Replace these with your actual values
APP_ID = "ea25290bc65e497280b3c298bddc9217"
TOKEN = "your-generated-token"  # Use None if tokens are not enabled
CHANNEL_NAME = "your-channel-name"

def main():
    # Initialize the bot service
    bot = VoiceBotService(app_id=APP_ID, token=TOKEN, channel_name=CHANNEL_NAME)

    # Start the bot
    bot.start()

if __name__ == "__main__":
    main()

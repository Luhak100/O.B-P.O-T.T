class RtcEngine:
    def __init__(self, appid: str, appcert: str):
        self.appid = appid
        self.appcert = appcert

        if not appid:
            raise Exception("App ID is required)")

        config = AgoraServiceConfig()
        config.audio_scenario = AudioScenarioType.AUDIO_SCENARIO_CHORUS
        config.appid = appid
        config.log_path = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(os.path.join(os.path.abspath(__file__)))
                )
            ),
            "agorasdk.log",
        )
        self.agora_service = AgoraService()
        self.agora_service.initialize(config)

from pulsarclassification.config.configuration import ConfigurationManager
from pulsarclassification.components.model_pusher import ModelPusher

class ModelPusherPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager()
            model_evaluation_config = config.get_model_evaluation_configuration()
            model_pusher_config = config.get_model_pusher_configuration()
            model_pusher = ModelPusher(
                modelevaluation_config=model_evaluation_config,
                modelpusher_config=model_pusher_config)
            model_pusher.get_model_pusher()
        except Exception as e:
            raise e
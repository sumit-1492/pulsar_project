from pulsarclassification.config.configuration import ConfigurationManager
from pulsarclassification.components.model_trainer import ModelTrainer

class ModelTrainerPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager()
            data_transformation_config = config.get_data_transformation_configuration()
            model_trainer_config = config.get_model_trainer_configuration()
            model_trainer = ModelTrainer(transformation_config=data_transformation_config,
                                        modeltrainer_config = model_trainer_config)
            model_trainer.save_model()
        except Exception as e:
            raise e
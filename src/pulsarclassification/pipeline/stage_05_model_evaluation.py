from pulsarclassification.config.configuration import ConfigurationManager
from pulsarclassification.components.model_evaluation import ModelEvaluation

class ModelEvaluationPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager()
            data_transformation_config = config.get_data_transformation_configuration()
            model_trainer_config = config.get_model_trainer_configuration()
            model_evaluation_config = config.get_model_evaluation_configuration()
            model_evaluator = ModelEvaluation(transformation_config=data_transformation_config,
                                        modeltrainer_config = model_trainer_config,
                                        modelevaluation_config=model_evaluation_config)
            model_evaluator.get_model_evaluation_result()
        except Exception as e:
            raise e
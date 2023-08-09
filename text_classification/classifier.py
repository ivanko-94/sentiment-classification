"""Class for the classification model"""

from logging import getLogger
from pathlib import Path
from typing import List

from datasets import Dataset
from sentence_transformers.losses import CosineSimilarityLoss
from setfit import SetFitModel, SetFitTrainer


class Classifier:
    """Classification interface for the sentiment classification model"""

    log = getLogger(__name__)

    def __init__(
        self, model_name: str = None, cache_dir: Path = None, path_to_trained_model: Path = None
    ):
        assert any(
            param is not None for param in [model_name, path_to_trained_model]
        ), "Either specify model name or path to the trained model"

        if path_to_trained_model is not None:
            assert (
                path_to_trained_model.exists()
            ), f"Model path does not exist: {path_to_trained_model}"
            self.model = SetFitModel.from_pretrained(path_to_trained_model)
            self.log.debug(f"Loaded model from disk: {path_to_trained_model}")
        else:
            self.model = SetFitModel.from_pretrained(model_name, cache_dir=cache_dir)
            self.log.debug(f"Loaded model from Huggingface's model hub: {model_name}")

    def train(
        self,
        train_ds: Dataset,
        test_ds: Dataset,
        batch_size: int = 32,
        num_iterations: int = 20,
        num_epochs: int = 2,
        column_mapping: dict = {"text": "text", "label": "label"},
    ) -> dict:
        """Wrapper for SetFit few-shot-learning training.
        Trains a model from Huggingface's model hub.

        Args:
            train_ds (Dataset): Dataset for training
            test_ds (Dataset): Dataset for evaluation
            batch_size (int, optional): Training batch size.
                Defaults to 32.
            num_iterations (int, optional): Number of pairs to generate for contrastive learning.
                Defaults to 20.
            num_epochs (int, optional): Number of epochs to use for contrastive learning.
                Defaults to 2.

        Returns:
            dict: Metrics from evaluation after training
        """

        # Create an FSL trainer
        trainer = SetFitTrainer(
            model=self.model,
            train_dataset=train_ds,
            eval_dataset=test_ds,
            loss_class=CosineSimilarityLoss,
            batch_size=batch_size,
            num_iterations=num_iterations,
            num_epochs=num_epochs,
            column_mapping=column_mapping,
        )

        trainer.train()
        self.model = trainer.model

        return trainer.evaluate()

    def export(self, path_to_trained_model: Path):
        """Exports trained model to a given path

        Args:
            path_to_trained_model (Path): Location for exporting the model
        """

        assert self.model is not None, "Model is not trained or not loaded"
        self.model.save_pretrained(path_to_trained_model)
        self.log.debug(f"Saved model to {path_to_trained_model}")

    def predict_proba(self, model_input: str) -> List[float]:
        """Predicts class probabilities for a given input

        Args:
            model_input (str): Input to transformer model

        Returns:
            List[float]: class probabilities
        """
        assert self.model is not None, "Model is not trained or not loaded"
        return self.model.predict_proba([model_input])[0]

"""gRPC wrapper for the sentiment classiffication service."""
from concurrent import futures
from logging import getLogger
from pathlib import Path

import grpc
from generated import text_classification_service_pb2 as messages
from generated import text_classification_service_pb2_grpc as service
from generated.text_classification_service_pb2_grpc import TextClassificationService

from text_classification.classifier import Classifier


class SentimentClassificationService(TextClassificationService):
    """gRPC wrapper for the sentiment classiffication service."""

    log = getLogger(__name__)
    classifier = Classifier(
        path_to_trained_model=Path(
            ".trained-models/cardiffnlp/twitter-roberta-base-sentiment/SetFit/SentEval-CR"
        )
    )

    def __init__(self):
        self.log.setLevel("INFO")

    def start(self):
        """Starts the gRPC server."""
        self.log.info("Starting sentiment classification service")
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        service.add_TextClassificationServiceServicer_to_server(
            SentimentClassificationService(), server
        )
        server.add_insecure_port("text-classification-service:9090")
        self.log.info("Starting sentiment classification service")
        Path("start_flag").touch()
        server.start()
        server.wait_for_termination()

    def Classify(self, request, context):
        """Classifies the input text and returns the class probabilities."""
        probability_neg, probability_pos = self.classifier.predict_proba(request.intput_text)

        return messages.Prediction(
            class_name="positive" if probability_pos >= probability_neg else "negative",
            confidence=probability_pos,
        )

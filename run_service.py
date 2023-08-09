"""Entrypoint for the sentiment classification service."""
from logging import getLogger
from text_classification.service import SentimentClassificationService


if __name__ == "__main__":
    getLogger(__name__).info("Starting sentiment classification service")
    service = SentimentClassificationService()
    service.start()

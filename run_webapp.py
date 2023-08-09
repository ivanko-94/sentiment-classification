"""Entrypoint for a web-based client to support interaction with the text classification service"""

import grpc
import streamlit as st

from generated import text_classification_service_pb2 as messages
from generated import text_classification_service_pb2_grpc as service

st.title("Sentiment Text Classification")
text_input = st.text_input("Enter text")
classify_button = st.button("Classify")

# each button click trigger a gRPC request
if classify_button:

    # name: text-classification-service is available in the docker network
    with grpc.insecure_channel("text-classification-service:9090") as channel:
        stub = service.TextClassificationServiceStub(channel)
        response = stub.Classify(request=messages.InputText(intput_text=text_input))

    st.write(f"Sentiment: {response.class_name} {'👍' if response.class_name == 'positive' else '👎'} ")
    st.write(f"Confidence: {response.confidence}")
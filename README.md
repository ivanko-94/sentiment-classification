
  

This repository illustrates how [sentiment classification](https://huggingface.co/datasets/SetFit/SentEval-CR) can reach an accuracy of ~0.9 using as little as 4 examples per class. To achieve this, I utilise a few-shot-learning approach from [SetFit](https://huggingface.co/blog/setfit) and leverage a pre-trained [roBEARTa](https://arxiv.org/abs/1907.11692) model [from Hugging Face 🤗]((https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment)). To enable user interaction, I built a simple web app. Furthermore, both components are run as docker images, which communicate using gRPC calls.

  

  

Artifacts are checked-in in: `.dataset`, `.pre-trained-models`, `.trained-models` folders.

  

  

There are two entities:

  

* Training a sentiment classification transformer model using SetFit 🤗

  

* Deploying a trained model mounted inside a Docker container, building a simple web app and enabling communication through the gRPC interface.

  

  

## Model Training 🧠

  

Model training is described through two jupyter notebooks based on the use cases:

  

* [train_sentiment.ipynb](https://github.com/ivanko-94/sentiment-classification/blob/main/train_sentiment.ipynb) - Describes how a transformer can be trained to classify customer reviews. Products of this training are used in the deployment section

  

* [train_sms_spam.ipynb](https://github.com/ivanko-94/sentiment-classification/blob/main/train_sms_spam.ipynb) - Investigates sms spam classification use case. It is not as documented as the sentiment analysis and is used only to investigate SMS spam classification feasibility.

  

  

Before running the notebooks, please prepare the dev environment by executing the following commands:

  

*  `conda create -n text-classification python=3.8`

  

*  `conda activate text-classification`

  

*  `pip install -r requirements/requirements_service.txt`

  

*  `pip install ipykernel ipywidgets matplotlib`

  

*  `pip install -e .`

  

  

## Deployment 🚗

  

The support code for sentiment classification is released as a docker image, whereas the model binaries are mounted on runtime, which ensures that containers are slim and flexible. Three core components are: Communication, Classification Service, Web App.

  

  

### Communication

  

Communication between docker containers is facilitated using [gRPC](https://grpc.io/), which is suitable for [Python integration](https://grpc.io/docs/languages/python/quickstart/). A simple communication service is defined in .proto files and the python interface is generated automatically. If using Intel platforms, command: [make generated](https://github.com/ivanko-94/sentiment-classification/blob/main/Makefile#L9C5-L9C5) automatically generates interface. If working with M1 Macs, I've uploaded the generated proto files.

  

  

### Service

  

The classification service container receives gRPC calls, invokes the classification model and returns the class confidence and the label. The source code for the classification service is split into [technology code](https://github.com/ivanko-94/sentiment-classification/blob/main/text_classification/classifier.py#L12), which facilitates training and inference, and the [service code](https://github.com/ivanko-94/sentiment-classification/blob/main/text_classification/service.py#L14), which serves as a wrapper interface. The split is done to follow the single responsibility principle and functional code decomposition.

  

* [make service](https://github.com/ivanko-94/sentiment-classification/blob/main/Makefile#L15) - will build a classification service container as specified in the [Dockerfile](https://github.com/ivanko-94/sentiment-classification/blob/main/dockerfiles/Dockerfile.service) and will start the [text classification service](https://github.com/ivanko-94/sentiment-classification/blob/main/run_service.py#L9).

  

  

### Web App

  

In our case, UI is a simple Streamlit application. "Streamlit is an open-source Python library that makes it easy to create and share beautiful, custom web apps for machine learning and data science." [\[1\]](https://docs.streamlit.io/)

  

* [make webapp](https://github.com/ivanko-94/sentiment-classification/blob/main/Makefile#L18) - will build a web interface image as specified in the [Dockerfile](https://github.com/ivanko-94/sentiment-classification/blob/main/dockerfiles/Dockerfile.webapp) and will run web application as [entry point](https://github.com/ivanko-94/sentiment-classification/blob/main/run_webapp.py).

  

  

### How to deploy the model?

  

After successfully building Docker images for [service](https://github.com/ivanko-94/sentiment-classification/blob/main/Makefile#L15) and [web app](https://github.com/ivanko-94/sentiment-classification/blob/main/Makefile#L9):

  

* [make up](https://github.com/ivanko-94/sentiment-classification/blob/main/Makefile#L21) - will start both containers

  

* open `http://localhost:8501` and try to classify customer reviews.

  

  

Once docker containers successfully start, the application will look like the screenshot below.

  

  

![Web App screenshot](https://github.com/ivanko-94/sentiment-classification/blob/main/figures/app_screenshot.png)
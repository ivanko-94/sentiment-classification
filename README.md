This repository consists of two elements:
* Training a sentiment classification transformer model using SetFit 🤗
* Deploying a trained model as a Docker image; building a simple web app and enabling communication through gRPC interface.

## Model Training 🧠
Model training is described through two jupyter notebooks based on the use cases:
* `train_sentiment.ipynb` - Describes how a transformer can be trained to classify customer reviews. Products of this training are used in the deployment section
* `train_sms_spam.ipynb` - Investigates sms spam classification use case. It is not as documented as the sentiment analysis and is used only to investigate SMS spam classification feasibility.

Before running the notebooks, please prepare the dev environment by executing the following commands:
* `conda create -n text-classification python=3.8`
* `conda activate text-classification`
* `pip install -r requirements/requirements_service.txt`
* `pip install ipykernel ipywidgets matplotlib`
* `pip install -e .`

## Deployment 🚗
The support code for sentiment classification is released as a docker image, whereas the model binaries are mounted on runtime, which ensures that containers are slim and flexible. Three core components are: Communication, Classification Service, Web App.

### Communication
Communication between docker containers is facilitated using [gRPC](https://grpc.io/), which is suitable for [Python integration](https://grpc.io/docs/languages/python/quickstart/). A simple communication service is defined in .proto files and the python interface is generated automatically. If using Intel platforms, command:  `make generated` automatically generates interface. If working with M1 Macs, I've uploaded the generated proto files.

### Service
The classification service container receives gRPC calls, invokes the classification model and returns the class confidence and the label.

### Web App
In our case, UI is a simple Streamlit application. "Streamlit is an open-source Python library that makes it easy to create and share beautiful, custom web apps for machine learning and data science." [\[1\]](https://docs.streamlit.io/)

### How to deploy the model?
`make service`
`make webapp`
`make up`

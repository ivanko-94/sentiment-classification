
# Tasks

* Choose a text classification problem for yourself, e.g., sentiment analysis, emotion detection, spam detection, or topic classification of news articles.

* Develop a machine learning model that takes a string as input and predicts a corresponding label. You should leverage a pre-trained model of your choice (e.g., a BERT-like model from Huggingface), otherwise, you can use any appropriate NLP techniques and machine learning algorithms for this task.

* Include a Python script that loads your trained model and executes it interactively on user input from the console. Alternatively, you can provide a simple web application or API to demonstrate its functionality.

  

# Text Classification Problem

As a demonstration of sentiment classification, I used [SentEval-CR](https://huggingface.co/datasets/SetFit/SentEval-CR) dataset from huggingface. As described in the [original paper](https://dl.acm.org/doi/10.1145/1014052.1014073), this dataset contains customer reviews in the e-commerce domain. The test split was created by randomly sampling 20% of the original data (753 samples), and the train split is the remaining 80% (3012 samples). Upon investigating class balance, one can observe that positive reviews dominate with roughly a 2:1 ratio, equally spanning across test and train subsets. This dataset faithfully describes a real-world text classification use case. For more detailed information about how this dataset was used, please refer to: `train_sentiment.ipynb`. Furthermore, out of curiosity, SMS spam classification is investigated, by developing a model to classify SMS messages. The dataset can be found on the [Hugging Face website](https://huggingface.co/datasets/sms_spam), and more details are contained in the `train_sms_spam.ipynb`.

  

# Develop an ML Model

Training code can be found in two `.ipynb` notebooks, which are checked in. For this task, I used [SetFit](https://huggingface.co/blog/setfit), a robust and reliable mechanism that trains transformer models using only a few examples.

There are multiple benefits to training a transformer-based classifier using SetFit.

* Few Shot Learning approach is essential for use cases which have an insufficient amount of data or where data labelling is an expensive task. Furthermore, an approach that quickly learns insights from a few examples is a good foundation for incremental improvement or active learning.

* Training a model using SetFit and FSL requires little compute infrastructure and can be completed quickly compared to traditional model training. As it shortens the development cycles, and increases response to data shifts, or the necessity to adapt the model to new tasks, SetFit is ideal for prototyping and R&D.

* FSL approach does not work well only with text, but also images. As contrastive learning is a general concept, one can easily use [transformers for images](https://huggingface.co/sentence-transformers/clip-ViT-B-32).

Two following figures show how the performance of this FSL method scales with the number of samples. Decent performance can be reached with very few samples per class.

![Performance of the sentiment classification model vs number of training samples](https://github.com/ivanko-94/sentiment-classification/blob/sentiment-classification-service/figures/sentiment-performance-curve.png)

![Performance of the SMS classification model vs number of training samples](https://github.com/ivanko-94/sentiment-classification/blob/sentiment-classification-service/figures/sms-performance-curve.png)

  

To further improve the sentiment model, [pre-trained roBERTa model](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment) is used. It was trained on a similar task (Twitter sentiment analysis). This allows us to achieve excellent performance (**accuracy ~0.9**) with only 4 samples of each class. Furthermore, the model achieves a throughput of >30 samples/sec, making it real-time-capable.
SMS spam classification task was more straightforward, and the model was able to achieve staggering accuracy of 0.98 using 32 samples of each class.

  

# Demonstrating Functionality

Once the model is trained, it can be integrated into its environment. Instead of invoking it using a simple script, one can make a web app. The block schema below describes the system design. Each component is a separate entity, released as a docker image. 
![System Block Diagram](https://github.com/ivanko-94/sentiment-classification/blob/sentiment-classification-service/figures/sys-design.png)

Web App is written as a simple [Streamlit](https://streamlit.io/) app. Through its simplicity, Streamlit shifts the focus to ML development and not UI design.

Classification container is released **without** model weights. This decision is to make the image as slim as possible and flexible to adding new models or efficiently replacing model weights. Instead, the folder containing the weights is mounted to the container, as specified in the [docker compose](https://github.com/ivanko-94/sentiment-classification/blob/sentiment-classification-service/docker-compose.yml#L21).

Communication between docker containers is achieved by using [rpc calls](https://github.com/ivanko-94/sentiment-classification/blob/sentiment-classification-service/proto/text_classification_service.proto#L8). Given that generating code from `.proto` files relies on `grpcio.tools`, which are poorly supported on Mac M1 chips, generated code is checked in. To regenerate the code, please run `make generated`

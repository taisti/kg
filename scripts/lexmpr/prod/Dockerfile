FROM python:3.7-slim
RUN apt-get update &&\
	apt-get -y install git
COPY app /app
# container: cd app
WORKDIR /app

# set environment variable to import from src
ENV PYTHONPATH=$PYTHONPATH:/app

# install required packages in docker environment
RUN pip3 install -r requirements.txt

# download LexMapr
RUN git clone https://github.com/taisti/LexMapr.git

# install LexMapr in current environment
RUN pip3 install ./LexMapr

# required for lexmapr
RUN python3 -c "import nltk;nltk.download('punkt');"

# run REST application
CMD python3 src/main.py
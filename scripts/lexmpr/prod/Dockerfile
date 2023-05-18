FROM python:3.7-slim
# container: find and install git
RUN apt-get update &&\
	apt-get -y install git

# copy directory app from local to docker container
COPY app /app

# container: cd app
WORKDIR /app

# container: set environment variable to import from src
ENV PYTHONPATH=$PYTHONPATH:/app

# container: install required packages in docker environment
RUN pip3 install -r requirements.txt

# container: download LexMapr
RUN git clone https://github.com/taisti/LexMapr.git

# container: install LexMapr in current environment
RUN pip3 install ./LexMapr

# container: run python3 script from string to download punkt
# required for lexmapr
RUN python3 -c "import nltk;nltk.download('punkt');"

# container: run REST application
CMD python3 src/main.py
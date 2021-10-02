FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

COPY . . 

RUN mkdir downloads
RUN apt-get update && apt-get install -y ffmpeg libpython3-dev build-essential python-wheel python-dev

RUN pip install -U pip
RUN pip install -r requirements.txt


CMD ["python3", "bot.py"]
FROM python:latest

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY *.py ./

VOLUME db

VOLUME work

COPY config.yaml config.yaml

ADD archetype archetype

CMD [ "python", "main.py" ]
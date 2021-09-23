FROM python:3.9-slim-buster

RUN python3 -m pip install --upgrade pip

RUN apt-get update \
    && apt-get -y install libpq-dev gcc postgresql

RUN useradd --create-home --shell /bin/bash worker
USER worker

WORKDIR /home/worker/code

COPY --chown=worker:worker requirements.txt requirements.txt
RUN python3 -m pip install --user -r requirements.txt

COPY --chown=worker:worker . .

EXPOSE 5000

CMD ["python3", "main.py"]
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

# CMD ["bash"]
CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]
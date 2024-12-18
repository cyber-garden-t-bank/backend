FROM python:slim
LABEL authors="exizman"

WORKDIR /app

COPY ./ml-worker/requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED=1

ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_HOST
ARG POSTGRES_PORT
ARG POSTGRES_NAME


ENV POSTGRES_USER=$POSTGRES_USER
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD
ENV POSTGRES_HOST=$POSTGRES_HOST
ENV POSTGRES_PORT=$POSTGRES_PORT
ENV POSTGRES_NAME=$POSTGRES_NAME



COPY ./ml-worker ./ml-worker
COPY ./db ./ml-worker/db




ENTRYPOINT ["python"]
CMD ["ml-worker/worker_entrypoint.py"]
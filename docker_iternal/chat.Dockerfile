FROM python:slim
LABEL authors="exizman"

WORKDIR /app

COPY ./core/requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1


ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_PORT
ARG POSTGRES_NAME


ENV POSTGRES_USER=$POSTGRES_USER
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD
ENV POSTGRES_HOST=$POSTGRES_HOST
ENV POSTGRES_PORT=$POSTGRES_PORT
ENV POSTGRES_NAME=$POSTGRES_NAME




COPY ./chatbot /app/chatbot
COPY ./db /app/db

COPY ./common /app/common


ENTRYPOINT ["uvicorn", "chatbot.run_web:app", "--host", "0.0.0.0", "--port", "8002"]
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./perekrestok_parser/ /app/perekrestok_parser

CMD ["perekrestok_parser/python", "app.py"]


```bash
docker compose up -d
```

python 3.8

```bash
pip install -r ./diksi_parser/requirements.txt
```

```bash
pip install -r ./perekrestok_parser/requirements.txt
```

flipped workers

```bash
python ./diksi_parser/local_app.py
```

```bash
python ./perekrestok_parser/local_app.py
```

consumer (Yura fix request)

```bash
python ./test-kafka/consumer.py
```
send tasks

```bash
python ./test-kafka/producer.py
```
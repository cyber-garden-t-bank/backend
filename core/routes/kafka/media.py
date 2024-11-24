import os

from confluent_kafka import Producer
from fastapi import File, UploadFile, APIRouter
from io import BytesIO


router = APIRouter(
    prefix="/finance",
    tags=["media"],
)

kafka_brokers = os.getenv("KAFKA_BROKERS")

kafka_producer = Producer({
        'bootstrap.servers': kafka_brokers,
        'broker.address.family': 'v4'# Update with your Kafka broker address
    })

@router.post("/upload/")
async def upload_file(img: UploadFile = File(...)):
    img_bytes = await img.read()
    kafka_producer.produce(img_bytes.decode('utf-8'), 'qr_process')
    return {'lol':"kek"}

# Запустите приложение с помощью uvicorn:
# uvicorn your_module_name:app --reload

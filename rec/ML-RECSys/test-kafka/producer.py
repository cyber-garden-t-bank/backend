import asyncio
from aiokafka import AIOKafkaProducer
import json

async def produce_messages():
    producer = AIOKafkaProducer(
        bootstrap_servers='localhost:9093',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    await producer.start()

    try:
        tasks = [
            {"task": "Торт", "store": "perekrestok"},
            {"task": "Суши", "store": "diksi"},
            {"task": "Мясо", "store": "perekrestok"},
            {"task": "Хлеб", "store": "diksi"}
        ]

        for task in tasks:
            print(f"Producing: {task}")
            await producer.send_and_wait('parse_tasks', task)
            await asyncio.sleep(1)
    finally:
        await producer.stop()

if __name__ == "__main__":
    asyncio.run(produce_messages())
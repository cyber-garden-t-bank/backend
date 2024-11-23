import asyncio
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import json

async def process_message(message):
    task = message['task']
    return f"{task[::-1]}"  # Reverse the task string

async def flipped_buffer_processor():
    consumer = AIOKafkaConsumer(
        'parse_tasks',
        bootstrap_servers='localhost:9093',
        group_id='flipped_processor_group',
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    producer = AIOKafkaProducer(
        bootstrap_servers='localhost:9093',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    await consumer.start()
    await producer.start()

    try:
        async for message in consumer:
            print(f"Processing: {message.value}")
            flipped_task = await process_message(message.value)
            print(f"Produced flipped task: {flipped_task}")
            await producer.send_and_wait('parse_results', {'flipped_task': flipped_task})
    finally:
        await consumer.stop()
        await producer.stop()

if __name__ == "__main__":
    asyncio.run(flipped_buffer_processor())
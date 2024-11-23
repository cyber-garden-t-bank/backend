import asyncio
from aiokafka import AIOKafkaConsumer
import asyncpg
import json

PG_DSN = "postgresql://postgres:postgres@localhost:5432/postgres"

# Создание таблицы, если её ещё нет
CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS parse_results (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    price TEXT NOT NULL,
    url TEXT UNIQUE NOT NULL
);
"""

# Вставка данных, если записи с таким URL ещё нет
INSERT_QUERY = """
INSERT INTO parse_results (title, price, url)
VALUES ($1, $2, $3)
ON CONFLICT (url) DO NOTHING;
"""

async def init_db():
    """Инициализация базы данных и создание таблицы."""
    conn = await asyncpg.connect(PG_DSN)
    try:
        await conn.execute(CREATE_TABLE_QUERY)
    finally:
        await conn.close()

async def save_result_to_db(data):
    """Сохранение результата в базу данных, если запись уникальна."""
    conn = await asyncpg.connect(PG_DSN)
    try:
        await conn.execute(INSERT_QUERY, data['title'], data['price'], data['url'])
    finally:
        await conn.close()

async def consume_results():
    """Чтение данных из Kafka и сохранение в базу данных."""
    consumer = AIOKafkaConsumer(
        'parse_results',
        bootstrap_servers='localhost:9093',
        group_id='results_consumer_group',
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )

    await consumer.start()
    await init_db()

    try:
        async for message in consumer:
            data = message.value
            print(f"Consumed result: {data}")
            await save_result_to_db(data)
    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(consume_results())
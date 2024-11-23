import asyncio
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import json
from aiohttp import ClientSession
from parsel import Selector


async def fetch_html(session, url):
    """Функция для получения HTML страницы."""
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        print(f"Ошибка при запросе {url}: {e}")
        return ""


async def search_for_word(word):
    """Функция для поиска слова на сайте."""
    base_url = "https://www.perekrestok.ru"
    url = f"{base_url}/cat/search?search={word}"
    result = []

    async with ClientSession() as session:
        html = await fetch_html(session, url)
        if not html:
            return {"error": "Не удалось получить HTML"}

        selector = Selector(html)
        products = selector.css("div.product-card-wrapper")

        if not products:
            return {"error": f"Слово '{word}' не найдено на сайте"}

        for product in products:
            title = product.css("span.product-card__link-text::text").get()
            price = product.css("div.price-new::text").getall()
            link = product.css("a.product-card__link::attr(href)").get()

            price_cleaned = " ".join(p.strip() for p in price if p.strip())

            if title and price_cleaned and link:
                result.append({
                    "title": title,
                    "price": price_cleaned,
                    "url": f"{base_url}{link}"
                })
                

    return result


async def process_message(message):
    """Обработка сообщения: поиск слова на сайте."""
    store = message.get('store', '')
    if store != 'perekrestok':
        print(f"Сообщение игнорируется, так как store='{store}'")
        return None

    word = message.get('task', '')
    if not word:
        return {"error": "No task provided"}
    
    print(f"Обработка задачи для магазина: {store}, слово: {word}")
    return await search_for_word(word)


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
            print(f"Получено сообщение: {message.value}")
            result = await process_message(message.value)
            if result is not None:  # Если задача обработана
                print(f"Отправка результата: {result}")
                await producer.send_and_wait('parse_results', result)
            else:
                print("Сообщение пропущено.")
    finally:
        await consumer.stop()
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(flipped_buffer_processor())
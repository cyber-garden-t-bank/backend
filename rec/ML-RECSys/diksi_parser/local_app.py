import asyncio
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import json
from playwright.async_api import async_playwright


async def diksi_parsing(request_word):
    """Parse Diksi data asynchronously using Playwright."""
    data = []
    base_url = "https://dixy.ru"
    url = f"{base_url}/catalog/search.php?q={request_word}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)

        # Дожидаемся загрузки всех карточек
        await page.wait_for_selector("article.card.bs-state")

        # Извлекаем карточки товаров
        product_cards = await page.query_selector_all("article.card.bs-state")
        for product in product_cards:
            try:
                title = await product.query_selector("h3.card__title")
                title_text = await title.inner_text() if title else "Unknown"

                price = await product.query_selector("div.card__price-num")
                price_text = await price.inner_text() if price else "Unknown"

                link = await product.query_selector("a.card__link")
                link_href = await link.get_attribute("href") if link else "#"
                full_link = base_url + link_href

                data.append(
                    {
                        "title": title_text.strip(),
                        "price": price_text.strip(),
                        "url": full_link.strip(),
                    }
                )
            except Exception as e:
                print(f"Error parsing product: {e}")
                continue

        await browser.close()

    return data


async def process_message(message):
    """Обработка сообщения: поиск товаров на сайте Дикси."""
    store = message.get('store', '')
    if store != 'diksi':
        print(f"Сообщение игнорируется, так как store='{store}'")
        return None

    word = message.get('task', '')
    if not word:
        return {"error": "No task provided"}

    print(f"Обработка задачи для магазина: {store}, слово: {word}")
    return await diksi_parsing(word)


async def flipped_buffer_processor():
    consumer = AIOKafkaConsumer(
        'parse_tasks',
        bootstrap_servers='localhost:9093',
        group_id='flipped_processor_group_diksi',
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

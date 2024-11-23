import asyncio
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
    
    async with ClientSession() as session:
        html = await fetch_html(session, url)
        if not html:
            print("Не удалось получить HTML.")
            return
        
        selector = Selector(html)
        products = selector.css("div.product-card-wrapper")
        
        if not products:
            print(f"Слово '{word}' не найдено на сайте.")
        else:
            print(f"Найденные товары для '{word}':")
            for product in products:
                title = product.css("span.product-card__link-text::text").get()
                price = product.css("div.price-new::text").getall()
                link = product.css("a.product-card__link::attr(href)").get()
                
                price_cleaned = " ".join(p.strip() for p in price if p.strip())
                
                if title and price_cleaned and link:
                    print(f"Название: {title}")
                    print(f"Цена: {price_cleaned}")
                    print(f"Ссылка: {base_url}{link}")
                    print("-" * 40)

if __name__ == "__main__":
    asyncio.run(search_for_word("торт"))
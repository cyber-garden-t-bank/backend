import asyncio
import csv
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

async def search_for_word(word, session, base_url="https://www.perekrestok.ru"):
    """Функция для поиска слова на сайте."""
    url = f"{base_url}/cat/search?search={word}"
    html = await fetch_html(session, url)
    if not html:
        print(f"Не удалось получить HTML для слова '{word}'.")
        return []

    selector = Selector(html)
    products = selector.css("div.product-card-wrapper")
    
    if not products:
        print(f"Слово '{word}' не найдено на сайте.")
        return []
    
    data = []
    for product in products:
        try:
            title = product.css("span.product-card__link-text::text").get()
            price = product.css("div.price-new::text").getall()
            link = product.css("a.product-card__link::attr(href)").get()
            
            price_cleaned = " ".join(p.strip() for p in price if p.strip())
            
            if title and price_cleaned and link:
                data.append({
                    "search_word": word,
                    "title": title.strip(),
                    "price": price_cleaned.strip(),
                    "url": base_url + link.strip()
                })
        except Exception as e:
            print(f"Ошибка при обработке продукта для слова '{word}': {e}")
    
    return data

async def main():
    search_words = [
        "Молоко", "Хлеб", "Яйца", "Сыр", "Масло сливочное", "Йогурт", "Кефир", "Творог", "Сметана",
        "Куриное филе", "Говядина", "Свинина", "Рыба", "Колбаса", "Сосиски", "Макароны", "Рис",
        "Гречка", "Овсянка", "Мука", "Сахар", "Соль", "Перец черный", "Чай черный", "Кофе молотый",
        "Шоколад", "Конфеты", "Варенье", "Мед", "Масло подсолнечное", "Масло оливковое", "Майонез",
        "Кетчуп", "Горчица", "Лук репчатый", "Чеснок", "Картофель", "Морковь", "Помидоры", "Огурцы",
        "Капуста белокочанная", "Яблоки", "Бананы", "Апельсины", "Груши", "Виноград", "Клубника",
        "Сок яблочный", "Вода питьевая", "Минеральная вода", "Авокадо", "Киви", "Манго", "Ананас",
        "Слива", "Персик", "Нектарин", "Черника", "Малина", "Клюква", "Шампиньоны", "Белые грибы",
        "Кукуруза консервированная", "Горошек консервированный", "Фасоль консервированная", "Оливки",
        "Маслины", "Тунец консервированный", "Скумбрия консервированная", "Сельдь соленая",
        "Крабовые палочки", "Кальмары", "Креветки", "Мидии", "Капуста брокколи", "Цветная капуста",
        "Шпинат", "Зеленый горошек", "Спаржа", "Батат", "Свекла", "Имбирь", "Лимон", "Лайм", "Гранат",
        "Арбуз", "Дыня", "Изюм", "Орехи грецкие", "Миндаль", "Фисташки", "Кешью", "Семечки подсолнечника",
        "Тыквенные семечки", "Финики", "Инжир", "Ржаной хлеб", "Печенье овсяное", "Мороженое ванильное",
        "Торт шоколадный"
    ]

    # Сохраняем все результаты
    all_results = []

    async with ClientSession() as session:
        for word in search_words:
            try:
                results = await search_for_word(word, session)
                all_results.extend(results)
                print(f"Найдено {len(results)} товаров для слова '{word}'.")
            except Exception as e:
                print(f"Ошибка при обработке слова '{word}': {e}")
                continue

    # Сохранение в CSV
    output_file = "perekrestok_products.csv"
    with open(output_file, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["search_word", "title", "price", "url"])
        writer.writeheader()
        writer.writerows(all_results)

    print(f"Сохранено {len(all_results)} записей в файл '{output_file}'.")

if __name__ == "__main__":
    asyncio.run(main())
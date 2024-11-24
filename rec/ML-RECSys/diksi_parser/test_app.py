import asyncio
import csv
from playwright.async_api import async_playwright

async def diksi_parsing(request_word, base_url="https://dixy.ru"):
    """Parse Diksi data asynchronously using Playwright for a single search term."""
    data = []
    url = f"{base_url}/catalog/search.php?q={request_word}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto(url)
            await page.wait_for_selector("article.card.bs-state", timeout=10000)  # Timeout 10s for loading cards

            # Extract product cards
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
                            "search_word": request_word,
                            "title": title_text.strip(),
                            "price": price_text.strip(),
                            "url": full_link.strip(),
                        }
                    )
                except Exception as e:
                    print(f"Error parsing product for word '{request_word}': {e}")
                    continue
        except Exception as e:
            print(f"Error loading page for word '{request_word}': {e}")
        finally:
            await browser.close()

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

    # Results will be stored in a list
    all_results = []

    for word in search_words:
        try:
            results = await diksi_parsing(word)
            all_results.extend(results)
            print(f"Parsed {len(results)} results for '{word}'")
        except Exception as e:
            print(f"Error parsing '{word}': {e}")
            continue

    # Save results to a CSV file
    output_file = "diksi_products.csv"
    with open(output_file, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["search_word", "title", "price", "url"])
        writer.writeheader()
        writer.writerows(all_results)

    print(f"Saved {len(all_results)} results to '{output_file}'")

if __name__ == "__main__":
    asyncio.run(main())
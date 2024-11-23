import asyncio
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

if __name__ == "__main__":
    request_word = "торт"
    results = asyncio.run(diksi_parsing(request_word))
    print(f"Found {len(results)} results for '{request_word}':")
    for result in results:
        print(result)
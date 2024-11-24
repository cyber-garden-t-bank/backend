# from generic_actor import GenericKafkaActor
#
#
# async def search_for_word(word):
#     """Функция для поиска слова на сайте."""
#     base_url = "https://www.perekrestok.ru"
#     url = f"{base_url}/cat/search?search={word}"
#     result = []
#
#     async with ClientSession() as session:
#         html = await fetch_html(session, url)
#         if not html:
#             return {"error": "Не удалось получить HTML"}
#
#         selector = Selector(html)
#         products = selector.css("div.product-card-wrapper")
#
#         if not products:
#             return {"error": f"Слово '{word}' не найдено на сайте"}
#
#         for product in products:
#             title = product.css("span.product-card__link-text::text").get()
#             price = product.css("div.price-new::text").getall()
#             link = product.css("a.product-card__link::attr(href)").get()
#
#             price_cleaned = " ".join(p.strip() for p in price if p.strip())
#
#             if title and price_cleaned and link:
#                 result.append({
#                     "title": title,
#                     "price": price_cleaned,
#                     "url": f"{base_url}{link}"
#                 })
#
#     return result
#
#
# async def process_message(message):
#     """Обработка сообщения: поиск слова на сайте."""
#     store = message.get('store', '')
#     if store != 'perekrestok':
#         print(f"Сообщение игнорируется, так как store='{store}'")
#         return None
#
#
#
# class ExpenseAnalyticsActor(GenericKafkaActor):
#     def __init__(self, message):
#         self.message = message
#         self.result = None
#
#     def process(self, data):
#         word = self.message.get('task', '')
#         if not word:
#             return {"error": "No task provided"}
#
#
#         self.result = search_for_word(word)
#
#     def output(self):
#         pass
#
#
#
#

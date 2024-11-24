from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.datasets import Dataset
from airflow.utils.dates import days_ago
from airflow.models import Variable
import asyncio
import csv
from aiohttp import ClientSession
from parsel import Selector
import boto3

S3_BUCKET_NAME = "hackgarden2024"
S3_KEY = "datasets/perekrestok_products.csv"

S3_ENDPOINT = Variable.get("S3_ENDPOINT")
S3_ACCESS_KEY = Variable.get("S3_ACCESS_KEY")
S3_SECRET_KEY = Variable.get("S3_SECRET_KEY")

example_dataset = Dataset(f"s3://{S3_BUCKET_NAME}/{S3_KEY}")

async def fetch_html(session, url):
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        print(f"Ошибка при запросе {url}: {e}")
        return ""

async def search_for_word(word, session, base_url="https://www.perekrestok.ru"):
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

def fetch_and_save_perekrestok_products_to_csv():
    async def main():
        search_words = [
            "Молоко", "Хлеб", "Яйца", "Сыр", "Масло сливочное", "Йогурт", "Кефир", "Творог", "Сметана",
            "Куриное филе", "Говядина", "Свинина", "Рыба", "Колбаса", "Сосиски", "Макароны", "Рис",
            "Гречка", "Овсянка", "Мука", "Сахар", "Соль", "Перец черный", "Чай черный", "Кофе молотый",
        ]
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

        with open("perekrestok_products.csv", mode="w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["search_word", "title", "price", "url"])
            writer.writeheader()
            writer.writerows(all_results)
        print(f"Сохранено {len(all_results)} записей в файл 'perekrestok_products.csv'.")

    asyncio.run(main())

def upload_csv_to_s3():
    s3_client = boto3.client(
        "s3",
        endpoint_url=S3_ENDPOINT,
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY,
    )
    s3_client.upload_file("perekrestok_products.csv", S3_BUCKET_NAME, S3_KEY)
    print(f"Файл успешно загружен в S3: s3://{S3_BUCKET_NAME}/{S3_KEY}")

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "retries": 1,
}

with DAG(
    "perekrestok_products_producer",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=["perekrestok", "scraping"],
) as producer_dag:

    fetch_and_save_task = PythonOperator(
        task_id="fetch_and_save_perekrestok_products_to_csv",
        python_callable=fetch_and_save_perekrestok_products_to_csv,
    )

    upload_to_s3_task = PythonOperator(
        task_id="upload_to_s3",
        python_callable=upload_csv_to_s3,
        outlets=[example_dataset],
    )

    fetch_and_save_task >> upload_to_s3_task

with DAG(
    "perekrestok_products_consumer",
    default_args=default_args,
    schedule=[example_dataset],
    catchup=False,
    tags=["perekrestok", "s3", "consume"],
) as consumer_dag:

    def process_s3_data():
        print(f"Данные доступны по адресу: s3://{S3_BUCKET_NAME}/{S3_KEY}")

    process_s3_data_task = PythonOperator(
        task_id="process_s3_data",
        python_callable=process_s3_data,
    )
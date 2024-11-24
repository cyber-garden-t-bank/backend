from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.datasets import Dataset
from airflow.utils.dates import days_ago
from airflow.models import Variable
import asyncio
import csv
from playwright.async_api import async_playwright
import boto3

S3_BUCKET_NAME = "hackgarden2024"
S3_KEY = "datasets/diksi_products.csv"

S3_ENDPOINT = Variable.get("S3_ENDPOINT")
S3_ACCESS_KEY = Variable.get("S3_ACCESS_KEY")
S3_SECRET_KEY = Variable.get("S3_SECRET_KEY")

example_dataset = Dataset(f"s3://{S3_BUCKET_NAME}/{S3_KEY}")

async def diksi_parsing(request_word, base_url="https://dixy.ru"):
    data = []
    url = f"{base_url}/catalog/search.php?q={request_word}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto(url)
            await page.wait_for_selector("article.card.bs-state", timeout=10000)

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

def fetch_and_save_diksi_products_to_csv():
    async def main():
        search_words = [
            "Молоко", "Хлеб", "Яйца", "Сыр", "Масло сливочное", "Йогурт", "Кефир", "Творог", "Сметана",
            # Add more items if needed
        ]
        all_results = []

        for word in search_words:
            try:
                results = await diksi_parsing(word)
                all_results.extend(results)
                print(f"Parsed {len(results)} results for '{word}'")
            except Exception as e:
                print(f"Error parsing '{word}': {e}")
                continue

        with open("diksi_products.csv", mode="w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["search_word", "title", "price", "url"])
            writer.writeheader()
            writer.writerows(all_results)
        print(f"Saved {len(all_results)} results to 'diksi_products.csv'")

    asyncio.run(main())

def upload_csv_to_s3():
    s3_client = boto3.client(
        "s3",
        endpoint_url=S3_ENDPOINT,
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY,
    )
    s3_client.upload_file("diksi_products.csv", S3_BUCKET_NAME, S3_KEY)
    print(f"Файл успешно загружен в S3: s3://{S3_BUCKET_NAME}/{S3_KEY}")

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "retries": 1,
}

with DAG(
    "diksi_products_producer",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=["diksi", "scraping"],
) as producer_dag:

    fetch_and_save_task = PythonOperator(
        task_id="fetch_and_save_diksi_products_to_csv",
        python_callable=fetch_and_save_diksi_products_to_csv,
    )

    upload_to_s3_task = PythonOperator(
        task_id="upload_to_s3",
        python_callable=upload_csv_to_s3,
        outlets=[example_dataset],
    )

    fetch_and_save_task >> upload_to_s3_task

with DAG(
    "diksi_products_consumer",
    default_args=default_args,
    schedule=[example_dataset],
    catchup=False,
    tags=["diksi", "s3", "consume"],
) as consumer_dag:

    def process_s3_data():
        print(f"Данные доступны по адресу: s3://{S3_BUCKET_NAME}/{S3_KEY}")

    process_s3_data_task = PythonOperator(
        task_id="process_s3_data",
        python_callable=process_s3_data,
    )
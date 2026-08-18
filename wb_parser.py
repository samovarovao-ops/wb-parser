import requests
import time
import csv
import os
from datetime import datetime


def search_wildberries(query):
    """Поиск товаров на Wildberries через API."""
    url = "https://search.wb.ru/exactmatch/ru/common/v7/search"
    params = {
        "ab_testing": "false",
        "appType": "1",
        "curr": "rub",
        "dest": "-1257786",
        "query": query,
        "resultset": "catalog",
        "spp": "30",
        "suppressSpellcheck": "false",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept-Language": "ru-RU,ru;q=0.9",
        "Origin": "https://www.wildberries.ru",
        "Referer": "https://www.wildberries.ru/",
    }

    for attempt in range(5):
        try:
            response = requests.get(url, params=params, headers=headers, timeout=15)
            if response.status_code == 429:
                wait = 10 * (attempt + 1)
                time.sleep(wait)
                continue
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            if attempt == 4:
                raise
            time.sleep(5)
    return {"products": []}


def extract_products(data):
    """Извлечение данных о товарах из JSON-ответа."""
    products = []
    for item in data.get("products", []):
        name = item.get("name", "Нет названия")
        brand = item.get("brand", "Нет бренда")
        rating = item.get("reviewRating", 0)
        feedbacks = item.get("feedbacks", 0)

        sizes = item.get("sizes", [])
        if sizes and sizes[0].get("price"):
            price_rub = sizes[0]["price"].get("product", 0) / 100
        else:
            price_rub = 0

        products.append({
            "name": name,
            "brand": brand,
            "price": price_rub,
            "rating": rating,
            "reviews": feedbacks,
        })
    return products


def save_to_csv(products, query):
    """Сохранение товаров в CSV-файл."""
    safe_name = "".join(c if c.isalnum() or c in " _-" else "_" for c in query)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"wb_{safe_name}_{timestamp}.csv"

    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "brand", "price", "rating", "reviews"])
        writer.writeheader()
        writer.writerows(products)

    return os.path.abspath(filename)


def format_products_text(products, limit=20):
    """Форматирование товаров в текст для Telegram (макс. limit штук)."""
    if not products:
        return "Товары не найдены."

    shown = products[:limit]
    lines = []
    for i, p in enumerate(shown, 1):
        lines.append(
            f"{i}. {p['brand']} — {p['name']}\n"
            f"   Цена: {p['price']:.0f} ₽ | Рейтинг: {p['rating']} | Отзывов: {p['reviews']}"
        )

    header = f"Найдено {len(products)} товаров (показаны первые {len(shown)}):\n\n"
    return header + "\n\n".join(lines)

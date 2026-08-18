from wb_parser import search_wildberries, extract_products, save_to_csv


def print_table(products):
    """Вывод товаров в виде таблицы."""
    if not products:
        print("Товары не найдены.")
        return

    print(f"\n{'№':<4} {'Бренд':<15} {'Название':<45} {'Цена':>10} {'Рейтинг':>8} {'Отзывы':>7}")
    print("-" * 95)

    for i, p in enumerate(products, 1):
        name = p["name"][:42] + "..." if len(p["name"]) > 45 else p["name"]
        print(f"{i:<4} {p['brand']:<15} {name:<45} {p['price']:>10.0f} {p['rating']:>8} {p['reviews']:>7}")


def main():
    query = input("Введите поисковый запрос (например, 'смартфон samsung'): ").strip()
    if not query:
        query = "смартфон samsung"

    print(f"\nПоиск: {query}...")
    try:
        data = search_wildberries(query)
        products = extract_products(data)
        print(f"Найдено товаров: {len(products)}")
        print_table(products)

        if products:
            save = input("\nСохранить в CSV-таблицу? (да/нет): ").strip().lower()
            if save in ("да", "y", "yes", "д"):
                filepath = save_to_csv(products, query)
                print(f"\nСохранено: {filepath}")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()

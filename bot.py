import os
import telebot
from wb_parser import search_wildberries, extract_products, save_to_csv, format_products_text

BOT_TOKEN = "8881039420:AAGsJqPAu0jJOGVpvy7WbwCfZ2Vf9zm_9C8"

bot = telebot.TeleBot(BOT_TOKEN)

MAX_LEN = 4000


def send_long(chat_id, text):
    """Разбить длинное сообщение на части."""
    while len(text) > MAX_LEN:
        cut = text.rfind("\n\n", 0, MAX_LEN)
        if cut == -1:
            cut = MAX_LEN
        bot.send_message(chat_id, text[:cut])
        text = text[cut:].lstrip("\n")
    if text:
        bot.send_message(chat_id, text)


@bot.message_handler(commands=["start"])
def cmd_start(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я парсер Wildberries.\n\n"
        "Напишите название товара — я найду его на WB и покажу название, бренд, цену, рейтинг и отзывы.\n\n"
        "Примеры запросов:\n"
        "• ноутбук\n"
        "• кроссовки nike\n"
        "• наушники sony"
    )


@bot.message_handler(func=lambda m: True)
def search(message):
    query = message.text.strip()
    if not query:
        return

    bot.send_message(message.chat.id, "Поиск на Wildberries...")

    try:
        data = search_wildberries(query)
        products = extract_products(data)

        if not products:
            bot.send_message(message.chat.id, "Товары не найдены.")
            return

        text = format_products_text(products)
        send_long(message.chat.id, text)

        # Сохраняем CSV и отправляем файл
        filepath = save_to_csv(products, query)
        with open(filepath, "rb") as f:
            bot.send_document(
                message.chat.id,
                f,
                caption=f"CSV-файл: {len(products)} товаров по запросу «{query}»"
            )
        os.remove(filepath)

    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")


if __name__ == "__main__":
    print("Telegram-бот запущен!")
    bot.infinity_polling()

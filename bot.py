import os
import sys
import time
import logging
import subprocess
import telebot
from wb_parser import search_wildberries, extract_products, save_to_csv, format_products_text


def kill_previous_instances():
    """Убить предыдущие копии этого скрипта."""
    current_pid = os.getpid()
    try:
        result = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq python.exe", "/FO", "CSV"],
            capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
        )
        for line in result.stdout.strip().split("\n")[1:]:
            parts = line.split(",")
            if len(parts) >= 2:
                pid = int(parts[1].strip('"'))
                if pid != current_pid:
                    try:
                        os.kill(pid, 9)
                        log.info(f"Killed old bot instance (PID {pid})")
                    except OSError:
                        pass
    except Exception:
        pass


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8881039420:AAGsJqPAu0jJOGVpvy7WbwCfZ2Vf9zm_9C8")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)

MAX_LEN = 4000


def send_long(chat_id, text):
    """Разбить длинное сообщение на части."""
    while len(text) > MAX_LEN:
        cut = text.rfind("\n\n", 0, MAX_LEN)
        if cut == -1:
            cut = MAX_LEN
        try:
            bot.send_message(chat_id, text[:cut])
        except Exception:
            log.exception("Failed to send message chunk")
        text = text[cut:].lstrip("\n")
    if text:
        try:
            bot.send_message(chat_id, text)
        except Exception:
            log.exception("Failed to send message chunk")


@bot.message_handler(commands=["start"])
def cmd_start(message):
    try:
        bot.send_message(
            message.chat.id,
            "Привет! Я парсер Wildberries.\n\n"
            "Напишите название товара — я найду его на WB и покажу название, бренд, цену, рейтинг и отзывы.\n\n"
            "Примеры запросов:\n"
            "• ноутбук\n"
            "• кроссовки nike\n"
            "• наушники sony"
        )
    except Exception:
        log.exception("Error in /start")


@bot.message_handler(func=lambda m: True)
def search(message):
    query = message.text.strip()
    if not query:
        return

    log.info(f"Search request: {query}")

    try:
        bot.send_message(message.chat.id, "Поиск на Wildberries...")
    except Exception:
        log.exception("Failed to send typing message")
        return

    try:
        data = search_wildberries(query)
        products = extract_products(data)
        log.info(f"Found {len(products)} products for '{query}'")

        if not products:
            bot.send_message(message.chat.id, "Товары не найдены.")
            return

        text = format_products_text(products)
        send_long(message.chat.id, text)

        filepath = save_to_csv(products, query)
        with open(filepath, "rb") as f:
            bot.send_document(
                message.chat.id,
                f,
                caption=f"CSV: {len(products)} товаров — «{query}»"
            )
        try:
            os.remove(filepath)
        except OSError:
            pass

    except Exception as e:
        log.exception("Search error")
        try:
            bot.send_message(message.chat.id, f"Ошибка: {e}")
        except Exception:
            pass


if __name__ == "__main__":
    kill_previous_instances()
    log.info("Telegram-бот запущен!")
    while True:
        try:
            bot.infinity_polling(timeout=30, long_polling_timeout=30)
        except Exception:
            log.exception("Polling crashed, restarting in 5s...")
            time.sleep(5)

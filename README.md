# WB Parser — Парсер Wildberries

Парсер товаров с Wildberries с веб-интерфейсом, Telegram-ботом и экспортом в CSV.

## Возможности

- Поиск товаров по любому запросу на Wildberries
- Отображение: название, бренд, цена, рейтинг, отзывы
- Экспорт результатов в CSV-файл (открывается в Excel)
- Веб-интерфейс с современным дизайном
- Telegram-бот для поиска прямо из мессенджера
- Автономное приложение (.exe) — не требует установки Python

## Технологии

- **Python 3.14** — основной язык
- **Flask** — веб-интерфейс
- **pyTelegramBotAPI** — Telegram-бот
- **Wildberries Search API** — получение данных о товарах
- **PyInstaller** — сборка в .exe

## Запуск

### Веб-интерфейс

```bash
pip install flask requests
python web_app.py
```

Откройте `http://localhost:8080` в браузере.

### Telegram-бот

1. Создайте бота через [@BotFather](https://t.me/BotFather)
2. Вставьте токен в `bot.py`
3. Запустите:

```bash
pip install pyTelegramBotAPI requests
python bot.py
```

### Консольный парсер

```bash
python parser.py
```

### Автономное приложение (.exe)

Готовый `.exe` находится в папке `dist/WBParser.exe`. Запуск двойным кликом — браузер откроется автоматически.

## Структура проекта

```
Parcer/
├── wb_parser.py        # Логика парсинга Wildberries API
├── parser.py           # Консольный парсер
├── web_app.py          # Веб-интерфейс (Flask)
├── bot.py              # Telegram-бот
├── run.py              # Точка входа для .exe
├── templates/
│   └── index.html      # Шаблон веб-страницы
└── dist/
    └── WBParser.exe    # Готовое приложение
```

## Лицензия

MIT

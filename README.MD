# Тестове завдання: Telegram Bot + WhatsApp Webhook + Selenium

## Опис проєкту

Цей проєкт реалізує інтеграцію WhatsApp (тестовий Twilio Sandbox), Telegram-бота та автоматизованого Selenium-скрипта. Основна мета проєкту — демонстрація роботи з месенджерами, обробкою фото-повідомлень та автоматизацією браузерних дій за допомогою Selenium.

## Технології

* **Django + Django REST Framework** (WhatsApp Twilio Sandbox Webhook)
* **Aiogram** (Telegram Bot)
* **Selenium** (Python автоматизація браузера)

## Структура проєкту

```
.
├── README.MD
├── backend/
│   └── (Django REST API логіка для WhatsApp webhook через Twilio)
├── bot/
│   └── (Aiogram Telegram Bot логіка)
|   └── Parser Selenium
├── docker-compose.yml
├── linter.sh
├── pyproject.toml
├── requirements.txt
└── venv_test_horand/
```

## Функціонал

### 1. WhatsApp (Twilio Sandbox)

* **Прийом та збереження фото:**

  * Приймає фото з приватних та групових чатів.
  * Фото зберігаються у структурованому вигляді в каталог `saved_photos/`.
* **Відповідь на фото:**

  * Автоматична відповідь на отримане фото:

    > "Фото збережено, дякуємо!"
* **Обробка текстових повідомлень:**

  * На текстове повідомлення "Привіт" надсилається відповідь:

    > "Вітаємо! Надішліть фото, щоб зберегти його."

### 2. Telegram-бот (Aiogram)

* **Команди:**

  * `/start` — вітальне повідомлення.
  * `/about` — коротка інформація про бот.
  * `/run` — запуск Selenium-скрипта для отримання цитат.

### 3. Selenium-скрипт (Python)

* Запускається командою `/run` у Telegram-боті.
* Виконує наступні дії:

  1. Відкриває сайт [quotes.toscrape.com/login](https://quotes.toscrape.com/login).
  2. Логується з даними:

     * **Логін:** `admin`
     * **Пароль:** `admin`
  3. Після входу переходить на головну сторінку цитат [quotes.toscrape.com](https://quotes.toscrape.com/).
  4. Вибирає 3 випадкові цитати зі сторінки.
  5. Відправляє повідомлення в Telegram:

     > "Успішно залогінено. Ось ваші цитати: …"

## Інструкція для запуску

1. **Запуск WhatsApp webhook (Twilio Sandbox):**

```

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
docker-compose up --build
cd backend/
python manage.py runserver
cd ../
python -m bot.main
```

2. **Запуск Telegram-бота:**

```
cd bot
pip install -r requirements.txt
python bot.py
```




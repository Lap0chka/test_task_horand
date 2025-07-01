import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT")

TOSCRAPE_LOGIN_PAGE = "https://quotes.toscrape.com/login"
TOSCRAPE_QUOTES_PAGE = "https://quotes.toscrape.com/"
TOSCRAPE_USERNAME = "admin"
TOSCRAPE_PASSWORD = "admin"

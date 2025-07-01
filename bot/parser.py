import logging
import random
import time
from typing import List

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.webdriver import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver, WebElement

from bot import settings

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ParserBase:
    def __init__(self) -> None:
        """Initialize WebDriver with Chrome options."""
        options = self.get_options()
        self.driver: WebDriver = webdriver.Chrome(options=options)
        logger.info("WebDriver initialized.")

    @staticmethod
    def get_options() -> Options:
        """
        Return configured ChromeOptions for headless browser.
        """
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        return options

    def get_page(self, url: str) -> None:
        """
        Open a web page by URL.
        """
        self.driver.get(url)

    def find_element(self, find_by: By, find_value: str) -> WebElement:
        try:
            return self.driver.find_element(find_by, find_value)
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Failed to fill field {find_value}: {e}")
            raise

    def fill_field(
        self, find_by: By, find_value: str, fill_value: str, is_send_keys: bool = False
    ) -> None:
        """
        Fill a form field with a given value.

        :param find_by: Selenium locator strategy
        :param find_value: Value to locate the element
        :param fill_value: Value to enter in the field
        :param is_send_keys: Whether to send RETURN key
        """
        try:
            find_element = self.find_element(find_by, find_value)
            find_element.send_keys(fill_value)
            if is_send_keys:
                find_element.send_keys(Keys.RETURN)
            time.sleep(1)
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Failed to fill field {find_value}: {e}")
            raise


class Parser(ParserBase):
    def get_login(self) -> None:
        """
        Log in using predefined credentials.
        """
        self.get_page(settings.TOSCRAPE_LOGIN_PAGE)
        self.fill_field(By.NAME, "username", settings.TOSCRAPE_USERNAME)
        self.fill_field(By.NAME, "password", settings.TOSCRAPE_PASSWORD, is_send_keys=True)
        logger.info("Logged in successfully.")

    def get_quotes(self) -> List[str]:
        """
        Extract quotes from the quotes page.
        """
        quotes = []
        self.get_page(settings.TOSCRAPE_QUOTES_PAGE)
        quotes_elements = self.driver.find_elements(By.CLASS_NAME, "quote")
        for q in quotes_elements:
            text = q.find_element(By.CLASS_NAME, "text").text
            author = q.find_element(By.CLASS_NAME, "author").text
            quotes.append(f"{text} — {author}")
        return quotes

    @staticmethod
    def get_random_quote(quotes: List[str]) -> List[str]:
        """
        Select 3 random quotes if possible, otherwise return all.
        """
        if len(quotes) >= 3:
            result = random.sample(quotes, 3)
        else:
            result = quotes
        logger.info(f"Selected {len(result)} random quotes.")
        return result

    def start_parser(self) -> List[str]:
        """
        Start the parsing process.
        """
        self.get_login()
        quotes = self.get_quotes()
        return self.get_random_quote(quotes)


pars = Parser()

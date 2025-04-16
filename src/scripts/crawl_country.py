import random
import requests
from typing import List
from loguru import logger
from src.models.book_model import Book

class CountryScraper:
    def __init__(self):
        self.countries = []

    def fetch_countries(self):
        try:
            logger.info("🌍 Fetching countries from API...")
            r = requests.get("https://restcountries.com/v3.1/all", timeout=10)
            r.raise_for_status()  # raise HTTPError if status != 200
            self.countries = [c["name"]["common"] for c in r.json()]
            logger.success(f"✅ Fetched {len(self.countries)} countries.")
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to fetch countries: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Unexpected error while fetching countries: {e}")
            raise

    def assign_random_country(self, books: List[Book]) -> List[Book]:
        try:
            if not self.countries:
                self.fetch_countries()

            logger.info(f"🎲 Assigning random country to {len(books)} books.")
            for book in books:
                book.publisher_country = random.choice(self.countries)
                logger.debug(f"➡️ {book.title} -> {book.publisher_country}")
            logger.success("🎉 Country assignment complete.")
            return books
        except Exception as e:
            logger.error(f"❌ Error assigning countries: {e}")
            raise

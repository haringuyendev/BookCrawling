from src.config.config import BOOKS_FILE, BOOKS_WITH_COUNTRY_FILE
from src.scripts.crawl_books import BookScraper
from src.scripts.crawl_country import CountryScraper
from src.models.book_model import serialize_books
import json
import os
from loguru import logger



# Kiểm tra và tạo file nếu chưa có
if not os.path.exists(BOOKS_FILE):
    os.makedirs(os.path.dirname(BOOKS_FILE), exist_ok=True)
    with open(BOOKS_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=4)  

if not os.path.exists(BOOKS_WITH_COUNTRY_FILE):
    os.makedirs(os.path.dirname(BOOKS_WITH_COUNTRY_FILE), exist_ok=True)
    with open(BOOKS_WITH_COUNTRY_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=4)  

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    logger.info("Crawling book data...")
    book_scrape = BookScraper(category="fiction_10", pages=3)
    country_scrape=CountryScraper()

    book_scrape.scrape()
    books = book_scrape.books

    logger.info("Saving to file...")
    with open(BOOKS_FILE, "w", encoding="utf-8") as f:
        json.dump(serialize_books(books), f, ensure_ascii=False, indent=4)

    logger.info(f"Collected {len(books)} books.")

    logger.info("Assigning random countries...")
    books_with_country = country_scrape.assign_random_country(books)

    logger.info("Saving to file...")
    with open(BOOKS_WITH_COUNTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(serialize_books(books_with_country), f, ensure_ascii=False, indent=4)


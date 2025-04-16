from loguru import logger
import requests
import os
from bs4 import BeautifulSoup
from src.models.book_model import Book

# Thiết lập lưu log ra file (nếu muốn)
logger.add("logs/scraper.log", rotation="1 MB", retention="7 days", level="INFO")

class BookScraper:
    def __init__(self, category: str, pages: int):
        self.category = category
        self.pages = pages
        self.base_url = f"https://books.toscrape.com/catalogue/category/books/{category}"
        self.books = []
        self.html_dir = "html_backup"
        os.makedirs(self.html_dir, exist_ok=True)

    def get_category_id(self):
        category_map = {
            "science": "22",
            "travel": "2",
            "poetry": "19",
        }
        return category_map.get(self.category.lower(), "1")

    def get_star_rating(self, rating_class: str) -> int:
        rating_map = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5
        }
        return rating_map.get(rating_class, 0)

    def scrape(self):
        for page in range(1, self.pages + 1):
            url = f"{self.base_url}/page-{page}.html"
            logger.info(f"Crawling page {page}: {url}")
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
            except Exception as e:
                logger.error(f"Failed to fetch page {page}: {e}")
                continue

            items = soup.select("article.product_pod")
            logger.info(f"Found {len(items)} books on page {page}")

            for item in items:
                try:
                    title = item.h3.a["title"]
                    price = item.select_one(".price_color").text
                    availability = item.select_one(".availability").text.strip()
                    rating_class = item.select_one("p.star-rating")["class"][1]
                    link = item.h3.a["href"].replace('../../../', '')
                    product_url = f"https://books.toscrape.com/catalogue/{link}"

                    # Fetch product page HTML
                    try:
                        html = requests.get(product_url, timeout=10).text
                        filename = title.replace("/", "-").replace("\\", "-") + ".html"
                        path = os.path.join(self.html_dir, filename)
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(html)
                    except Exception as e:
                        logger.warning(f"Could not save HTML for {title}: {e}")

                    book = Book(
                        title=title,
                        price=price,
                        availability=availability,
                        product_url=product_url,
                        star_rating=self.get_star_rating(rating_class),
                    )
                    self.books.append(book)
                    logger.success(f"✅ Added book: {title}")

                except Exception as e:
                    logger.error(f"❌ Error processing a book on page {page}: {e}")

        logger.success(f"🎉 Scraping finished. Total books collected: {len(self.books)}")
        return self.books

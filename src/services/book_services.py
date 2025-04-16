import json
from typing import List
from models.book_model import Book
from loguru import logger

from dtos.BookDTO import BookCreateDTO

BOOK_FILE = "../data/books_with_country.json"

class BookService:
    def __init__(self):
        self.books = self.load_books()

    def load_books(self) -> List[Book]:
        try:
            with open(BOOK_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                logger.success(f"📖 Loaded {len(data)} books from {BOOK_FILE}")
                return [Book(**b) for b in data]
        except FileNotFoundError:
            logger.warning(f"⚠️ Book file not found at {BOOK_FILE}. Starting with empty list.")
            return []
        except Exception as e:
            logger.error(f"❌ Error loading books: {e}")
            return []

    def get_all_books(self) -> List[Book]:
        logger.info("📚 Fetching all books")
        return [book for book in self.books if not book.is_deleted]

    def get_books_by_country(self, country: str) -> List[Book]:
        logger.info(f"🌍 Filtering books by country: {country}")
        return [
            book for book in self.books
            if not book.is_deleted and book.publisher_country.lower() == country.lower()
        ]

    def add_book(self, book_dto: BookCreateDTO):
        try:
            book = Book(
                title=book_dto.title,
                price=book_dto.price,
                availability=book_dto.availability,
                product_url=book_dto.product_url,
                star_rating=book_dto.star_rating,
                publisher_country=book_dto.publisher_country,
            )
            
            self.books.append(book)
            self.save_books()
            logger.success(f"✅ Book '{book.title}' added")
        except Exception as e:
            logger.error(f"❌ Error adding book '{book_dto.title}': {e}")
            raise

    def delete_book_by_title(self, title: str):
        try:
            found = False
            for book in self.books:
                if title in book.title and not book.is_deleted:
                    book.is_deleted = 1
                    found = True
                    break

            if found:
                self.save_books()
                logger.success(f"🗑️ Book '{title}' marked as deleted (soft delete)")
            else:
                logger.warning(f"⚠️ Book '{title}' not found or already deleted")
        except Exception as e:
            logger.error(f"❌ Error deleting book '{title}': {e}")
            raise


    def save_books(self):
        try:
            with open(BOOK_FILE, "w", encoding="utf-8") as f:
                json.dump([b.dict() for b in self.books], f, ensure_ascii=False, indent=4)
                logger.info(f"💾 Books saved to {BOOK_FILE}")
        except Exception as e:
            logger.error(f"❌ Error saving books: {e}")
            raise

from dotenv import load_dotenv
import os

# Load biến từ .env
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
BOOKS_FILE = os.getenv("BOOKS_FILE")
BOOKS_WITH_COUNTRY_FILE = os.getenv("BOOKS_WITH_COUNTRY_FILE")
USERS_FILE = os.getenv("USERS_FILE")
BOOK_SCRAPE_URL=os.getenv("BOOK_SCRAPE_URL")
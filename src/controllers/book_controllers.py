from typing import List
from fastapi import APIRouter, Depends, HTTPException
from services.book_services import BookService
from loguru import logger

from dtos.BookDTO import BookCreateDTO, BookResponseDTO
from models.base_response import BaseResponse
from controllers.auth_controller import get_current_user

router = APIRouter()
book_service = BookService()

@router.get("/books")
def get_books(country: str = None, current_user: dict = Depends(get_current_user)):
    try:
        if country:
            logger.info(f"📦 Getting books from country: {country}")
            books = book_service.get_books_by_country(country)
        else:
            logger.info("📚 Getting all books")
            books = book_service.get_all_books()
        book_dtos = [BookResponseDTO(**book.__dict__) for book in books]

        return BaseResponse[List[BookResponseDTO]](data=book_dtos)

    except Exception as e:
        logger.error(f"❌ Error fetching books: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
@router.post("/books")
def create_book(book: BookCreateDTO, current_user: dict = Depends(get_current_user)):
    try:
        logger.info(f"➕ Adding new book: {book.title}")
        book_service.add_book(book)
        logger.success(f"✅ Book '{book.title}' added successfully")
        return BaseResponse[str](data=f"✅ Book '{book.title}' added successfully")
    except Exception as e:
        logger.error(f"❌ Error adding book: {e}")
        raise HTTPException(status_code=500, detail="Failed to add book")

@router.delete("/books/{title}")
def delete_book(title: str, current_user: dict = Depends(get_current_user)):
    try:
        logger.info(f"🗑️ Deleting book: {title}")
        book_service.delete_book_by_title(title)
        logger.success(f"✅ Book '{title}' deleted successfully")
        return BaseResponse[str](data=f"✅ Book '{title}' deleted successfully")

    except Exception as e:
        logger.error(f"❌ Error deleting book '{title}': {e}")
        raise HTTPException(status_code=500, detail="Failed to delete book")

from fastapi import FastAPI
from controllers.book_controllers import router as book_router
from controllers.auth_controller import router as auth_router

from config.logger_config import logger 

logger.add("logs/app.log", rotation="1 MB", retention="7 days", compression="zip")

app = FastAPI()
app.include_router(auth_router)
app.include_router(book_router)


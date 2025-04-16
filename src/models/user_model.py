from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class User(BaseModel):
    username: str
    password: str 

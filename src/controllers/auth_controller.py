from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from pydantic import BaseModel
from auth import AuthService
from models.base_response import BaseResponse

router = APIRouter( tags=["Auth"])
auth_service = AuthService()
auth_scheme = HTTPBearer()

class User(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: User):
    if auth_service.get_user(user.username):
        return BaseResponse[None](status=400,message="Username already registered", data=None)
    auth_service.create_user(user.username, user.password)
    return BaseResponse[str](data="User created successfully")

@router.post("/login", response_model=Token)
def login_for_access_token(user: User):
    stored_user = auth_service.get_user(user.username)
    if not stored_user or not auth_service.verify_password(user.password, stored_user["hashed_password"]):
        return BaseResponse[None](status=401,message="Invalid credentials", data=None)
    access_token = auth_service.create_access_token(data={"sub": user.username})
    return {
            "access_token": access_token,
            "token_type": "bearer"
        }

def get_current_user(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
        try:
            payload = auth_service.verify_access_token(token.credentials)
            if payload is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            return payload
        except Exception as e:
            raise HTTPException(status_code=401, detail="Invalid token")
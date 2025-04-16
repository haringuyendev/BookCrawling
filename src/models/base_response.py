from typing import Generic, TypeVar, Optional
from pydantic.generics import GenericModel

T = TypeVar("T")

class BaseResponse(GenericModel, Generic[T]):
    status: int = 200
    message: Optional[str] = "success"
    data: Optional[T] = None


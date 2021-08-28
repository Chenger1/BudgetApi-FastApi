from tortoise.contrib.pydantic import pydantic_model_creator

from .models import User, Category, Transaction, Message

from pydantic import BaseModel

from typing import Optional, List

from datetime import date


User_Schema = pydantic_model_creator(User)
Transaction_Schema = pydantic_model_creator(Transaction)
Category_Schema = pydantic_model_creator(Category)
Message_Schema = pydantic_model_creator(Message)


class UserIn(BaseModel):
    username: str
    password: str


class EditUser(BaseModel):
    username: Optional[str] = None
    fixed_balance: Optional[float] = None
    use_fixed_balance: Optional[bool] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class CreateCategory(BaseModel):
    name: str


class EditCategory(BaseModel):
    name: str


class CategoryList(BaseModel):
    user_id: int  #: user id
    username: str
    categories: List[Category_Schema]

    class Config:
        arbitrary_types_allowed = True


class CreateTransaction(BaseModel):
    sum: float
    category: int
    type: bool
    planned: Optional[date] = None

    class Config:
        orm_mode = True


class EditTransaction(BaseModel):
    sum: Optional[float] = None
    user: Optional[int] = None
    category: Optional[int] = None

    class Config:
        orm_mode = True


class TransactionList(BaseModel):
    user_id: int  #: user id
    username: str
    transactions: List[Transaction_Schema]

    class Config:
        arbitrary_types_allowed = True


class MessageList(BaseModel):
    user_id: int
    username: str
    messages: List[Message_Schema]

    class Config:
        arbitrary_types_allowed = True

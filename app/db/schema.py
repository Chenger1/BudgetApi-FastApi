from typing import Optional, List

from pydantic import BaseModel

from datetime import date


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    username: str

    class Config:
        orm_mode = True


class BaseCategory(BaseModel):
    name: str

    class Config:
        orm_mode = True


class Category(BaseCategory):
    user_id: int
    id: Optional[int] = None


class EditCategory(BaseCategory):
    pass


class CategoryList(User):
    categories: List[Category]

    class Config:
        arbitrary_types_allowed = True


class BaseTransaction(BaseModel):
    sum: int
    user_id: int
    category_id: int

    class Config:
        orm_mode = True


class CreateTransaction(BaseTransaction):
    number: Optional[int] = None
    created: Optional[str] = None


class Transaction(BaseTransaction):
    id: int
    number: int
    created: date
    category_name: Optional[str] = None


class TransactionList(User):
    transactions: List[Transaction]

    class Config:
        arbitrary_types_allowed = True


class EditTransaction(BaseModel):
    sum: Optional[int] = None
    category_id: Optional[int] = None

from typing import Optional, List

from pydantic import BaseModel


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


class EditCategory(BaseCategory):
    pass


class CategoryList(User):
    categories: List[Category]

    class Config:
        arbitrary_types_allowed = True

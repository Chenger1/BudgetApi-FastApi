from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)

    categories = relationship('Category', back_populates='user')
    transactions = relationship('Transaction', back_populates='user')


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='categories')
    transactions = relationship('Transaction', back_populates='category', uselist=True)


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer)
    sum = Column(Float)

    created = Column(Date)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='transactions')

    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='transactions')

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from python.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))  # Связь с пользователем
    user = relationship("User", back_populates="orders")  # Связываем с пользователем

User.orders = relationship("Order", back_populates="user")
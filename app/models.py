from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    account_status = Column(
        String(20),
        nullable=False,
        default="ACTIVE"
    )

    orders = relationship("Order", back_populates="user")


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(String(20), primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    symbol = Column(String(20), nullable=False)
    quantity = Column(Integer, nullable=False)
    side = Column(String(10), nullable=False)
    order_type = Column(String(20), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    status = Column(
        String(20),
        nullable=False,
        default="PENDING"
    )

    user = relationship("User", back_populates="orders")
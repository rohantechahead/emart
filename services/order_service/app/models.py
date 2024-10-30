from sqlalchemy import Column, Integer, TIMESTAMP, Float, String
from sqlalchemy.orm import declarative_base

OrderServiceBase = declarative_base()

class Cart(OrderServiceBase):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP', onupdate='CURRENT_TIMESTAMP')


class OrderItem(OrderServiceBase):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)


class Order(OrderServiceBase):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    total_amount = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    status = Column(String(50), default="pending")



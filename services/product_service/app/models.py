from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from common.database import Base

class ProductCategory(Base):
    __tablename__ = 'product_categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    status = Column(Boolean, default=True)

class ProductImages(Base):
    __tablename__ = 'product_Images'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    image_url = Column(String(255), nullable=False)


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    price = Column(Integer, nullable=False)
    stock_quantity = Column(Integer, index=True)
    category_id = Column(Integer, ForeignKey('product_categories.id'), nullable=False)
    status = Column(Boolean, default=True)







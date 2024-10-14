from sqlalchemy import Column, Integer, String, Boolean
from common.database import Base

class ProductCategory(Base):
    __tablename__ = 'product_categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    status = Column(Boolean, default=True)

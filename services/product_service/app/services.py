from sqlalchemy.orm import Session
from services.product_service.app.models import ProductCategory
from services.product_service.app.schemas import ProductCategoryCreate, ProductCategoryUpdate


def create_category(db: Session, category: ProductCategoryCreate):
    db_category = ProductCategory(name=category.name, status=True)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, category_update: ProductCategoryUpdate):
    db_category = db.query(ProductCategory).filter(ProductCategory.id == category_id).first()
    if db_category:
        db_category.name = category_update.name
        db_category.status = category_update.status
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = db.query(ProductCategory).filter(ProductCategory.id == category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category


def search_category_by_name(db: Session, search_query: str = None):
    if search_query:
        return db.query(ProductCategory).filter(ProductCategory.name.ilike(f'%{search_query}%')).all()
    return db.query(ProductCategory).all()


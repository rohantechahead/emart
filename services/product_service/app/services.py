from app import schemas
from app.models import ProductCategory, Product, ProductImages
from sqlalchemy.orm import Session
from .schemas import ProductCategoryCreate, ProductCategoryUpdate, ProductCreate


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


def create_product(db: Session, product: ProductCreate):
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock_quantity=product.stock_quantity,
        category_id=product.category_id,
        status=product.status
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    save_product_images(db_product, product.image_urls, db)
    return db_product


def save_product_images(product, image_urls, db):
    for image_url in image_urls:
        db_image = ProductImages(product_id=product.id, image_url=image_url)
        db.add(db_image)
    db.commit()


def update_product_by_id(db: Session, product_id: int, product_update: schemas.ProductUpdate):
    db_product = db.query(Product).filter(Product.id == product_id).first()

    if not db_product:
        return None

    db_product.name = product_update.name
    db_product.description = product_update.description
    db_product.price = product_update.price
    db_product.stock_quantity = product_update.stock_quantity
    db_product.category_id = product_update.category_id
    db_product.status = product_update.status
    db.commit()
    db.refresh(db_product)

    return db_product


def delete_product(db: Session, product_id: int):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        db.query(ProductImages).filter(ProductImages.product_id == product_id).delete()
        db.delete(db_product)
        db.commit()

    return db_product


def get_products(db: Session, product_id: int = None):
    if product_id is not None:
        return db.query(Product).filter(Product.id == product_id).first()
    return db.query(Product).all()

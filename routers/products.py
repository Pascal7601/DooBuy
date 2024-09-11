from core.connection import get_db
from fastapi import Depends, APIRouter, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from models.products import Product
from schemas import productSchema
from sqlalchemy import select


products_router = APIRouter(prefix='/api/v1/products', tags=['products'])

@products_router.get('/', response_model=List[productSchema.ProductResponseModel])
def all_products(db: Session = Depends(get_db)):
    """
    get all products
    """
    products = db.query(Product).all()
    return products


@products_router.get('/{name}', response_model=productSchema.ProductResponseModel)
async def products(name: str, db: Session = Depends(get_db)):
    """
    get user by their id
    """
    product = db.query(Product).filter(Product.name == name).first()
    if not product:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'product not found')
    return product


@products_router.post('/', status_code=status.HTTP_201_CREATED)
async def add_product(product: productSchema.ProductPostModel, db: Session = Depends(get_db)):
    """
    add a user
    """
    new_product = Product(
        name=product.name,
        price=product.price,
        description=product.description)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {'message': f'succesfully registered product_id {new_product.id} to our system'}


@products_router.put('/{name}', response_model=productSchema.ProductResponseModel)
async def update_product(name: str, updated_data: productSchema.ProductPostModel,
                      db: Session = Depends(get_db)):
    """
    update a user
    """
    product = db.query(Product).filter(Product.name == name).first()
    if not product:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'product not found')
        
    if product.name:
        product.name = updated_data.name
    if product.price:
        product.price = updated_data.price
    if product.description:
        product.description = updated_data.description
    db.commit()
    db.refresh(product)

    return product


@products_router.delete('/{name}')
async def delete_product(name: str, db: Session = Depends(get_db)):
    """
    get user by their id
    """
    product = db.query(Product).filter(Product.name == name).first()
    if not product:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'user not found')
    db.delete(product)
    db.commit()
    return {'message': 'product succesfully deleted'}

@products_router.get('/search/', response_model=List[productSchema.ProductResponseModel])
async def search_product(query: str, db: Session = Depends(get_db)):
    """
    search for a specific product
    """
    product = select(Product).where(Product.name.ilike(f'%{query}%'))
    result = db.execute(product).scalars().all()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='product not found'
            )
    return result

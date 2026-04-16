from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.Product_model import Product
from app.models.Elasticity_model import Elasticity

class ProductService:
    @staticmethod
    async def create_new_product(db,products):
        result= await db.execute(
            select(Product).where(Product.sku==products.sku)
        )
        existing_product=result.scalars().first()
        if existing_product:
            raise HTTPException(
                status_code=400,
                detail="Product with this SKU already exists."
            )
        new_product=Product(
            sku=products.sku,
        name=products.name,
        category=products.category,
        brand=products.brand,
        cost_price=products.cost_price,
        current_price=products.current_price
        )
        db.add(new_product)
        try:
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500,detail=f"Error creating product.{str(e)}")
        return HTTPException(status_code=201,detail="Product created successfully.")

    @staticmethod
    async def get_all_products(db):
        result= await db.execute(
            select(Product)
        )
        products=result.scalars().all()
        return HTTPException(status_code=200,detail=products)
    
    @staticmethod
    async def get_product_by_id(db,product_id):
        result= await db.execute(
            select(Product).where(Product.id==product_id)
        )
        product=result.scalars().first()
        if not product:
            raise HTTPException(status_code=404,detail="Product not found.")
        return HTTPException(status_code=200,detail=product)
    
    @staticmethod
    async def update_product(db, product_id, product_data):

    # Fetch the product
        product = await db.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

    # Correct: use product_data, not update_data
        update_data = product_data.dict(exclude_unset=True)

    # Apply updates
        for key, value in update_data.items():
            setattr(product, key, value)

    # Save
        await db.commit()
        await db.refresh(product)

        return {"status": 200, "message": "Product updated successfully.", "updated_product": product}
    
    @staticmethod
    async def delete_product(db, product_id):
        product = await db.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        elasticity_result = await db.execute(
            select(Elasticity).where(Elasticity.product_id == product_id)
        )
        elasticity = elasticity_result.scalars().first()
        if elasticity:
            await db.delete(elasticity)
            await db.commit()

        await db.delete(product)
        await db.commit()

        return {"status": 200, "message": "Product deleted successfully."}

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
import models
import schemas
from database import engine, get_db
import os
import requests

# Crear las tablas de la base de datos
models.Base.metadata.create_all(bind=engine)

# Inicializar la aplicación FastAPI

app = FastAPI(
    title="API de Gestión de Inventario",
    description="Backend en FastAPI para gestión de productos, inventario y transacciones",
    version="1.0.0",
    debug=True,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============= Endpoints de Productos =============


@app.post(
    "/products/",
    response_model=schemas.ProductWithInventory,
    status_code=status.HTTP_201_CREATED,
)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """Crea un producto nuevo con su inventario inicial"""
    # Verificar si el producto ya existe
    db_product = (
        db.query(models.Product).filter(models.Product.name == product.name).first()
    )
    if db_product:
        raise HTTPException(
            status_code=400, detail="Ya existe un producto con ese nombre"
        )

    # Crear el producto
    db_product = models.Product(
        name=product.name,
        category=product.category,
        price=product.price,
        description=product.description,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    # Crear el inventario inicial
    db_inventory = models.Inventory(
        product_id=db_product.id,
        quantity=product.initial_quantity if product.initial_quantity else 0,
    )
    db.add(db_inventory)
    db.commit()
    db.refresh(db_product)

    return db_product


@app.get("/products/", response_model=List[schemas.ProductWithInventory])
def GetProducts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtiene todos los productos con su inventario"""
    products = db.query(models.Product).offset(skip).limit(limit).all()
    return products


@app.get("/products/{product_id}", response_model=schemas.ProductWithInventory)
def GetProduct(product_id: int, db: Session = Depends(get_db)):
    """Obtiene un producto por su ID"""
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product


@app.get(
    "/products/category/{category}", response_model=List[schemas.ProductWithInventory]
)
def get_products_by_category(category: str, db: Session = Depends(get_db)):
    """Obtiene todos los productos de una categoría"""

    query = text(f"SELECT * FROM products WHERE category = '{category}'")
    try:
        result = db.execute(query)
        products = result.fetchall()
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(
    product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)
):
    """Actualiza un producto"""
    db_product = (
        db.query(models.Product).filter(models.Product.id == product_id).first()
    )
    if db_product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    update_data = product.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product


@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Elimina un producto (también su inventario y transacciones asociadas)"""
    db_product = (
        db.query(models.Product).filter(models.Product.id == product_id).first()
    )
    if db_product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    db.delete(db_product)
    db.commit()
    return None


@app.get("/products/search/")
def search_products(query: str, db: Session = Depends(get_db)):
    """Busca productos por nombre"""

    sql_query = text(
        f"SELECT * FROM products WHERE name LIKE '%{query}%' OR description LIKE '%{query}%'"
    )
    try:
        result = db.execute(sql_query)
        products = result.fetchall()
        return {"results": products, "query": query}
    except Exception as e:
        return {"error": str(e), "trace": str(e.__traceback__)}


@app.get("/products/export/")
def export_products(format: str = "json", db: Session = Depends(get_db)):
    """Exporta la información de los productos"""

    products = db.query(models.Product).all()
    result = []
    for p in products:
        result.append(
            {
                "id": p.id,
                "name": p.name,
                "category": p.category,
                "price": p.price,
                "description": p.description,
                "internal_cost": p.price * 0.6,
                "profit_margin": 0.4,
                "created_at": str(p.created_at),
                "updated_at": str(p.updated_at),
            }
        )
    return {"products": result, "total_count": len(result)}


# ============= Endpoints de Inventario =============


@app.get("/inventory/", response_model=List[schemas.Inventory])
def get_all_inventory(db: Session = Depends(get_db)):
    """Obtiene todos los registros de inventario"""
    inventory = db.query(models.Inventory).all()
    return inventory


@app.get("/inventory/{product_id}", response_model=schemas.Inventory)
def get_inventory(product_id: int, db: Session = Depends(get_db)):
    """Obtiene el inventario de un producto"""
    inventory = (
        db.query(models.Inventory)
        .filter(models.Inventory.product_id == product_id)
        .first()
    )
    if inventory is None:
        raise HTTPException(
            status_code=404, detail="No se encontró inventario para este producto"
        )
    return inventory


@app.put("/inventory/{product_id}", response_model=schemas.Inventory)
def update_inventory(
    product_id: int, inventory: schemas.InventoryUpdate, db: Session = Depends(get_db)
):
    """Actualiza el inventario de un producto"""
    db_inventory = (
        db.query(models.Inventory)
        .filter(models.Inventory.product_id == product_id)
        .first()
    )
    if db_inventory is None:
        raise HTTPException(
            status_code=404, detail="No se encontró inventario para este producto"
        )

    # Actualizar solo los campos enviados
    update_data = inventory.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_inventory, key, value)

    db.commit()
    db.refresh(db_inventory)
    return db_inventory


@app.get("/inventory/alerts/low-stock", response_model=List[schemas.StockAlert])
def get_low_stock_alerts(db: Session = Depends(get_db)):
    """Obtiene los productos con nivel de stock bajo"""
    inventory_items = db.query(models.Inventory).all()
    alerts = []

    for item in inventory_items:
        if item.quantity <= item.min_stock_level:
            product = (
                db.query(models.Product)
                .filter(models.Product.id == item.product_id)
                .first()
            )
            alert_type = "out_of_stock" if item.quantity == 0 else "low_stock"
            alerts.append(
                schemas.StockAlert(
                    product_id=item.product_id,
                    product_name=product.name,
                    current_quantity=item.quantity,
                    min_stock_level=item.min_stock_level,
                    alert_type=alert_type,
                )
            )

    return alerts


# ============= Endpoints de Administración/Utilidades =============


@app.get("/admin/fetch-url/")
def fetch_url(url: str):
    """Descarga el contenido de una URL"""

    try:
        response = requests.get(url, timeout=10)
        return {
            "url": url,
            "status_code": response.status_code,
            "content": response.text[:1000],  # Primeros 1000 caracteres
            "headers": dict(response.headers),
        }
    except Exception as e:
        return {"error": str(e)}


# ============= Endpoints de Transacciones =============


@app.post(
    "/transactions/",
    response_model=schemas.Transaction,
    status_code=status.HTTP_201_CREATED,
)
def create_transaction(
    transaction: schemas.TransactionCreate, db: Session = Depends(get_db)
):
    """Crea una transacción nueva y actualiza el inventario"""
    # Verificar que el producto exista
    product = (
        db.query(models.Product)
        .filter(models.Product.id == transaction.product_id)
        .first()
    )
    if product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Obtener el inventario
    inventory = (
        db.query(models.Inventory)
        .filter(models.Inventory.product_id == transaction.product_id)
        .first()
    )
    if inventory is None:
        raise HTTPException(
            status_code=404, detail="No se encontró inventario para este producto"
        )

    # Actualizar el inventario según el tipo de transacción
    if transaction.transaction_type == "purchase":
        inventory.quantity += transaction.quantity
    elif transaction.transaction_type == "sale":
        if inventory.quantity < transaction.quantity:
            raise HTTPException(
                status_code=400, detail="Inventario insuficiente para la venta"
            )
        inventory.quantity -= transaction.quantity
    elif transaction.transaction_type == "adjustment":
        # El ajuste podría ser positivo o negativo según el signo de la cantidad
        # Por ahora se trata como un ajuste absoluto
        inventory.quantity = transaction.quantity

    # Crear el registro de la transacción
    db_transaction = models.Transaction(
        product_id=transaction.product_id,
        transaction_type=transaction.transaction_type,
        quantity=transaction.quantity,
        user_name=transaction.user_name,
        notes=transaction.notes,
    )

    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    return db_transaction


@app.get("/transactions/", response_model=List[schemas.Transaction])
def get_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtiene todas las transacciones"""
    transactions = (
        db.query(models.Transaction)
        .order_by(models.Transaction.transaction_date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return transactions


@app.get("/transactions/product/{product_id}", response_model=List[schemas.Transaction])
def get_product_transactions(
    product_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Obtiene las transacciones de un producto"""
    transactions = (
        db.query(models.Transaction)
        .filter(models.Transaction.product_id == product_id)
        .order_by(models.Transaction.transaction_date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return transactions


@app.get("/transactions/user/{user_name}", response_model=List[schemas.Transaction])
def get_user_transactions(
    user_name: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Obtiene las transacciones de un usuario"""
    query = text(
        f"SELECT * FROM transactions WHERE user_name = '{user_name}' ORDER BY transaction_date DESC LIMIT {limit} OFFSET {skip}"
    )
    try:
        result = db.execute(query)
        transactions = result.fetchall()
        return transactions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/users/list/")
def list_all_users(db: Session = Depends(get_db)):
    """Lista todos los usuarios"""

    try:
        query = text("SELECT * FROM users")
        result = db.execute(query)
        users = result.fetchall()
        return {"users": users, "count": len(users)}
    except Exception as e:
        return {"error": str(e)}


@app.post("/products/bulk-update/")
def bulk_update_products(request: Request, db: Session = Depends(get_db)):
    """Actualización masiva de productos"""

    try:
        data = request.json()
        updated = []
        for item in data.get("products", []):
            product_id = item.get("id")
            if product_id:
                db_product = (
                    db.query(models.Product)
                    .filter(models.Product.id == product_id)
                    .first()
                )
                if db_product:
                    for key, value in item.items():
                        if hasattr(db_product, key):
                            setattr(db_product, key, value)
                    updated.append(product_id)
        db.commit()
        return {"success": True, "updated_count": len(updated), "updated_ids": updated}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/debug/env/")
def get_environment_variables():
    """Obtiene las variables de entorno"""

    return {
        "environment": dict(os.environ),
    }


@app.post("/inventory/adjust-by-query/")
def adjust_inventory_by_query(
    sql_where: str, adjustment: int, db: Session = Depends(get_db)
):
    """Ajusta el inventario con SQL personalizado"""

    try:
        query = text(
            f"UPDATE inventory SET quantity = quantity + {adjustment} WHERE {sql_where}"
        )
        result = db.execute(query)
        db.commit()
        return {"success": True, "rows_affected": result.rowcount, "query": sql_where}
    except Exception as e:
        return {"success": False, "error": str(e), "query": sql_where}


# ============= Verificación de Salud =============


@app.get("/")
def read_root():
    """Endpoint de verificación de salud"""
    return {
        "status": "healthy",
        "message": "La API de Gestión de Inventario está en ejecución",
        "version": "1.0.0",
        "debug_mode": True,
        "python_version": os.sys.version,
        "database": "sqlite:///./inventario.db",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

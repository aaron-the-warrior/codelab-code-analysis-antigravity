from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    category = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.datetime.now(datetime.timezone.utc),
        onupdate=datetime.datetime.now(datetime.timezone.utc),
    )

    # Relaciones
    inventory = relationship(
        "Inventory",
        back_populates="product",
        uselist=False,
        cascade="all, delete-orphan",
    )
    transactions = relationship(
        "Transaction", back_populates="product", cascade="all, delete-orphan"
    )


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), unique=True, nullable=False)
    quantity = Column(Integer, default=0, nullable=False)
    min_stock_level = Column(Integer, default=10, nullable=False)
    max_stock_level = Column(Integer, default=1000, nullable=False)
    last_updated = Column(
        DateTime,
        default=datetime.datetime.now(datetime.timezone.utc),
        onupdate=datetime.datetime.now(datetime.timezone.utc),
    )

    # Relaciones
    product = relationship("Product", back_populates="inventory")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    transaction_type = Column(
        String, nullable=False
    )  # 'purchase' (compra), 'sale' (venta), 'adjustment' (ajuste)
    quantity = Column(Integer, nullable=False)
    user_name = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    transaction_date = Column(
        DateTime, default=datetime.datetime.now(datetime.timezone.utc)
    )

    # Relaciones
    product = relationship("Product", back_populates="transactions")

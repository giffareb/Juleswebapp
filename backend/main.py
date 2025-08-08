from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from sqlmodel import Session, select

from backend.database import create_db_and_tables, get_session
from backend.models import Product, Sale, SaleItem # Import SaleItem
from backend import promptpay_utils

# Create the FastAPI app
app = FastAPI(
    title="Modern POS API",
    description="API for a modern Point of Sale system with inventory and profit tracking.",
    version="1.1.0"
)

# CORS Middleware
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models for Request/Response ---

class ProductCreate(BaseModel):
    name: str
    price: float
    cost: float # New field
    quantity: int # New field
    description: Optional[str] = None

class CartItem(BaseModel):
    product_id: int
    quantity: int

class SaleResponse(BaseModel):
    id: int
    timestamp: object
    items: List[CartItem]

class PromptPayRequest(BaseModel):
    amount: float

# --- Event Handlers ---

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# --- API Endpoints ---

@app.get("/api/products", response_model=List[Product], summary="Get all products")
def get_products(session: Session = Depends(get_session)):
    """
    Retrieve a list of all products from the database, including stock levels.
    """
    products = session.exec(select(Product)).all()
    return products

@app.post("/api/products", response_model=Product, status_code=201, summary="Create a new product")
def create_product(product: ProductCreate, session: Session = Depends(get_session)):
    """
    Add a new product to the inventory.
    """
    # The new fields `cost` and `quantity` are now handled automatically
    # as they are part of the ProductCreate model.
    db_product = Product.from_orm(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@app.post("/api/sales", status_code=201, summary="Create a new sale")
def create_sale(cart_items: List[CartItem], session: Session = Depends(get_session)):
    """
    Process a new sale from a list of cart items.
    This endpoint performs a transaction to:
    1. Create a single Sale record.
    2. For each item in the cart, create a SaleItem record.
    3. Deduct the sold quantity from the Product's stock.
    The entire operation is a transaction. It will fail if any product is not found
    or if there is insufficient stock for any item.
    """
    # Create a new Sale record to link all items in this transaction
    new_sale = Sale()
    session.add(new_sale)
    session.commit()
    session.refresh(new_sale)

    for item in cart_items:
        # Get the product from DB
        product = session.get(Product, item.product_id)
        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product with id {item.product_id} not found."
            )

        # Check for sufficient stock
        if product.quantity < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for {product.name}. Available: {product.quantity}, Requested: {item.quantity}"
            )

        # Deduct stock
        product.quantity -= item.quantity

        # Create the SaleItem record
        sale_item = SaleItem(
            sale_id=new_sale.id,
            product_id=product.id,
            quantity=item.quantity,
            price_at_sale=product.price,
            cost_at_sale=product.cost
        )
        session.add(sale_item)

    # Commit the transaction to save all changes
    session.commit()

    return {"message": "Sale created successfully", "sale_id": new_sale.id}


@app.post("/api/payment/promptpay", summary="Generate PromptPay QR Payload")
def get_promptpay_payload(request: PromptPayRequest):
    """
    Generates a standardized PromptPay QR code payload string from an amount.
    """
    phone_number = "0917797477"
    payload = promptpay_utils.generate_payload(phone_number, request.amount)
    return {"payload": payload}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Modern POS Backend v1.1"}

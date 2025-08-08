from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from sqlmodel import Session, select

from backend.database import create_db_and_tables, get_session
from backend.models import Product, Sale
from backend import promptpay_utils

# Create the FastAPI app
app = FastAPI()

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

# Pydantic models for request bodies
class ProductCreate(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

class SaleCreate(BaseModel):
    total_amount: float
    # In a real app, you'd likely have a list of product IDs and quantities
    # For now, just the total amount is fine as per the models.

class PromptPayRequest(BaseModel):
    amount: float

# Event handler to create DB and tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# API Endpoints
@app.get("/api/products", response_model=List[Product])
def get_products(session: Session = Depends(get_session)):
    products = session.exec(select(Product)).all()
    return products

@app.post("/api/products", response_model=Product)
def create_product(product: ProductCreate, session: Session = Depends(get_session)):
    db_product = Product.from_orm(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@app.post("/api/sales", response_model=Sale)
def create_sale(sale: SaleCreate, session: Session = Depends(get_session)):
    db_sale = Sale.from_orm(sale)
    session.add(db_sale)
    session.commit()
    session.refresh(db_sale)
    return db_sale

@app.post("/api/payment/promptpay")
def get_promptpay_payload(request: PromptPayRequest):
    # The phone number is hardcoded as per the instructions
    phone_number = "0917797477"
    payload = promptpay_utils.generate_payload(phone_number, request.amount)
    return {"payload": payload}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Modern POS Backend"}

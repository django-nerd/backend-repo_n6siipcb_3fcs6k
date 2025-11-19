"""
Database Schemas for Nizard Gaming

Each Pydantic model represents a collection in MongoDB. The collection name
is the lowercase of the class name (e.g., Team -> "team").
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

# Core user (kept for potential future use)
class User(BaseModel):
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: Optional[str] = Field(None, description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

# Merchandise product
class Product(BaseModel):
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    image_url: Optional[str] = Field(None, description="Main product image")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Esports team information
class Team(BaseModel):
    name: str = Field(..., description="Team name")
    game: str = Field(..., description="Game title (e.g., BGMI, Valorant)")
    description: Optional[str] = Field(None, description="Short bio / highlights")
    tier: Optional[str] = Field(None, description="Tier or division")
    availability: str = Field("available", description="available | booked | tryouts")
    contact_email: Optional[EmailStr] = Field(None, description="Point of contact")

# Hire/apply/contact application
class Application(BaseModel):
    name: str = Field(..., description="Applicant or company name")
    email: EmailStr
    phone: Optional[str] = None
    type: str = Field(..., description="hire-team | content | join-team")
    game: Optional[str] = Field(None, description="Target game if relevant")
    message: Optional[str] = None
    budget: Optional[str] = Field(None, description="Budget range if hiring")
    role: Optional[str] = Field(None, description="Preferred role if joining team")
    created_at: Optional[datetime] = None

# Order item for merchandise
class OrderItem(BaseModel):
    product_id: str = Field(..., description="Referenced product _id as string")
    title: str
    price: float
    quantity: int = Field(..., ge=1)
    image_url: Optional[str] = None

# Merchandise order
class Order(BaseModel):
    customer_name: str
    email: EmailStr
    address: str
    items: List[OrderItem]
    total_amount: float = Field(..., ge=0)
    status: str = Field("pending", description="pending | paid | shipped | delivered | cancelled")
    notes: Optional[str] = None
    created_at: Optional[datetime] = None

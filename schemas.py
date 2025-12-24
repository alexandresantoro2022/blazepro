from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from models import UserRole, OrderStatus, PaymentStatus, PaymentMethod

# Base Schemas
class AddressBase(BaseModel):
    street: str
    number: str
    complement: Optional[str] = None
    neighborhood: str
    city: str
    state: str
    zip_code: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_default: bool = False

class AddressCreate(AddressBase):
    pass

class AddressUpdate(AddressBase):
    street: Optional[str] = None
    number: Optional[str] = None
    neighborhood: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None

class Address(AddressBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    phone: str
    full_name: str
    role: UserRole = UserRole.CUSTOMER

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    addresses: List[Address] = []

    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str

# Restaurant Schemas
class RestaurantBase(BaseModel):
    name: str
    description: Optional[str] = None
    phone: str
    email: EmailStr
    street: str
    number: str
    complement: Optional[str] = None
    neighborhood: str
    city: str
    state: str
    zip_code: str
    delivery_fee: float = 5.0
    minimum_order: float = 20.0
    delivery_time: int = 45

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    delivery_fee: Optional[float] = None
    minimum_order: Optional[float] = None
    delivery_time: Optional[int] = None
    is_open: Optional[bool] = None
    opening_hours: Optional[Dict[str, Any]] = None

class Restaurant(RestaurantBase):
    id: int
    owner_id: int
    logo_url: Optional[str] = None
    banner_url: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_open: bool
    is_active: bool
    rating: float
    total_reviews: int
    opening_hours: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Category Schemas
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    display_order: int = 0

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None

class Category(CategoryBase):
    id: int
    restaurant_id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Product Schemas
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0)
    category_id: int
    preparation_time: int = 20

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    category_id: Optional[int] = None
    preparation_time: Optional[int] = None
    is_available: Optional[bool] = None

class Product(ProductBase):
    id: int
    restaurant_id: int
    image_url: Optional[str] = None
    is_available: bool
    is_active: bool
    created_at: datetime
    category: Optional[Category] = None

    class Config:
        from_attributes = True

# Order Item Schemas
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    notes: Optional[str] = None

class OrderItem(OrderItemBase):
    price: float
    product: Optional[Product] = None

    class Config:
        from_attributes = True

# Order Schemas
class OrderBase(BaseModel):
    delivery_address_id: int
    payment_method: PaymentMethod
    customer_notes: Optional[str] = None

class OrderCreate(OrderBase):
    restaurant_id: int
    items: List[OrderItemBase]

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    delivery_person_id: Optional[int] = None
    delivery_notes: Optional[str] = None

class Order(OrderBase):
    id: int
    order_number: str
    customer_id: int
    restaurant_id: int
    delivery_person_id: Optional[int] = None
    subtotal: float
    delivery_fee: float
    total: float
    status: OrderStatus
    payment_status: PaymentStatus
    created_at: datetime
    confirmed_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    cancellation_reason: Optional[str] = None
    rating: Optional[int] = None
    review_text: Optional[str] = None
    
    customer: Optional[User] = None
    restaurant: Optional[Restaurant] = None
    delivery_person: Optional[User] = None
    delivery_address: Optional[Address] = None

    class Config:
        from_attributes = True

# Payment Schemas
class PaymentBase(BaseModel):
    method: PaymentMethod
    amount: float = Field(gt=0)

class PaymentCreate(PaymentBase):
    order_id: int
    payment_data: Optional[Dict[str, Any]] = None

class Payment(PaymentBase):
    id: int
    order_id: int
    transaction_id: str
    status: PaymentStatus
    created_at: datetime
    paid_at: Optional[datetime] = None
    refunded_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Review Schemas
class ReviewBase(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    restaurant_id: int
    order_id: int

class Review(ReviewBase):
    id: int
    user_id: int
    restaurant_id: int
    order_id: int
    created_at: datetime
    user: Optional[User] = None

    class Config:
        from_attributes = True

# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Response Schemas
class MessageResponse(BaseModel):
    message: str
    success: bool = True

class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    per_page: int
    pages: int

# Delivery Tracking Schema
class DeliveryTrackingCreate(BaseModel):
    order_id: int
    latitude: float
    longitude: float

class DeliveryTracking(DeliveryTrackingCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
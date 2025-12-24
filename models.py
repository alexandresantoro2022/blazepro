from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Enum, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

# Enums
class UserRole(str, enum.Enum):
    CUSTOMER = "customer"
    RESTAURANT = "restaurant"
    DELIVERY = "delivery"
    ADMIN = "admin"

class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERING = "delivering"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"

class PaymentMethod(str, enum.Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PIX = "pix"
    CASH = "cash"

# Tabela de associação para itens do pedido
order_items = Table('order_items', Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id')),
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('quantity', Integer, default=1),
    Column('price', Float),
    Column('notes', Text)
)

# Modelos
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    addresses = relationship("Address", back_populates="user")
    customer_orders = relationship("Order", foreign_keys="Order.customer_id", back_populates="customer")
    delivery_orders = relationship("Order", foreign_keys="Order.delivery_person_id", back_populates="delivery_person")
    restaurant = relationship("Restaurant", back_populates="owner", uselist=False)
    reviews = relationship("Review", back_populates="user")

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    street = Column(String, nullable=False)
    number = Column(String, nullable=False)
    complement = Column(String)
    neighborhood = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    user = relationship("User", back_populates="addresses")
    orders = relationship("Order", back_populates="delivery_address")

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), unique=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    logo_url = Column(String)
    banner_url = Column(String)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    
    # Endereço
    street = Column(String, nullable=False)
    number = Column(String, nullable=False)
    complement = Column(String)
    neighborhood = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Configurações
    delivery_fee = Column(Float, default=5.0)
    minimum_order = Column(Float, default=20.0)
    delivery_time = Column(Integer, default=45)  # em minutos
    is_open = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    rating = Column(Float, default=0.0)
    total_reviews = Column(Integer, default=0)
    
    # Horários de funcionamento (JSON)
    opening_hours = Column(Text)  # JSON com horários por dia da semana
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    owner = relationship("User", back_populates="restaurant")
    categories = relationship("Category", back_populates="restaurant")
    products = relationship("Product", back_populates="restaurant")
    orders = relationship("Order", back_populates="restaurant")
    reviews = relationship("Review", back_populates="restaurant")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    name = Column(String, nullable=False)
    description = Column(Text)
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    restaurant = relationship("Restaurant", back_populates="categories")
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    price = Column(Float, nullable=False)
    image_url = Column(String)
    preparation_time = Column(Integer, default=20)  # em minutos
    is_available = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    restaurant = relationship("Restaurant", back_populates="products")
    category = relationship("Category", back_populates="products")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String, unique=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"))
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    delivery_person_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    delivery_address_id = Column(Integer, ForeignKey("addresses.id"))
    
    # Valores
    subtotal = Column(Float, nullable=False)
    delivery_fee = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    
    # Status
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    confirmed_at = Column(DateTime(timezone=True))
    delivered_at = Column(DateTime(timezone=True))
    cancelled_at = Column(DateTime(timezone=True))
    
    # Notas
    customer_notes = Column(Text)
    delivery_notes = Column(Text)
    cancellation_reason = Column(Text)
    
    # Avaliação
    rating = Column(Integer)
    review_text = Column(Text)

    # Relacionamentos
    customer = relationship("User", foreign_keys=[customer_id], back_populates="customer_orders")
    restaurant = relationship("Restaurant", back_populates="orders")
    delivery_person = relationship("User", foreign_keys=[delivery_person_id], back_populates="delivery_orders")
    delivery_address = relationship("Address", back_populates="orders")
    payment = relationship("Payment", back_populates="order", uselist=False)

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True)
    transaction_id = Column(String, unique=True, index=True)
    amount = Column(Float, nullable=False)
    method = Column(Enum(PaymentMethod), nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    
    # Dados do pagamento (JSON)
    payment_data = Column(Text)  # JSON com dados específicos do método
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    paid_at = Column(DateTime(timezone=True))
    refunded_at = Column(DateTime(timezone=True))

    # Relacionamentos
    order = relationship("Order", back_populates="payment")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    order_id = Column(Integer, ForeignKey("orders.id"))
    rating = Column(Integer, nullable=False)  # 1-5
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    user = relationship("User", back_populates="reviews")
    restaurant = relationship("Restaurant", back_populates="reviews")

class DeliveryTracking(Base):
    __tablename__ = "delivery_tracking"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    order = relationship("Order")
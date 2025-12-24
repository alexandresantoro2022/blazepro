from sqlalchemy.orm import Session
from models import Order, OrderItem, OrderStatus, UserRole
from typing import Optional, List
import random
import string
from datetime import datetime

def generate_order_number() -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def create_order(db: Session, customer_id: int, restaurant_id: int, 
                 items: List[dict], delivery_address: str, delivery_fee: float,
                 delivery_latitude: float = None, delivery_longitude: float = None,
                 notes: str = None, payment_method: str = "cash"):
    
    subtotal = sum(item['price'] * item['quantity'] for item in items)
    total = subtotal + delivery_fee
    
    order_number = generate_order_number()
    
    db_order = Order(
        order_number=order_number,
        customer_id=customer_id,
        restaurant_id=restaurant_id,
        subtotal=subtotal,
        delivery_fee=delivery_fee,
        total=total,
        delivery_address=delivery_address,
        delivery_latitude=delivery_latitude,
        delivery_longitude=delivery_longitude,
        notes=notes,
        payment_method=payment_method,
        status=OrderStatus.PENDING
    )
    db.add(db_order)
    db.flush()
    
    for item in items:
        order_item = OrderItem(
            order_id=db_order.id,
            menu_item_id=item['menu_item_id'],
            quantity=item['quantity'],
            price=item['price'],
            notes=item.get('notes')
        )
        db.add(order_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order_by_id(db: Session, order_id: int) -> Optional[Order]:
    return db.query(Order).filter(Order.id == order_id).first()

def get_order_by_number(db: Session, order_number: str) -> Optional[Order]:
    return db.query(Order).filter(Order.order_number == order_number).first()

def get_orders_by_customer(db: Session, customer_id: int, skip: int = 0, limit: int = 50) -> List[Order]:
    return db.query(Order).filter(Order.customer_id == customer_id).order_by(Order.created_at.desc()).offset(skip).limit(limit).all()

def get_orders_by_restaurant(db: Session, restaurant_id: int, skip: int = 0, limit: int = 50) -> List[Order]:
    return db.query(Order).filter(Order.restaurant_id == restaurant_id).order_by(Order.created_at.desc()).offset(skip).limit(limit).all()

def get_orders_by_driver(db: Session, driver_id: int, skip: int = 0, limit: int = 50) -> List[Order]:
    return db.query(Order).filter(Order.driver_id == driver_id).order_by(Order.created_at.desc()).offset(skip).limit(limit).all()

def get_pending_orders(db: Session, skip: int = 0, limit: int = 50) -> List[Order]:
    return db.query(Order).filter(Order.status == OrderStatus.PENDING).order_by(Order.created_at.desc()).offset(skip).limit(limit).all()

def get_available_orders_for_delivery(db: Session, skip: int = 0, limit: int = 50) -> List[Order]:
    return db.query(Order).filter(
        Order.status == OrderStatus.READY,
        Order.driver_id == None
    ).order_by(Order.created_at.desc()).offset(skip).limit(limit).all()

def update_order_status(db: Session, order_id: int, status: OrderStatus, driver_id: int = None):
    order = get_order_by_id(db, order_id)
    if order:
        order.status = status
        order.updated_at = datetime.utcnow()
        if driver_id:
            order.driver_id = driver_id
        db.commit()
        db.refresh(order)
    return order

def assign_driver_to_order(db: Session, order_id: int, driver_id: int):
    order = get_order_by_id(db, order_id)
    if order:
        order.driver_id = driver_id
        order.status = OrderStatus.IN_DELIVERY
        order.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(order)
    return order

def cancel_order(db: Session, order_id: int):
    return update_order_status(db, order_id, OrderStatus.CANCELLED)

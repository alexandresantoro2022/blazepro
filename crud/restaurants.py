from sqlalchemy.orm import Session
from models import Restaurant, MenuItem
from typing import Optional, List

def get_restaurant_by_id(db: Session, restaurant_id: int) -> Optional[Restaurant]:
    return db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()

def get_restaurants(db: Session, skip: int = 0, limit: int = 100) -> List[Restaurant]:
    return db.query(Restaurant).filter(Restaurant.is_open == True).offset(skip).limit(limit).all()

def get_restaurants_by_owner(db: Session, owner_id: int) -> List[Restaurant]:
    return db.query(Restaurant).filter(Restaurant.owner_id == owner_id).all()

def create_restaurant(db: Session, name: str, description: str, address: str, 
                      phone: str, owner_id: int, latitude: float = None, 
                      longitude: float = None, image_url: str = None,
                      delivery_fee: float = 5.0, min_order: float = 10.0):
    db_restaurant = Restaurant(
        name=name,
        description=description,
        address=address,
        phone=phone,
        owner_id=owner_id,
        latitude=latitude,
        longitude=longitude,
        image_url=image_url,
        delivery_fee=delivery_fee,
        min_order=min_order
    )
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant

def update_restaurant(db: Session, restaurant_id: int, **kwargs):
    restaurant = get_restaurant_by_id(db, restaurant_id)
    if restaurant:
        for key, value in kwargs.items():
            if hasattr(restaurant, key) and value is not None:
                setattr(restaurant, key, value)
        db.commit()
        db.refresh(restaurant)
    return restaurant

def get_menu_items(db: Session, restaurant_id: int) -> List[MenuItem]:
    return db.query(MenuItem).filter(
        MenuItem.restaurant_id == restaurant_id,
        MenuItem.is_available == True
    ).all()

def create_menu_item(db: Session, name: str, description: str, price: float,
                     category: str, restaurant_id: int, image_url: str = None):
    db_item = MenuItem(
        name=name,
        description=description,
        price=price,
        category=category,
        restaurant_id=restaurant_id,
        image_url=image_url
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_menu_item_by_id(db: Session, item_id: int) -> Optional[MenuItem]:
    return db.query(MenuItem).filter(MenuItem.id == item_id).first()

def update_menu_item(db: Session, item_id: int, **kwargs):
    item = get_menu_item_by_id(db, item_id)
    if item:
        for key, value in kwargs.items():
            if hasattr(item, key) and value is not None:
                setattr(item, key, value)
        db.commit()
        db.refresh(item)
    return item

def delete_menu_item(db: Session, item_id: int):
    item = get_menu_item_by_id(db, item_id)
    if item:
        db.delete(item)
        db.commit()
        return True
    return False

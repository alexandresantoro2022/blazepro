from database import SessionLocal
from models import User, Restaurant, MenuItem, UserRole
from crud import users, restaurants
import random

def create_seed_data():
    db = SessionLocal()
    
    # Check if data already exists
    existing_users = db.query(User).first()
    if existing_users:
        db.close()
        return
    
    print("Creating seed data...")
    
    # Create admin user
    admin = users.create_user(
        db=db,
        email="admin@deliverypro.com",
        password="admin123",
        full_name="Administrador",
        role=UserRole.ADMIN,
        phone="(11) 99999-9999",
        address="Rua Admin, 123"
    )
    
    # Create restaurant owners
    restaurant_owners = []
    for i in range(1, 4):
        owner = users.create_user(
            db=db,
            email=f"restaurante{i}@email.com",
            password="123456",
            full_name=f"Dono Restaurante {i}",
            role=UserRole.RESTAURANT,
            phone=f"(11) 9888{i}-000{i}",
            address=f"Rua Comercial, {i}00"
        )
        restaurant_owners.append(owner)
    
    # Create drivers
    drivers = []
    for i in range(1, 6):
        driver = users.create_user(
            db=db,
            email=f"entregador{i}@email.com",
            password="123456",
            full_name=f"Entregador {i}",
            role=UserRole.DRIVER,
            phone=f"(11) 9777{i}-000{i}",
            address=f"Rua Entregador, {i}0"
        )
        drivers.append(driver)
    
    # Create customers
    customers = []
    for i in range(1, 11):
        customer = users.create_user(
            db=db,
            email=f"cliente{i}@email.com",
            password="123456",
            full_name=f"Cliente {i}",
            role=UserRole.CUSTOMER,
            phone=f"(11) 9666{i}-000{i}",
            address=f"Rua Cliente, {i}00"
        )
        customers.append(customer)
    
    # Create restaurants
    restaurant_data = [
        {
            "name": "Pizzaria Bella Napoli",
            "description": "As melhores pizzas artesanais da cidade",
            "address": "Av. Paulista, 1000",
            "phone": "(11) 3000-1000",
            "delivery_fee": 8.0,
            "min_order": 25.0,
            "categories": {
                "Pizzas Tradicionais": [
                    {"name": "Pizza Margherita", "description": "Molho de tomate, mussarela, manjericão", "price": 45.00},
                    {"name": "Pizza Calabresa", "description": "Calabresa, cebola, azeitonas", "price": 42.00},
                    {"name": "Pizza Portuguesa", "description": "Presunto, ovos, cebola, azeitonas", "price": 48.00},
                    {"name": "Pizza Quatro Queijos", "description": "Mussarela, provolone, gorgonzola, parmesão", "price": 52.00},
                ],
                "Pizzas Especiais": [
                    {"name": "Pizza Frango Catupiry", "description": "Frango desfiado, catupiry", "price": 50.00},
                    {"name": "Pizza Bacon", "description": "Bacon, mussarela, cebola", "price": 48.00},
                ],
                "Bebidas": [
                    {"name": "Refrigerante 2L", "description": "Coca-Cola, Guaraná, Fanta", "price": 10.00},
                    {"name": "Suco Natural 500ml", "description": "Laranja, Limão, Morango", "price": 8.00},
                ]
            }
        },
        {
            "name": "Burger House",
            "description": "Hambúrgueres artesanais e suculentos",
            "address": "Rua Augusta, 500",
            "phone": "(11) 3000-2000",
            "delivery_fee": 6.0,
            "min_order": 20.0,
            "categories": {
                "Hambúrgueres": [
                    {"name": "Classic Burger", "description": "Pão, hambúrguer 180g, queijo, alface, tomate", "price": 28.00},
                    {"name": "Bacon Burger", "description": "Pão, hambúrguer 180g, bacon, queijo cheddar", "price": 32.00},
                    {"name": "Double Burger", "description": "Pão, 2 hambúrgueres 180g, queijo, molho especial", "price": 42.00},
                    {"name": "Veggie Burger", "description": "Pão, hambúrguer de grão de bico, queijo, vegetais", "price": 26.00},
                ],
                "Acompanhamentos": [
                    {"name": "Batata Frita", "description": "Porção grande de batatas crocantes", "price": 15.00},
                    {"name": "Onion Rings", "description": "Anéis de cebola empanados", "price": 18.00},
                ],
                "Bebidas": [
                    {"name": "Refrigerante Lata", "description": "Coca-Cola, Guaraná, Sprite", "price": 6.00},
                    {"name": "Milkshake", "description": "Chocolate, Morango, Baunilha", "price": 14.00},
                ]
            }
        },
        {
            "name": "Sushi Master",
            "description": "Culinária japonesa autêntica",
            "address": "Rua da Liberdade, 200",
            "phone": "(11) 3000-3000",
            "delivery_fee": 10.0,
            "min_order": 35.0,
            "categories": {
                "Combinados": [
                    {"name": "Combinado 1", "description": "20 peças variadas de sushi e sashimi", "price": 65.00},
                    {"name": "Combinado 2", "description": "30 peças variadas de sushi e sashimi", "price": 95.00},
                    {"name": "Combinado Especial", "description": "40 peças premium de sushi e sashimi", "price": 135.00},
                ],
                "Hot Rolls": [
                    {"name": "Hot Philadelphia", "description": "Salmão, cream cheese, empanado", "price": 42.00},
                    {"name": "Hot Skin", "description": "Salmão skin, cebolinha, empanado", "price": 38.00},
                ],
                "Temakis": [
                    {"name": "Temaki Salmão", "description": "Salmão, arroz, alga nori", "price": 22.00},
                    {"name": "Temaki Atum", "description": "Atum, arroz, alga nori", "price": 24.00},
                ],
                "Bebidas": [
                    {"name": "Suco de Laranja", "description": "Natural 500ml", "price": 10.00},
                    {"name": "Chá Gelado", "description": "Limão ou Pêssego 500ml", "price": 8.00},
                ]
            }
        }
    ]
    
    for idx, rest_data in enumerate(restaurant_data):
        restaurant = restaurants.create_restaurant(
            db=db,
            name=rest_data["name"],
            description=rest_data["description"],
            address=rest_data["address"],
            phone=rest_data["phone"],
            owner_id=restaurant_owners[idx].id,
            delivery_fee=rest_data["delivery_fee"],
            min_order=rest_data["min_order"]
        )
        
        for category, items in rest_data["categories"].items():
            for item in items:
                restaurants.create_menu_item(
                    db=db,
                    name=item["name"],
                    description=item["description"],
                    price=item["price"],
                    category=category,
                    restaurant_id=restaurant.id
                )
    
    print("Seed data created successfully!")
    db.close()

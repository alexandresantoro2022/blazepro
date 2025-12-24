from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import timedelta
import uvicorn

from database import get_db, init_db
from auth import (
    authenticate_user, create_access_token, get_current_active_user,
    get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES
)
from models import User, Restaurant, MenuItem, Order, OrderStatus, UserRole
from crud import users, restaurants, orders

app = FastAPI(title="DeliveryPro - Sistema de Delivery Profissional")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()
    # Create seed data if needed
    from seed_data import create_seed_data
    create_seed_data()

# ==================== WEB ROUTES ====================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    current_user = None
    
    if token:
        try:
            from auth import get_current_user
            current_user = get_current_user(token.replace("Bearer ", ""), db)
        except:
            pass
    
    all_restaurants = restaurants.get_restaurants(db)
    return templates.TemplateResponse("home.html", {
        "request": request,
        "restaurants": all_restaurants,
        "current_user": current_user
    })

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = authenticate_user(db, email, password)
    if not user:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Email ou senha incorretos"
        })
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return response

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(...),
    phone: str = Form(...),
    address: str = Form(...),
    role: str = Form("customer"),
    db: Session = Depends(get_db)
):
    existing_user = users.get_user_by_email(db, email)
    if existing_user:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Email já cadastrado"
        })
    
    user_role = UserRole(role)
    new_user = users.create_user(
        db=db,
        email=email,
        password=password,
        full_name=full_name,
        phone=phone,
        address=address,
        role=user_role
    )
    
    return RedirectResponse(url="/login", status_code=303)

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("access_token")
    return response

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        from auth import get_current_user
        current_user = get_current_user(token.replace("Bearer ", ""), db)
    except:
        return RedirectResponse(url="/login", status_code=303)
    
    context = {"request": request, "current_user": current_user}
    
    if current_user.role == UserRole.CUSTOMER:
        user_orders = orders.get_orders_by_customer(db, current_user.id)
        context["orders"] = user_orders
        return templates.TemplateResponse("dashboard_customer.html", context)
    
    elif current_user.role == UserRole.RESTAURANT:
        user_restaurants = restaurants.get_restaurants_by_owner(db, current_user.id)
        context["restaurants"] = user_restaurants
        if user_restaurants:
            restaurant_orders = orders.get_orders_by_restaurant(db, user_restaurants[0].id)
            context["orders"] = restaurant_orders
        return templates.TemplateResponse("dashboard_restaurant.html", context)
    
    elif current_user.role == UserRole.DRIVER:
        driver_orders = orders.get_orders_by_driver(db, current_user.id)
        available_orders = orders.get_available_orders_for_delivery(db)
        context["orders"] = driver_orders
        context["available_orders"] = available_orders
        return templates.TemplateResponse("dashboard_driver.html", context)
    
    elif current_user.role == UserRole.ADMIN:
        all_orders = orders.get_pending_orders(db, limit=100)
        all_restaurants = restaurants.get_restaurants(db, limit=100)
        context["orders"] = all_orders
        context["restaurants"] = all_restaurants
        return templates.TemplateResponse("dashboard_admin.html", context)
    
    return templates.TemplateResponse("dashboard_customer.html", context)

@app.get("/restaurant/{restaurant_id}", response_class=HTMLResponse)
async def restaurant_detail(request: Request, restaurant_id: int, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    current_user = None
    
    if token:
        try:
            from auth import get_current_user
            current_user = get_current_user(token.replace("Bearer ", ""), db)
        except:
            pass
    
    restaurant = restaurants.get_restaurant_by_id(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurante não encontrado")
    
    menu_items = restaurants.get_menu_items(db, restaurant_id)
    
    # Group items by category
    categories = {}
    for item in menu_items:
        if item.category not in categories:
            categories[item.category] = []
        categories[item.category].append(item)
    
    return templates.TemplateResponse("restaurant_detail.html", {
        "request": request,
        "restaurant": restaurant,
        "categories": categories,
        "current_user": current_user
    })

@app.post("/restaurant/create")
async def create_restaurant(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    address: str = Form(...),
    phone: str = Form(...),
    delivery_fee: float = Form(5.0),
    min_order: float = Form(10.0),
    db: Session = Depends(get_db)
):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        from auth import get_current_user
        current_user = get_current_user(token.replace("Bearer ", ""), db)
    except:
        return RedirectResponse(url="/login", status_code=303)
    
    new_restaurant = restaurants.create_restaurant(
        db=db,
        name=name,
        description=description,
        address=address,
        phone=phone,
        owner_id=current_user.id,
        delivery_fee=delivery_fee,
        min_order=min_order
    )
    
    return RedirectResponse(url="/dashboard", status_code=303)

@app.post("/menu/add")
async def add_menu_item(
    request: Request,
    restaurant_id: int = Form(...),
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    category: str = Form(...),
    db: Session = Depends(get_db)
):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        from auth import get_current_user
        current_user = get_current_user(token.replace("Bearer ", ""), db)
    except:
        return RedirectResponse(url="/login", status_code=303)
    
    restaurants.create_menu_item(
        db=db,
        name=name,
        description=description,
        price=price,
        category=category,
        restaurant_id=restaurant_id
    )
    
    return RedirectResponse(url="/dashboard", status_code=303)

@app.post("/order/create")
async def create_order(
    request: Request,
    restaurant_id: int = Form(...),
    items: str = Form(...),  # JSON string
    delivery_address: str = Form(...),
    notes: str = Form(""),
    payment_method: str = Form("cash"),
    db: Session = Depends(get_db)
):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        from auth import get_current_user
        current_user = get_current_user(token.replace("Bearer ", ""), db)
    except:
        return RedirectResponse(url="/login", status_code=303)
    
    import json
    items_list = json.loads(items)
    
    restaurant = restaurants.get_restaurant_by_id(db, restaurant_id)
    
    new_order = orders.create_order(
        db=db,
        customer_id=current_user.id,
        restaurant_id=restaurant_id,
        items=items_list,
        delivery_address=delivery_address,
        delivery_fee=restaurant.delivery_fee,
        notes=notes,
        payment_method=payment_method
    )
    
    return RedirectResponse(url="/dashboard", status_code=303)

@app.post("/order/{order_id}/update-status")
async def update_order_status(
    request: Request,
    order_id: int,
    new_status: str = Form(...),
    db: Session = Depends(get_db)
):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        from auth import get_current_user
        current_user = get_current_user(token.replace("Bearer ", ""), db)
    except:
        return RedirectResponse(url="/login", status_code=303)
    
    status_enum = OrderStatus(new_status)
    orders.update_order_status(db, order_id, status_enum)
    
    return RedirectResponse(url="/dashboard", status_code=303)

@app.post("/order/{order_id}/assign-driver")
async def assign_driver(
    request: Request,
    order_id: int,
    db: Session = Depends(get_db)
):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        from auth import get_current_user
        current_user = get_current_user(token.replace("Bearer ", ""), db)
    except:
        return RedirectResponse(url="/login", status_code=303)
    
    if current_user.role != UserRole.DRIVER:
        raise HTTPException(status_code=403, detail="Apenas entregadores podem aceitar pedidos")
    
    orders.assign_driver_to_order(db, order_id, current_user.id)
    
    return RedirectResponse(url="/dashboard", status_code=303)

# ==================== API ROUTES ====================

@app.get("/api/restaurants")
async def api_get_restaurants(db: Session = Depends(get_db)):
    all_restaurants = restaurants.get_restaurants(db)
    return all_restaurants

@app.get("/api/restaurant/{restaurant_id}/menu")
async def api_get_menu(restaurant_id: int, db: Session = Depends(get_db)):
    menu_items = restaurants.get_menu_items(db, restaurant_id)
    return menu_items

@app.get("/api/orders/my")
async def api_get_my_orders(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    if current_user.role == UserRole.CUSTOMER:
        user_orders = orders.get_orders_by_customer(db, current_user.id)
    elif current_user.role == UserRole.RESTAURANT:
        user_restaurants = restaurants.get_restaurants_by_owner(db, current_user.id)
        if user_restaurants:
            user_orders = orders.get_orders_by_restaurant(db, user_restaurants[0].id)
        else:
            user_orders = []
    elif current_user.role == UserRole.DRIVER:
        user_orders = orders.get_orders_by_driver(db, current_user.id)
    else:
        user_orders = []
    
    return user_orders

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)

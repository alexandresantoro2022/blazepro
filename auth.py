from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import TokenData
import os
from dotenv import load_dotenv

load_dotenv()

# Configurações
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Contexto de criptografia
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

# Funções de hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha está correta"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Gera o hash da senha"""
    return pwd_context.hash(password)

# Funções JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Cria um token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    """Verifica e decodifica o token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        email: str = payload.get("email")
        role: str = payload.get("role")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id, email=email, role=role)
        return token_data
    except JWTError:
        raise credentials_exception

# Dependências de autenticação
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Obtém o usuário atual através do token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_token(token, credentials_exception)
    user = db.query(User).filter(User.id == token_data.user_id).first()
    
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Verifica se o usuário está ativo"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Dependências de autorização por role
async def get_admin_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Verifica se o usuário é admin"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

async def get_restaurant_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Verifica se o usuário é restaurante ou admin"""
    if current_user.role not in ["restaurant", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

async def get_delivery_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Verifica se o usuário é entregador ou admin"""
    if current_user.role not in ["delivery", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

# Funções auxiliares
def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Autentica um usuário"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_user_token(user: User) -> dict:
    """Cria token para um usuário"""
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email,
            "role": user.role.value
        },
        expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
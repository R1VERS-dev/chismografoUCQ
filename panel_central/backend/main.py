from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
import httpx
import os
import uvicorn
from typing import Optional

# Importar modelos y utilidades locales
import models
import schemas
import crud
from database import SessionLocal, engine, Base

# Configuración
SECRET_KEY = "tu_clave_secreta_super_segura_cambiala_en_produccion"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# URLs de las APIs existentes
SERGIO_API_URL = "http://localhost:8001"
ANDREA_API_URL = "http://localhost:8002"

# Crear tablas
Base.metadata.create_all(bind=engine)

# Configurar FastAPI
app = FastAPI(
    title="Panel Central API Hub",
    description="Panel centralizado para gestión de APIs y autenticación",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuración de seguridad
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependencias
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

# Rutas de autenticación
@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    return crud.create_user(db=db, user=user)

@app.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

# Rutas del frontend
@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    return FileResponse('static/index.html')

@app.get("/dashboard", response_class=HTMLResponse)
def serve_dashboard():
    return FileResponse('static/dashboard.html')

@app.get("/login", response_class=HTMLResponse)
def serve_login():
    return FileResponse('static/login.html')

# Proxy para las APIs existentes
@app.get("/api/sergio/{path:path}")
async def proxy_sergio(path: str, request: Request, current_user: models.User = Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        url = f"{SERGIO_API_URL}/{path}"
        params = dict(request.query_params)
        response = await client.get(url, params=params)
        return response.json()

@app.post("/api/sergio/{path:path}")
async def proxy_sergio_post(path: str, request: Request, current_user: models.User = Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        url = f"{SERGIO_API_URL}/{path}"
        body = await request.body()
        headers = {"Content-Type": "application/json"}
        response = await client.post(url, content=body, headers=headers)
        return response.json()

@app.delete("/api/sergio/{path:path}")
async def proxy_sergio_delete(path: str, current_user: models.User = Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        url = f"{SERGIO_API_URL}/{path}"
        response = await client.delete(url)
        return response.json() if response.content else {"message": "Deleted successfully"}

@app.get("/api/andrea/{path:path}")
async def proxy_andrea(path: str, request: Request, current_user: models.User = Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        url = f"{ANDREA_API_URL}/{path}"
        params = dict(request.query_params)
        response = await client.get(url, params=params)
        return response.json()

@app.post("/api/andrea/{path:path}")
async def proxy_andrea_post(path: str, request: Request, current_user: models.User = Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        url = f"{ANDREA_API_URL}/{path}"
        body = await request.body()
        headers = {"Content-Type": "application/json"}
        response = await client.post(url, content=body, headers=headers)
        return response.json()

@app.delete("/api/andrea/{path:path}")
async def proxy_andrea_delete(path: str, current_user: models.User = Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        url = f"{ANDREA_API_URL}/{path}"
        response = await client.delete(url)
        return response.json() if response.content else {"message": "Deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import users as user_model
from ..schemas import users as user_schemas
from config.config import settings
from database.database import engine, get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
import datetime

router = APIRouter(
    prefix="/users"
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

# Hashing utility with bcrypt


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
user_model.Base.metadata.create_all(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.datetime.utcnow() + expires_delta
        else:
            expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        settings.logger.exception("create access token error", str(e))
        raise HTTPException(status_code=500, detail="access token exception")


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_schemas.TokenData(email=email)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    return decode_access_token(token)


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


@router.get("/about_me",  response_model=user_schemas.User)
def read_users_me(current_user: user_schemas.TokenData = Depends(get_current_user), db: Session = Depends(get_db)):
    db_user = None
    if current_user.email:
        db_user = db.query(user_model.User).filter(
            user_model.User.email == current_user.email).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/", response_model=user_schemas.User)
def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = get_password_hash(user.password)
    db_user = user_model.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/", response_model=List[user_schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(user_model.User).offset(skip).limit(limit).all()
    return users


@router.get("/{user_id}", response_model=user_schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(user_model.User).filter(
        user_model.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{user_id}", response_model=user_schemas.User)
def update_user(user_id: int, user: user_schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(user_model.User).filter(
        user_model.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key in db_user.__dict__.keys():
        if user.model_dump().get(key, None) is not None:
            if key == "password":
                setattr(db_user, key, user.create_hashed_password())
                continue
            setattr(db_user, key, user.model_dump().get(key, ""))
        else:
            setattr(db_user, key, db_user.__dict__.get(key, ""))
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/{user_id}", response_model=user_schemas.UserDelete)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(user_model.User).filter(
        user_model.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"id": user_id}


@router.post("/login", response_model=user_schemas.Token)
def login_user(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(user_model.User).filter(
        user_model.User.email == user.username).first()
    if not db_user:
        db_user = db.query(user_model.User).filter(
            user_model.User.username == user.username).first()
    if not db_user:
        raise HTTPException(
            status_code=401, detail="Incorrect email/username or password")
    else:
        if verify_password(user.password, db_user.password):
            access_token_expires = datetime.timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": db_user.email}, expires_delta=access_token_expires)
            return {"access_token": access_token, "token_type": "bearer"}
        else:
            raise HTTPException(
                status_code=401, detail="Incorrect email/username or password")

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import DecodeError
from dotenv import load_dotenv
import os
import uuid
from datetime import datetime, timedelta
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

load_dotenv()


# SQLAlchemy configuration
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define your user model
class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    guid = Column(String(36), nullable=False, unique=True)
    fullname = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

# Create the table
Base.metadata.create_all(bind=engine)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def exist_user(email:str, db):
    return db.query(UserModel).filter(UserModel.email == email).first()

def create_user(email: str, fullname: str, password: str, db):
    hashed_password = pwd_context.hash(password)
    user = UserModel(email=email, password=hashed_password, guid= uuid.uuid4(), fullname=fullname)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Function to authenticate user
def authenticate_user(email: str, password: str, db):
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user or not verify_password(password, user.password):
        return None
    return user

def current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"),algorithms=["HS256"])
        email: str = payload.get("email")
        guid: str = payload.get("guid")
        id: str = payload.get("id")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
        token_data = UserModel(email=email, guid=guid, id=id)
        return token_data
    except DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token")

        

def create_jwt(email: str, fullname: str, guid: str, id: int):
    jwt_payload = {"email" : email, "fullname" : fullname, "guid" : guid, "id" : id }
    expire = datetime.utcnow() + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    jwt_payload.update({"exp": expire})
    jwt_token = jwt.encode(jwt_payload, os.getenv("SECRET_KEY"), algorithm="HS256")

    return jwt_token
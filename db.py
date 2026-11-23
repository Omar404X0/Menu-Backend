import os
from pathlib import Path

from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

pwd_pass = CryptContext(schemes=['bcrypt'], deprecated="auto")


def hashfunction(password):
    return pwd_pass.hash(password)


def verify_password(plain, hashed):
    return pwd_pass.verify(plain, hashed)


BASE_DIR = Path(__file__).resolve().parent

DATABASE_URL = os.getenv('DATABASE_URL', f"sqlite:///{BASE_DIR / 'main.db'}")

if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

if DATABASE_URL.startswith('postgresql'):
    eng = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
        connect_args={'connect_timeout': 15},
    )
else:
    eng = create_engine(DATABASE_URL)


menu = [

    {"name": "Cappuccino",         "price": 112, "category": "hot"},
    {"name": "Latte",              "price": 112, "category": "hot"},
    {"name": "Flat White",         "price": 105, "category": "hot"},
    {"name": "Spanish Latte",      "price": 132, "category": "hot"},
    {"name": "Caramel Macchiato",  "price": 132, "category": "hot"},
    {"name": "Turkish Cappuccino", "price": 92,  "category": "hot"},
    {"name": "Hot Chocolate",      "price": 127, "category": "hot"},
    {"name": "Tea",                "price": 65,  "category": "hot"},


    {"name": "Iced Latte",         "price": 112, "category": "cold"},
    {"name": "Iced Spanish Latte", "price": 127, "category": "cold"},
    {"name": "Latte Frappe",       "price": 127, "category": "cold"},
    {"name": "Iced Matcha",        "price": 132, "category": "cold"},


    {"name": "Carrot Cake",        "price": 130, "category": "cake"},
    {"name": "Cheesecake",         "price": 130, "category": "cake"},
    {"name": "Tiramisu Cake",      "price": 130, "category": "cake"},
    {"name": "Salted Caramel Brownie", "price": 115, "category": "cake"},
]


Base = declarative_base()


Session_local = sessionmaker(bind=eng)


class Menu (Base) :
    __tablename__ ='menu'
    id = Column(Integer,primary_key=True)
    name=Column(String,nullable=False,unique=True)
    category=Column(String,nullable=False)
    price = Column(Float,nullable=False)



class Admin (Base) :
    __tablename__ ='admin'
    id = Column(Integer,primary_key=True)
    email=Column(String,nullable=False,unique=True)
    password =Column(String,nullable=False)


def seed_menu():
    session = Session_local()
    try:
        if session.query(Menu).count() == 0:
            for item in menu:
                session.add(Menu(**item))
            session.commit()
    finally:
        session.close()


def ensure_admin():
    email = os.getenv('ADMIN_EMAIL')
    password = os.getenv('ADMIN_PASSWORD')
    if not email or not password:
        return

    session = Session_local()
    try:
        if not session.query(Admin).filter(Admin.email == email).first():
            session.add(Admin(email=email, password=hashfunction(password)))
            session.commit()
    finally:
        session.close()


Base.metadata.create_all(eng)

ensure_admin()

if os.getenv('SEED_MENU') == '1':
    seed_menu()


if __name__ == '__main__':
    seed_menu()
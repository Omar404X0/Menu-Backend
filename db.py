from sqlalchemy import Column,Integer,String,Float,ForeignKey,Table,create_engine 
from sqlalchemy.orm import sessionmaker , declarative_base 
from passlib.context import CryptContext

from pathlib import Path
pwd_pass = CryptContext(schemes=['bcrypt'],deprecated="auto")

def hashfunction (password) : 
    return pwd_pass.hash(password)


def verify_password(plain, hashed):
    return pwd_pass.verify(plain, hashed)


BASE_DIR = Path(__file__).resolve().parent
eng = create_engine(f"sqlite:///{BASE_DIR / 'main.db'}")


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



Base.metadata.create_all(eng)


if __name__ =='__main__' :
    session= Session_local()
    for item in menu :
        session.add(Menu(**item))

    
    
    session.commit()
    session.close()


if __name__ =='__main__' :
    session= Session_local()
    
    session.add(Admin(email='o24@gmail.com',password=hashfunction('1234')))
    session.commit()
    session.close()


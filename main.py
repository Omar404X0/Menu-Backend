from fastapi import FastAPI ,HTTPException
from pydantic import BaseModel 
from fastapi.middleware.cors import CORSMiddleware
from db import Session_local ,Menu ,Admin, pwd_pass ,verify_password
import redis 
import secrets

import os

r = redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=6379, db=0, decode_responses=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)



class Item(BaseModel) :
    name:str
    category:str
    price : int




@app.get('/') 
def show_items (): 
    menu_list=[]
    session= Session_local()
    All_items = session.query(Menu).all()
    for item in All_items :
        menu_list.append({ 'id':item.id , 'name':item.name ,'price':item.price, 'category':item.category})
    session.close()
    return menu_list 

     


class Admin_type (BaseModel) : 
    
    password : str
    email : str

@app.post('/edit/login')
async def checkAdmin (admin:Admin_type) :
    session = Session_local()
    try:
        user = session.query(Admin).filter(Admin.email == admin.email).first()

        if not user or not verify_password(admin.password,user.password) :
            raise HTTPException(status_code=401,detail='Wrong In email or password')

        
        token = secrets.token_urlsafe(32)
        r.set(f'session:{token}',user.id,ex=3600)
        return{'token':token}
    finally:
        session.close()

@app.get('/edit/get')
async def show_items() : 
    session =Session_local()
    items_list =[]
    all_items = session.query(Menu).all()
    for item in all_items : 
    
        items_list.append({'name':item.name,'id':item.id,'price':item.price,'category':item.category})
    session.close()
    return items_list
    

class Edit_item (BaseModel) :
    token:str
    name:str
    price:int
    id:int
    category:str 

@app.post('/edit/item') 
async def edit (edit_item:Edit_item) : 
    if not r.get(f'session:{edit_item.token}'):
        raise HTTPException(status_code=401,detail='Token are Invalid Or Not Found Please Login Again')

    session=Session_local()
    item = session.query(Menu).filter(Menu.id == edit_item.id).first()
    item.category = edit_item.category
    item.name = edit_item.name
    item.price = edit_item.price
    session.commit()
    session.close()
    return {"ok":True}



class Delete_item(BaseModel):
    token: str
    id: int


@app.post('/edit/delete')
async def delete(delete_item: Delete_item):
    if not r.get(f'session:{delete_item.token}'):
        raise HTTPException(status_code=401, detail='Token is invalid or expired, please login again')

    session = Session_local()
    try:
        item = session.query(Menu).filter(Menu.id == delete_item.id).first()
        if not item:
            raise HTTPException(status_code=404, detail='Item not found')

        session.delete(item)
        session.commit()
        return {'ok': True}
    finally:
        session.close()


class New_prodact (BaseModel):
    token:str
    name:str
    price:int
    category:str


@app.post('/edit/add')
async def delete(new_prodact: New_prodact):
    if not r.get(f'session:{new_prodact.token}'):
        raise HTTPException(status_code=401, detail='Token is invalid or expired, please login again')

    session = Session_local()
    try:
        new_item = Menu(name = new_prodact.name,price=new_prodact.price,category=new_prodact.category)
        
        

        session.add(new_item)
        session.commit()
        return {'ok': True}
    finally:
        session.close()
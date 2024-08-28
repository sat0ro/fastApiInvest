from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import engine, database
from app import models, schemas, auth

app = FastAPI()

@app.on_event('startup')
async def startup():
    await database .connect()
    
@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()
    
@app.post('/register', response_model = schemas.User)
async def register_user(user: schemas.UserCreate):
    query = models.users.select().where(models.users.c.username == user.username)
    existing_user = await database.fetch_one(query)
    
    if existing_user:
        raise HTTPException(status_code=400, detail='Username already register')
    
    hashed_password = auth.get_password_hash(user.password)
    query = models.users.insert(username=user.username, hashed_password=hashed_password)
    last_record_id = await database.execute(query)
    
    return schemas.User(id=last_record_id, username=user.username)

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: schemas.UserCreate):
    query = models.users.select().where(models.users.c.username == form_data.username)
    user = await database.fetch_one(query)
    
    if not user or not auth.verify_password(form_data.password, user['haashed_password']):
        raise HTTPException(status_code=400, detail='Invalid username or password')
    
    access_token = auth.create_access_token(data={'sub':user['username']})
    return {'access_token':access_token, 'token_type': 'bearer'}
import logging

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import database
from app import models, schemas, auth
from app import crypto


logging.basicConfig(level=logging.INFO)


app = FastAPI('FastAPI Investment App')

@app.on_event('startup')
async def startup():
    """
    Connect to the database and setup the startup event.
    """
    try:
        if not database.is_connected:
            await database.connect()
            logging.info("Connected to database!")
    except Exception as e:
        logging.error(f"Error connecting to database: {e}")

@app.on_event('shutdown')
async def shutdown():
    """
    Disconnect from the database and setup the shutdown event.
    """
    if database.is_connected:
        try:
            await database.disconnect()
            logging.info("Disconnect from database!")
        except Exception as e:
            logging.error(f"Error disconnecting from database: {e}")
    else:
        logging.info("Database is already disconnected")

    
@app.post('/register', response_model = schemas.User)
async def register_user(user: schemas.UserCreate):
    if not user:
        raise HTTPException(status_code=400, detail='User is empty')
    
    logging.info(f"Регистрация пользователя: {user.username}")
    query = models.users.select().where(models.users.c.username == user.username)
    existing_user = await database.fetch_one(query)
    
    if existing_user:
        raise HTTPException(status_code=400, detail='Username already register')
    
    if not user.password:
        raise HTTPException(status_code=400, detail='Password is empty')
    
    try:
        hashed_password = auth.get_password_hash(user.password)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Error hashing password: {e}')
    
    query = models.users.insert(username=user.username, hashed_password=hashed_password)
    
    try:
        last_record_id = await database.execute(query)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Error inserting user: {e}')
    
    return schemas.User(id=last_record_id, username=user.username, status=200)

@app.post('/token', response_model=schemas.Token)
async def login_for_access_token(form_data: schemas.UserCreate):
    query = models.users.select().where(models.users.c.username == form_data.username)
    user = await database.fetch_one(query)
    
    if user is None or not auth.verify_password(form_data.password, user['hashed_password']):
        raise HTTPException(status_code=400, detail='Invalid username or password')
    
    if user['hashed_password'] is None:
        raise HTTPException(status_code=400, detail='Password is empty')
    
    try:
        access_token = auth.create_access_token(data={'sub': user['username']})
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Error creating access token: {e}')
    
    return {'access_token':access_token, 'token_type': 'bearer'}


@app.post('/add_cryptos')
async def add_cryptos(symbol: str, user: schemas.User):
    if not symbol:
        raise HTTPException(status_code=400, detail='Symbol is empty')
    
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    
    query = models.cryptocurrencies.insert().values(name=symbol, symbol=symbol, user_id=user.id)
    
    try:
        await database.execute(query)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Error inserting cryptos: {e}')
    
    return {'message': f'Cryptocurrency {symbol} added to your list.'}

@app.get('/my_cryptos')
async def get_cryptos(user: schemas.User):
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    
    query = models.cryptocurrencies.select().where(models.cryptocurrencies.c.user_id == user.id)
    user_cryptos = await database.fetch_all(query)
    
    if user_cryptos is None:
        raise HTTPException(status_code=404, detail='Cryptocurrencies not found')
    
    result = []
    for crypto_item in user_cryptos:
        if crypto_item is None:
            raise HTTPException(status_code=404, detail='Cryptocurrency not found')
        
        price = crypto.get_crypto_price(crypto_item['symbol'])
        
        if price is None:
            raise HTTPException(status_code=404, detail='Price not found')
        
        result.append({
            'name': crypto_item['item'],
            'symbol': crypto_item['symbol'],
            'price': price
        })
        
    return result

from pydentic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    
class User(BaseModel):
    id: int
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
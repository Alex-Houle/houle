from typing import Optional, List
from pydantic import BaseModel
from flask_login import UserMixin

class User(BaseModel):
    '''a user'''
    username: str
    password: str
    admin: Optional[bool] = False

class UserQuery(BaseModel):
    '''user query model'''
    username: Optional[str] = None
    password: Optional[str] = None
    admin: Optional[bool] = None

class UserUpdate(BaseModel):
    '''user update model'''
    password: Optional[str] = None
    admin: Optional[bool] = None

class UserAuth(BaseModel):
    username: str
    password: str

class UserLogin(UserMixin):
    def __init__(self, id: str, username, admin):
        self.id = id
        self.username = username
        self.admin = admin

class UserCollection(BaseModel):
    users: List[dict]

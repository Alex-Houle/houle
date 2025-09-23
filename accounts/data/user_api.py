from .user_manager import UserManager
from .user_models import *

class UserAPI:
    def __init__(self, user_manager: UserManager):
        self.um = user_manager

    def authenticate(self, auth: dict) -> dict | None:
        '''
        Authenticates a user by username and password.
        Returns the user dict if successful, otherwise None.
        '''
        ua = UserAuth(**auth)
        u = self.um.read(ua.model_dump())
        if u:
            user_doc = u[0]
            user_doc['id'] = str(user_doc.pop('_id'))
            return user_doc
        return None

    def delete_all(self) -> int:
        return self.um.delete_all()

    def create(self, user: dict) -> str:
        '''takes an unvalidated dict, validates, and passes dict to UserManager for insertion'''
        u = User(**user).model_dump()
        inserted_id = self.um.create(u)
        return str(inserted_id)

    def read_by_id(self, uid: str) -> dict:
        '''reads, validates, and returns dict'''
        u = self.um.read_by_id(uid)
        if u:
            validated_data = User(**u).model_dump()
            validated_data['id'] = str(u['_id'])
            return validated_data
    
    def read_all(self) -> dict:
        us = self.um.read_all()
        for u in us:
            u['id'] = str(u.pop('_id'))
        return UserCollection(users=us).model_dump()
    
    def read(self, query: dict) -> dict:
        q = UserQuery(**query)
        # Use exclude_none=True to only query with the provided fields
        us = self.um.read(q.model_dump(exclude_none=True))
        for u in us:
            u['id'] = str(u.pop('_id'))
        return UserCollection(users=us).model_dump()
    
    def update(self, id: str, update: dict) -> int:
        u = UserUpdate(**update)
        n = self.um.update(id, u.model_dump(exclude_none=True))
        return n
    
    def delete_by_id(self, id: str) -> int:
        return self.um.delete_by_id(id)
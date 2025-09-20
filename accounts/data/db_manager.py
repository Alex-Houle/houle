from bson import ObjectId
import pymongo
from pydantic import BaseModel

class DBManager:

    def __init__(self, conn_str:str, db, col):
        '''connect to db server and set self.col'''
        
        myclient = pymongo.MongoClient(conn_str)
        mydb = myclient[db]
        self.col = mydb[col]
        self.col.create_index("username", unique=True)


    
    def create(self, d: dict):
        '''create user and return inserted_id'''
        
        result = self.col.insert_one(d)
        return result.inserted_id

    def read_by_id(self, obj_id:str):
        '''read user by id and return one
        return None if user not found'''
        
        try:
            result = self.col.find_one({"_id": ObjectId(obj_id)})
            return result
        except:
            return None;

    def read(self,query:dict):
        '''read by query and return many'''
        
        result = self.col.find(query)
        return list(result)
    

    def read_all(self):
        return list(self.col.find({}))

    def update(self,obj_id,updates:dict):
        ''' update by id and return modified_count '''
        
        try:

            result = self.col.update_one(
                {"_id": ObjectId(obj_id)}, 
                {"$set": updates}
            )
            return result.modified_count
        except:
            return 0

    def delete_by_id(self,obj_id):
        ''' delete by id and return deleted_count '''
        
        try:
            result = self.col.delete_one({"_id": ObjectId(obj_id)})
            return result.deleted_count
        except:
            return 0
    
    def delete(self,query:dict):
        ''' update by query and return deleted_count '''
        
        result = self.col.delete_many(query)
        return result.deleted_count
    
    def delete_all(self):
        ''' deletes all entries'''
        result = self.col.delete_many({})
        return result.deleted_count              
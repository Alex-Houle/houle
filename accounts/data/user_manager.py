from .db_manager import DBManager

class UserManager(DBManager):

    def __init__(self, conn_str: str, db: str, col: str):
        '''
        Connect to the database server and set up the collection.
        '''
        super().__init__(conn_str, db, col)
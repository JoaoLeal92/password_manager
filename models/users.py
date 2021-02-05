from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String

# Global Variables
SQLITE = 'sqlite'

# Table Names
USERS = 'users'

class UserDatabase:
  # Instantiate reference object for supported dbs
  DB_ENGINE = {
    SQLITE: 'sqlite:///{DB}'
  }
  db_engine = None
  
  def __init__(self, dbtype, username='', password='', dbname=''):
      dbtype = dbtype.lower()
      print(dbtype)
      
      if dbtype in self.DB_ENGINE.keys():
          engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
          self.db_engine = create_engine(engine_url)
          print(self.db_engine)
      else:
          print("DBType is not found in DB_ENGINE")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

import sys
sys.path.append("..") 

from ..entities.Users import Base, User

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

        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
            self.db_engine = create_engine(engine_url)

            # Creates database, if it doesn't exists
            if not database_exists(engine_url):
                create_database(engine_url)
                print('Created "users" database')

            # Creates users table if it doesn't exists
            if not self.db_engine.has_table('users'):
                try:
                    Base.metadata.create_all(bind=self.db_engine)
                    print('Created "users" table')
                except Exception as e:
                    print('Error during creation of "users" table')
                    print(e)
            
            print(self.db_engine)
        else:
            print("DBType is not found in DB_ENGINE")

    def create_user(self, username: str, password: str,):
        # Checks if user already exists on database
        check_user = self.get_user_by_name(username=username)
        if check_user:
            return 'User already exists'

        new_user = User(username=username, password=password)

        Session = sessionmaker(bind=self.db_engine)

        session = Session()

        session.add(new_user)
        session.commit()

        session.close()

        return 'User created successfuly'

    def get_user_by_name(self, username):
        Session = sessionmaker(bind=self.db_engine)
        session = Session()

        user = session.query(User).filter_by(username=username).first()

        session.close()

        return user

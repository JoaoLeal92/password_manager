from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

import sys

sys.path.append("..")

from ..entities.Credentials import Base, Credential

# Global Variables
SQLITE = 'sqlite'

# Table Names
USERS = 'users'


class CredentialsDatabase:
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
            self.Session = sessionmaker(bind=self.db_engine)

            # Creates database, if it doesn't exists
            if not database_exists(engine_url):
                create_database(engine_url)
                print('Created "Credentials" database')

            # Creates users table if it doesn't exists
            if not self.db_engine.has_table('credentials'):
                try:
                    Base.metadata.create_all(bind=self.db_engine)
                    print('Created "credentials" table')
                except Exception as e:
                    print('Error during creation of "credentials" table')
                    print(e)
        else:
            print("DBType is not found in DB_ENGINE")

    def create_credential(self, username: str, credential_name: str, credential_url: str, credential_password: str):
        # Checks if credential already exists on database
        check_credential = self.get_credential_by_name(credential_name=credential_name)
        if check_credential:
            return None
        # if check_credential:
        #     return 'Credential already exists'

        new_credential = Credential(username=username, name=credential_name, url=credential_url, password=credential_password)

        session = self.Session(expire_on_commit=False)

        session.add(new_credential)
        session.commit()

        session.close()

        return new_credential

    def get_credential_by_name(self, credential_name):
        session = self.Session()

        credential = session.query(Credential).filter_by(name=credential_name).first()

        session.close()

        return credential

    def get_all_credentials(self, username):
        session = self.Session()

        credentials = session.query(Credential).filter_by(username=username).all()

        session.close()

        return credentials

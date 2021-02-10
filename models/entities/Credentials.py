from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Credential(Base):
    __tablename__ = 'credentials'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    url = Column('url', String, nullable=True)
    password = Column('password', String)


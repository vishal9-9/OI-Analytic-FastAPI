from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
import pymysql

engine = create_engine('mysql+pymysql://root:password@localhost/alex')
Base = declarative_base()
database = Session(bind = engine, expire_on_commit = False)

def get_db():
    db = database
    try:
        yield db
    finally:
        db.close()
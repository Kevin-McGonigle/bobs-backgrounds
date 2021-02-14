from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

ENGINE = create_engine("sqlite:///resources/data/db.sqlite", echo=True)
CONNECTION = ENGINE.connect()
SESSION = sessionmaker(ENGINE)
BASE = declarative_base()

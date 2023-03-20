from sqlalchemy_utils import create_database, database_exists
from sqlalchemy import create_engine

from .models import Base

DATABASE_URL = "sqlite:///./weather.db"

if not database_exists(DATABASE_URL):
    create_database(DATABASE_URL)

engine = create_engine(DATABASE_URL)

Base.metadata.create_all(bind=engine)

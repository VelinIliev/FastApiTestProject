from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# sqlite3
# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db'
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

# PostgreSQL
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:velko@localhost/todo_app'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

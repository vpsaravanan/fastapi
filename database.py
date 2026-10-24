# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# For SQLite, use 'sqlite:///./sql_app.db'
# DATABASE_URL = "sqlite:///./test.db"
DATABASE_URL = 'mysql+pymysql://root:password@127.0.0.1:3306/temple?charset=utf8mb4'

# create_engine manages the connection pool
engine = create_engine(
    DATABASE_URL, 
    # connect_args={"check_same_thread": False}  # Only needed for SQLite
)

# Each instance of SessionLocal will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# The base class that our models will inherit from to be registered by the ORM
# import models
Base = declarative_base()
# Base.metadata.create_all(bind=engine)
# print(__file__)
# print(Base.metadata.tables.keys())


# Dependency to get the database session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
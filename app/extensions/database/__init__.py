import os
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import url

db = SQLAlchemy()

uri = url.URL(
    drivername='mysql+pymysql',  # Use the correct driver
    username=os.environ['DB_USER'],
    password=os.environ['DB_PASS'],
    database=os.environ['DB_NAME'],
    host=os.environ['PUBLIC_IP_ADDRESS'],  # Public IP address of the Cloud SQL instance
    port=3306,  # Default MySQL port
    query={}  # Optional: provide an empty dictionary for query if not needed
)
engine = create_engine(uri, pool_size=10, max_overflow=20)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    db_session = SessionLocal() 
    return db_session

#1. import SQLAlchemy parts
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

#2. Create PostgreSQL database and define a database url
DATABASE_URL = os.environ["DATABASE_URL"]

#3. Create SQLAlchemy engine (allows us to use the hosted database)
engine = create_engine(DATABASE_URL)

#4. Create a SessionLocal class (this is the database session, or the instance is)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #we use engine that we defined in previous step

#5. Create a Base class (we use it to create the database models)
Base = declarative_base()




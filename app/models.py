from .database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

#Allowing clients to authenticate with a username + password by storing 
#credentials in our database.
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

    disabled = Column(Boolean, default=False)

    #lists = relationship("List", back_populates="user")




class List(Base):
    __tablename__ = "lists"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False)

    tasks = relationship("Task", back_populates="list")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String, nullable=False)
    completed = Column(Boolean, default=False)

    list_id = Column(Integer, ForeignKey("lists.id"))

    list = relationship("List", back_populates="tasks")


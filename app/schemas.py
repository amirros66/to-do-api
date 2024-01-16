from pydantic import BaseModel
from typing import List

#Users
class UserBase(BaseModel):
    id: int
    username: str

#Allow users to sign up with username and password
class UserCreate(BaseModel):
    username: str
    password: str

#The schema for the database model
class User(UserBase):
    # lists: list[List] = []

    class Config:
        from_attributes = True

 
class UserCredentials(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    exp: int
    sub: str

#Tasks
class TaskBase(BaseModel):
    id: int
    title: str
    completed: bool


class TaskCreate(BaseModel):
    title: str


class Task(TaskBase):
    list_id: int

    class Config:
        orm_mode = True

#Lists
class ListBase(BaseModel):
    id: int
    name: str


class ListCreate(BaseModel):
    name: str


class List(ListBase):
    tasks: list[Task] = []
    owner: User               # add the owner

    class Config:
        from_attributes = True
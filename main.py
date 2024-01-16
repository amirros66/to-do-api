#This is the main FastAPI application & it defines routes to handle GET, POST, and 
#DELETE operations for managing lists / tasks in a database. It uses SQLAlchemy 
#for database interactions, Pydantic for data validation, and FastAPI 
#for building a modern web API. 

#Import necessary modules / classes from FastAPI
from typing import List, Annotated
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
#Import modules from local 'app' package.
from app import lists, models, database, schemas, tasks, users
from app.deps import get_current_user, UserBase
#Had to add above line to define get_current_user + UserBase on line 120


from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


#Create an instance of the FastAPI class, which represents the main application.
app = FastAPI()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/docslogin",  # only for usage in the docs!
    scheme_name="JWT"
)



#Configure Cross-Origin Resource Sharing (CORS) middleware to allow requests from 
#any origin ("*"). CORS headers are added to responses to handle cross-origin requests.
#origins = ["*"]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#Dependency
#Define a function (get_db) to obtain a database session (SessionLocal) using 
#FastAPI's dependency injection. The session is yielded for use in route functions, 
#and it's ensured to be closed after use.

def get_db():
    db = database.SessionLocal()
    #Begins by creating a new DB session ('db') using 
    #'SessionLocal' method from the database module. This session represents a connection 
    #to the database.
    try:
        yield db
    #This try block contains a 'yield' statement. It provides the db session to 
    #the route function that depends on this get_db function which allows the route function
    #to use the session for db operations.
    finally:
        db.close()
    #This finally block ensures that the database session is closed.
        
#Purpose of 'get_db' function:
    #Dependency for Route Functions - When a route function depends on get_db, FastAPI will 
    #automatically provide it with a database session.
    #Database Session Management - ensure that each route function gets its own isolated 
    #session. This helps manage transactions and prevent unintended side effects between different 
    #parts of your application.
    #Resource Cleanup: finally block ensures that the database session is properly closed, even if an error occurs.       


#Users
#Sign up users
@app.post("/users", response_model=schemas.UserBase)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return users.create_user(db, user=user)

#login users
@app.post("/users/login", response_model=schemas.Token)
def login_user(user: schemas.UserCredentials, db: Session = Depends(get_db)):
    return users.login_user(db, user=user)

#on the api, it asks for the access_key
# only that server / api that gave that key should be able to see (this is the JWT token)

@app.post("/docslogin", response_model=schemas.Token) #?schemas.Token?
def login_with_form_data(
    user: OAuth2PasswordRequestForm = Depends(), #dependency injection - automatically provides required dependencies to function.
    #declares a parameter 'user' of type OAuth2PasswordRequestForm.
    #OAuth2PasswordRequestForm is a Pydantic model provided by FastAPI 
    #specifically designed for handling OAuth2 password grant type requests.
    db: Session = Depends(get_db)
):
    return users.login_user(db, user=user)

#LISTS  
#Get all lists
#Define a GET endpoint (/lists) to retrieve a list of items from the database. It 
#uses the get_lists function from the lists file.
@app.get("/lists", response_model=List[schemas.List])
def read_lists(token: Annotated[str, Depends(reuseable_oauth)], skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    db = database.SessionLocal()
    results = lists.get_lists(db, skip=skip, limit=limit)
    if results is None:
        raise HTTPException(status_code=404, detail="No lists found")
    return results




#Create list
@app.post("/lists", response_model=schemas.List)
def create_list(
    list: schemas.ListCreate, 
    user: UserBase = Depends(get_current_user), 
    db: Session = Depends(get_db)
    ):
    return lists.create_list(db, user_id=user.id, list=list)


#Delete list
@app.delete("/lists", response_model=schemas.List)
def delete_lists(list_id: int, db: Session = Depends(get_db)):
    return lists.delete_list(db, list_id=list_id)


#TASKS 

#Get tasks from a list
@app.get("/lists/{list_id}/tasks", response_model=List[schemas.Task])
def read_list_tasks(list_id: int, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    results = tasks.get_tasks(db, list_id=list_id, skip=skip, limit=limit)
    if results is None:
        raise HTTPException(status_code=404, detail="No tasks found")
    return results

#Create task
@app.post("/lists/{list_id}/tasks", response_model=schemas.Task)
def create_list_task(list_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return tasks.create_task(db, list_id=list_id, task=task)

#Delete task
@app.delete("/lists/{list_id}/tasks", response_model=schemas.List)
def delete_list_task(list_id: int, task_id: int, db: Session = Depends(get_db)):
    return tasks.delete_task(db, list_id=list_id, task_id=task_id)
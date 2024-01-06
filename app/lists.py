from sqlalchemy.orm import Session
#Session: a high-level abstraction that represents a "workspace" for your interactions with 
#the database. It provides a way to manage database connections, transactions, and the overall 
#state of your interactions with the database.

from . import models, schemas

#Get lists:
#This function retrieves a list of items from the db taking session as the object, 
#db as a parameter along with optional parameters for pagination. 
def get_lists(db: Session, skip: int = 0, limit: int = 20):
    lists = db.query(models.List).offset(skip).limit(limit).all() #the query part here
    #is what selects all rows from from the list model (which corresponds to a db table).
    print(lists)
    return lists
#Use the provided Session (db) to query the database for a 
#specified number of lists. The offset and limit functions 
#are used for pagination, and all() fetches all the results.
#print lists to console for debugging purposes
#Return the retrieved lists from the function

#Querying: 
#This is used to retrieve data from a database using 
#SQLAlchemy (an ORM Object-Relational Mapping library).
#Reasons for querying:
#Reading Data: The primary purpose of querying is to read data from the database. 
#This could involve retrieving a list of items, fetching a specific item by ID or name.
#Data Manipulation: In the case of creating or deleting a list, querying is used to 
#interact with the database to persist changes.





#Create list:
#This function adds a new list to the db.
def create_list(db: Session, list: schemas.ListCreate):
    db_list = models.List(**list.dict()) #Creates a new instance
    #of the 'list' model using data provided in the 'list'
    #parameter. **list.dict() syntax is used to convert the Pydantic 
    #model to a dictionary and then unpack it.
    db.add(db_list) #adds newly created db_list instance to current db
    #session. The changes are only made within the session and not reflected
    #in the actual db at this point.
    db.commit() #This is where actual db transaction is committed. Changes 
    #made within the session are persisted to underlying db.
    db.refresh(db_list) #After committing the changes this line is used to 
    #refresh the db_list instance with any changes that might have been 
    #applied to it on the db side. 
    return db_list
    #Return newly created list from the function.

#More on commit:
#db.commit() statement triggers the actual commit to the database.
#The commit operation ensures that the changes become permanent and 
#visible to other transactions and sessions. 
#It is a crucial step in the process of persisting changes 
#made within a SQLAlchemy session to the actual database, making them 
#permanent and visible to other parts of the application.



#Delete list
#This function deletes a list from the database based on its ID.
def delete_list(db: Session, list_id: int):
    list = db.query(models.List).filter(models.List.id == list_id).first()
    #Query the database to retrieve the list with the specified ID.
    #Line by line - db.query(models.List) initiates a query on the List model 
    #(representing a database table) within the current database session.
    #.filter(models.List.name == name): filter method is used to specify a filter 
    #criteria for the rows to be retrieved.
    #models.List.name == name is the filter condition. It checks for rows where the 
    #value in the name column of the List table is equal to the provided name parameter.
    #first() : method that fetches only the first result that satisfies the conditions 
    #specified in the query. 
    #list: Result of the query is assigned to a variable named list.
    db.delete(list)
    db.commit()
    #Delete retrieved list from the db and commit changes.
    return list
    #Return the deleted list from the function.

#Get one list
#This function retrieves a specific list from the database based on its ID.
def get_list(db: Session, list_id: int):
    list = db.query(models.List).filter(models.List.id == list_id).first()
    #Query the database to retrieve the list with the specified ID.
    print(list)
    #Print list to console for debugging purposes.
    return list
    #Return the retrieved list from the function.

#Get list by name
#This function retrieves a specific list from the database based on its name.
def get_list_by_name(db: Session, name: str):
    list = db.query(models.List).filter(models.List.name == name).first()
    #Query the database to retrieve the list with the specified name.
    print(list)
    return list

#The above code defines several that interact with a database using SQLAlchemy.
#Session class is used for managing the database sessions, and models and schemas
#contain the data models and pydantic schemas used in these database operations.

import config.config as config
from fastapi import HTTPException
from pydantic import BaseModel
from typing import Optional
from enum import Enum
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions

USER_CONTAINER = config.settings['user_container']
HOST = config.settings['host']
MASTER_KEY = config.settings['master_key']
DATABASE_ID = config.settings['database_id']

#Start database connectors.
dbclient = cosmos_client.CosmosClient(HOST,MASTER_KEY)
database = dbclient.get_database_client(DATABASE_ID)
container = database.get_container_client(USER_CONTAINER)

#Declare classes that will be used for user operations.
class Roles(BaseModel):
    id : str
    role_name: str
    scopes : list
    

class User(BaseModel):      
    id : str
    first_name : str
    last_name : str
    user_principal_name : str
    roles : Roles


async def add_user(User):
    print(f"Trying to create user \'{User}\' in table \'{USER_CONTAINER}\' in database \'{DATABASE_ID}\'")
    
    #Code for insert/upsert here.
    try:
        container.create_item(body=User)
    except exceptions.CosmosResourceExistsError:
        print(f"User \'{User}\' already exists...")
        raise HTTPException(status_code=409, detail=f"User \'{User.user_principal_name}\' already exists in table \'{USER_CONTAINER}\'")


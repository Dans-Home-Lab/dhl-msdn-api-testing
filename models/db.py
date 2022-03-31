from asyncio.windows_events import NULL
from fastapi import HTTPException
from pydantic import BaseModel
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
import config.config as config

HOST = config.settings['host']
MASTER_KEY = config.settings['master_key']
DATABASE_ID = config.settings['database_id']

dbclient = cosmos_client.CosmosClient(HOST,MASTER_KEY)

async def get_all_databases():
    print("Fetching all databases")
    try:
        databases = list(dbclient.list_databases())
        if not databases:
            return HTTPException(status_code=400, detail="No databases found")
        return databases
    except exceptions:
        return HTTPException(status_code=500, detail="Server error occured.")

async def get_database_path(id):
    print("Get a Database by id")

    try:
        database = dbclient.get_database_client(id)
        database.read()
        print('Database with id \'{0}\' was found, it\'s link is {1}'.format(id, database.database_link))
        return database.database_link

    except exceptions.CosmosResourceNotFoundError:
        print('A database with id \'{0}\' does not exist'.format(id))
        return NULL
        #from https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/cosmos/azure-cosmos/samples/database_management.py
        #Also see: https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/cosmos/azure-cosmos/samples/document_management.py#L41-L49

async def create_database(id):
    print('creating database by name: {0}'.format(id))
    try:
        dbclient.create_database(id=id)
        print('Database with id \'{0}\' created'.format(id))
        new_db_path = get_database_path(id)
        return new_db_path
    except exceptions.CosmosResourceExistsError:
        print('Database with id \'{0}\' already exists'.format(id))
        existing_db_path = get_database_path(id)
        return HTTPException(status_code=309, detail="Location: {0}".format(existing_db_path))

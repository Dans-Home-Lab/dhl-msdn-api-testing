from asyncio.windows_events import NULL
from fastapi import HTTPException
from pydantic import BaseModel
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import config.config as config

HOST = config.settings['host']
MASTER_KEY = config.settings['master_key']
DATABASE_ID = config.settings['database_id']

dbclient = cosmos_client.CosmosClient(HOST,MASTER_KEY)

#GET: /dbs
async def get_all_databases():
    print("Fetching all databases")
    try:
        databases = list(dbclient.list_databases())
        if not databases:
            return HTTPException(status_code=400, detail="No databases found")
        return databases
    except exceptions:
        return HTTPException(status_code=500, detail="Server error occured.")

#GET: /db/{id}
async def get_database_path(id):
    print("Get a Database by id")

    try:
        database = dbclient.get_database_client(id)
        database.read()
        print('Database with id \'{0}\' was found, it\'s link is {1}'.format(id, database.database_link))
        #this returns the wrong link. dbs/test instead of db/test (singular vs plural)
        return database.database_link
        

    except exceptions.CosmosResourceNotFoundError:
        print('A database with id \'{0}\' does not exist'.format(id))
        return  HTTPException(status_code=404, detail=f"No database {id} found")
        #from https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/cosmos/azure-cosmos/samples/database_management.py
        #Also see: https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/cosmos/azure-cosmos/samples/document_management.py#L41-L49

async def get_database(id):
    print('Return a database object by id: {0}'.format(id))
    try:
        database = dbclient.get_database_client(id)

    except exceptions.CosmosResourceNotFoundError:
        return HTTPException(status_code=404, detail="No containers found")

#POST: /db/{id}
async def create_database(id):
    print('creating database by name: {0}'.format(id))
    try:
        dbclient.create_database_if_not_exists(id)
        print('Database with id \'{0}\' created'.format(id))
        database_url = '/db/{0}'.format(id)
        return database_url

    except exceptions.CosmosResourceExistsError:
        print('Database with id \'{0}\' already exists'.format(id))
        existing_db_path = get_database_path(id)
        return HTTPException(status_code=309, detail="Location: {0}".format(existing_db_path))

#POST: /db/{db}/container/{id}
async def create_container(db,id):
    partition_key = PartitionKey(path='/id', kind='Hash')
    print('Creating container in database: {0} with id: {1}'.format(db,id))

    try:
        database = dbclient.get_database_client(db)
        database.create_container(id=id, partition_key=partition_key)
        print('Container with id \'{0}\' created'.format(id))

    except exceptions.CosmosResourceExistsError:
        print('A container with id \'{0}\' already exists in database \'{1}\''.format(id,db))
        raise HTTPException(status_code=409, detail=f"Container {id} already exists in database {db}")

    except exceptions.CosmosResourceNotFoundError:
        print('A database with name \'{0}\' was not found'.format(db))
        raise HTTPException(status_code=404, detail=f"No database {db} found")

    return (f'/db/{db}/container/{id}')

#GET: /db/{db}/containers
async def list_containers(db):
    try:
        #Get db based on id, don't just pass a string
        database = dbclient.get_database_client(db)
        print('Containers:')
        containers = list(database.list_containers())
        for container in containers:
            print(container['id'])

    except exceptions.CosmosResourceNotFoundError:
        print('No containers found')
        raise HTTPException(status_code=404, detail="No containers found")
    
    return containers

#GET: /db/{db}/container/{id}
async def get_container(db,id):
    print('Trying container \'{0}\' in database \'{1}\'.'.format(id,db))
    try:
        container_client = dbclient.get_database_client(db)
        container = container_client.get_container_client(id)
        container.read
        return container._get_properties()

    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail='No container \'{0}\' found in database \'{1}\''.format(id,db))

async def get_item_by_id(container, id):
    print('Getting item by id \'{0}\''.format(id))
    #https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/cosmos/azure-cosmos/samples/document_management.py#L46-L54
    #or https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/cosmos/azure-cosmos/samples/document_management.py#L71-L83
    response = container.read_item(item=id, partition_key=id)
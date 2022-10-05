from asyncio.windows_events import NULL
from logging import exception
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
        raise  HTTPException(status_code=404, detail=f"No database {id} found")

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

#GET: /db/{db}/container/{container_name}/item/{item_number}
async def get_item_by_id(db, container_id, id):
    print('Getting item by id \'{0}\''.format(id))
    try:
        container_client = dbclient.get_database_client(db)
        container = container_client.get_container_client(container_id)
        item = container.read_item(item=id, partition_key=id)
        print('Retrieved item by id \'{0}\'. Its name is: \'{1}\''.format(id, item['name']))
        return item
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail='No item found \'{0}\' in container \'{1}\' in database \'{2}\''.format(id, container_id, db))

#GET: /db/{db}/container/{container_name}/items?column_name=name&column_value=value
async def get_item_by_column(db, container_id, column_name, column_value):
    print(f'Getting item where {column_name} is {column_value}')
    try:
        container_client = dbclient.get_database_client(db)
        container = container_client.get_container_client(container_id)
        items = list(container.query_items(
            query = f'SELECT * FROM r WHERE r.{column_name} = @column_value',
            parameters=[
            {"name":"@column_value", "value": column_value}
            ],enable_cross_partition_query=True
        ))
        if len(items) != 0:
            return items
        else:
            raise HTTPException(status_code=404, detail='No item found in container \'{0}\' matching conditions.'.format(container_id))

    except:
        print(exception)
        raise HTTPException(status_code=500, detail='Server error when querying container \'{0}\' matching conditions.'.format(container_id))
        
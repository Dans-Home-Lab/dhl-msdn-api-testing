from asyncio.windows_events import NULL
from pydantic import BaseModel
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
import config.config as config

HOST = config.settings['host']
MASTER_KEY = config.settings['master_key']
DATABASE_ID = config.settings['database_id']

dbclient = cosmos_client.CosmosClient(HOST,MASTER_KEY)

async def get_database(id):
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
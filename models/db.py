from pydantic import BaseModel
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from .. import config

HOST = config.settings['host']
MASTER_KEY = config.settings['master_key']
DATABASE_ID = config.settings['database_id']

def read_database(client, id):
    print("\n3. Get a Database by id")

    try:
        database = client.get_database_client(id)
        database.read()
        print('Database with id \'{0}\' was found, it\'s link is {1}'.format(id, database.database_link))

    except exceptions.CosmosResourceNotFoundError:
        print('A database with id \'{0}\' does not exist'.format(id))
        #from https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/cosmos/azure-cosmos/samples/database_management.py
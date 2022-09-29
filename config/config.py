import os

settings = {
    'host': os.environ.get('DWAAS_API_ACCOUNT_HOST'),
    'master_key': os.environ.get('DWAAS_API_ACCOUNT_KEY'),
    'read_key': os.environ.get('DWAAS_API_READ_KEY'),
    'database_id': os.environ.get('DWAAS_API_COSMOS_DATABASE'),
    'container_id': os.environ.get('DWAAS_API_COSMOS_CONTAINER')
}
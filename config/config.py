import os

settings = {
    'host': os.environ.get('DHL-API-ACCOUNT_HOST', '[]'),
    'master_key': os.environ.get('DHL-API-ACCOUNT_KEY'),
    'database_id': os.environ.get('DHL-API-COSMOS_DATABASE'),
    'container_id': os.environ.get('DHL-API-COSMOS_CONTAINER')
}
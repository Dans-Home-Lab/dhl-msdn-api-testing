import os

settings = {
    'host': os.environ.get('DWAAS-API-ACCOUNT-HOST',),
    'master_key': os.environ.get('DWAAS-API-ACCOUNT-KEY'),
    'database_id': os.environ.get('DWAAS-API-COSMOS-DATABASE'),
    'container_id': os.environ.get('DWAAS-API-COSMOS-CONTAINER')
}
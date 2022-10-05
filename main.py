from asyncio.windows_events import NULL
from urllib import response
from fastapi import FastAPI, Response, HTTPException
from pydantic import BaseModel
from models import db as DB
#from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

#Some static elements first. Not really part of the API but this is also where we can store the openapi spec.
#To Do: Use 'from fastapi.staticfiles import StaticFiles; ... app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/")
async def root():
    try:
        file = open("./static/index.html")
        indexfile = Response(content=file.read(), media_type="text/html")
    finally:
        file.close
        return indexfile

@app.get("/static/theme.css")
async def theme():
    try:
        file = open("./static/theme.css")
        theme_css = Response(content=file.read(), media_type="text/css")
    finally:
        file.close
        return theme_css
#End Static Region

@app.get("/dbs")
async def get_all_databases():
    databases = await DB.get_all_databases()
    return databases


@app.get("/db/{id}")
async def get_database(id):
    db_result = await DB.get_database_path(id)
    if (db_result == NULL):
        raise HTTPException(status_code=404, detail="Database {0} not found".format(id))
    return db_result

@app.post("/db/{id}")
async def create_database(id):
    db_result = await DB.create_database(id)
    return db_result

@app.post("/db/{db}/container/{id}")
async def create_container(db,id):
    db_result = await DB.create_container(db,id)
    return db_result

@app.get("/db/{db}/containers")
async def get_containers(db):
    containers = await DB.list_containers(db)
    return containers

@app.get("/db/{db}/container/{id}")
async def get_container(db,id):
    c_data = await DB.get_container(db,id)
    return c_data

@app.get("/db/{db}/container/{container_id}/item/{item_id}")
async def get_item(db,container_id,item_id):
    item = await DB.get_item_by_id(db,container_id,item_id)
    return item

#Uses query params 
#Strings added that aren't part of the path are treated as query parameters
#See: https://fastapi.tiangolo.com/tutorial/query-params/
@app.get("/db/{db}/container/{container_id}/items")
async def get_item_by_column(db,container_id,column_name: str = 'name', column_value: str = None):
    items = await DB.get_item_by_column(db,container_id,column_name,column_value)
    return items
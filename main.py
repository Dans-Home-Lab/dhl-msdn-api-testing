from asyncio.windows_events import NULL
from urllib import response
from fastapi import FastAPI, Response, HTTPException
from pydantic import BaseModel
from models import db as DB

app = FastAPI()

#Some static elements first. Not really part of the API but this is also where we can store the openapi spec.
@app.get("/")
async def root():
    try:
        file = open("./static/index.html")
        r = Response(content=file.read(), media_type="text/html")
    finally:
        file.close
        return r

@app.get("/static/theme.css")
async def theme():
    try:
        file = open("./static/theme.css")
        theme_css = Response(content=file.read(), media_type="text/css")
    finally:
        file.close
        return theme_css

@app.get("/dbs")
async def get_all_databases():
    databases = await DB.get_all_databases()
    return databases


@app.get("/db/{id}")
async def get_database(id):
    db_result = await DB.get_database_path(id)
    if (db_result == NULL):
        raise HTTPException(status_code=404, detail="Item not found")
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
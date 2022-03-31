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

@app.get("/db")
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
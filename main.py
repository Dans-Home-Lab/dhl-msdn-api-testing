from fastapi import FastAPI, Response
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
async def root():
    try:
        file = open("./static/theme.css")
        r = Response(content=file.read(), media_type="text/css")
    finally:
        file.close
        return r

    

@app.get("/vpc/{id}")
async def vpc_id(id):
    DB.read_database
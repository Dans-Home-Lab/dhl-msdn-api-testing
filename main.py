from fastapi import FastAPI, Response
from pydantic import BaseModel

app = FastAPI()

#Some static elements first. Not really part of the API but this is also where we can store the openapi spec.
@app.get("/")
async def root():
    file = open("./static/index.html")
    r = Response(content=file.read(), media_type="text/html")
    file.close
    return r

@app.get("/static/theme.css")
async def root():
    file = open("./static/theme.css")
    r = Response(content=file.read(), media_type="text/css")
    file.close
    return r

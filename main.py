from fastapi import FastAPI, Response
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def root():
    file = open("./static/index.html")
    return Response(content=file.read(), media_type="text/html")





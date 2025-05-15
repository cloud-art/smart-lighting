from fastapi import FastAPI,Query
from typing import Annotated
from pydantic import BaseModel,Field
import asyncio
app = FastAPI()

class LightingInfo(BaseModel):
    power:Annotated[int, Field(gt=10)]
    name:str 

class LightingRequst(BaseModel):
    power:Annotated[int, Field(gt=10)]
    name:str 

@app.get('/ping/{id}')
def ping(id:int,data: Annotated[LightingRequst, Query()])->LightingInfo:
    return LightingInfo(power=12,name='asd')

@app.websocket('/ws')
async def ws():
    for i in range(10):
        yield i
        await asyncio.sleep(.5)


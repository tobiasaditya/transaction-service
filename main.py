from fastapi import FastAPI
from pydantic.fields import Field
from pydantic.main import BaseModel
from pydantic.types import UUID1
from model.transaction import TransactionData
from datetime import datetime
from config.config import trx_collection
app = FastAPI()

class DefaultResponse(BaseModel):
    request_time:str
    status_code:str
    message:str

@app.post("/add_transaction",response_model=DefaultResponse)
async def add_transaction(trx_data:TransactionData):
    trx_data.requestTime = datetime.now()
    insert_trx = await trx_collection.insert_one(trx_data.dict())
    return {
        "request_time":str(datetime.now()),
        "status_code":200,
        "message":"Success added transaction"}
from fastapi import FastAPI
# from pydantic.fields import Field
from pydantic.main import BaseModel
# from pydantic.types import UUID1
from model.transaction import TransactionData
from datetime import datetime
from config.config import trx_collection
import logging

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


app = FastAPI()

class DefaultResponse(BaseModel):
    request_time:str
    status_code:str
    message:str

class DefaultResponseContent(BaseModel):
    request_time:str
    status_code:str
    message:str
    content:dict

@app.post("/add_transaction",response_model=DefaultResponse)
async def add_transaction(trx_data:TransactionData):
    trx_data.requestTime = datetime.now()
    insert_trx = await trx_collection.insert_one(trx_data.dict())
    return {
        "request_time":str(datetime.now()),
        "status_code":200,
        "message":"Success added transaction"}

@app.get("/transaction",response_model=DefaultResponseContent)
async def get_transaction():
    n_data = await trx_collection.count_documents({})
    if n_data ==0:
        all_trx = []
        status_code = 404
    else:
        all_trx = await trx_collection.find({},{"_id":0}).to_list(n_data)
        status_code = 200
    content = {
        "n_data":n_data,
        "datas":all_trx
        }
    return {
        "request_time":str(datetime.now()),
        "status_code":status_code,
        "message":"Success get transaction data",
        "content":content
    }
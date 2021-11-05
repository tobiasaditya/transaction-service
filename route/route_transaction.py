from fastapi import APIRouter

from model.model_response import DefaultResponse, DefaultResponseContent
from model.transaction import TransactionData

from config.config import trx_collection

from datetime import datetime
import uuid


router_transaction = APIRouter()

@router_transaction.post("/add",response_model=DefaultResponse)
async def add_transaction(trx_data:TransactionData):
    trx_data.requestTime = datetime.now()
    trx_data.trxId = str(uuid.uuid4())
    insert_trx = await trx_collection.insert_one(trx_data.dict())
    return {
        "request_time":str(datetime.now()),
        "status_code":200,
        "message":"Success added transaction"}

@router_transaction.get("/get",response_model=DefaultResponseContent)
async def get_transaction():
    n_data = await trx_collection.count_documents({})
    if n_data ==0:
        all_trx = []
        status_code = 404
    else:
        all_trx = await trx_collection.find({},{"_id":0}).to_list(n_data)
        total_income = 0
        total_purchase = 0
        for trx in all_trx:
            if trx['trxType'] == "PURCHASE":
                total_purchase+=int(trx['amount'])
            elif trx['trxType'] == "INCOME":
                total_income+=int(trx['amount'])


        status_code = 200

    content = {
        "n_data":n_data,
        "total_purchase":(total_purchase),
        "total_income":(total_income),
        "total_net":(total_income-total_purchase),
        "datas":all_trx
        }

    return {
        "request_time":str(datetime.now()),
        "status_code":status_code,
        "message":"Success get transaction data",
        "content":content
    }
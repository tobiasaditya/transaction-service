from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter
from enum_model.enum_transaction import trxMethodEnum,trxTypeEnum

from model.model_response import DefaultResponse, DefaultResponseContent
from model.transaction import TransactionData, TransactionDataShow, TransactionFilter

from config.config import trx_collection

from util.util_datetime import datetime_jakarta
import uuid


router_transaction = APIRouter()

@router_transaction.post("/add",response_model=DefaultResponse)
async def add_transaction(trx_data:TransactionData):
    request_time = datetime_jakarta()
    trx_data.requestTime = request_time
    trx_data.trxId = str(uuid.uuid4())
    insert_trx = await trx_collection.insert_one(trx_data.dict())
    return {
        "request_time":str(request_time),
        "status_code":200,
        "message":"Success added transaction"}

@router_transaction.get("/get",response_model=DefaultResponseContent)
async def get_transaction(
    startDate : Optional[str] = None,
    endDate : Optional[str] = None,
    trxType : Optional[trxTypeEnum] = None,
    trxMethod : Optional[trxMethodEnum] = None):

    filter = {}

    if startDate and endDate:
        startDate = datetime.strptime(startDate,"%d/%m/%Y")
        endDate = datetime.strptime(endDate,"%d/%m/%Y")
        filter['requestTime'] = {
            "$gte": startDate,
            "$lt": endDate+timedelta(days=1)
        }

    if trxType:
        filter['trxType'] = trxType
    
    if trxMethod:
        filter['trxMethod'] = trxMethod

    n_data = await trx_collection.count_documents(filter)
    total_income = 0
    total_purchase = 0
    if n_data ==0:
        all_trx = []
        status_code = 404
    else:
        all_trx = await trx_collection.find(filter).to_list(n_data)
        
        for trx in all_trx:
            if trx['trxType'] == "PURCHASE":
                total_purchase+=int(trx['amount'])
            elif trx['trxType'] == "INCOME":
                total_income+=int(trx['amount'])


        status_code = 200
    

    data = TransactionDataShow(content = all_trx)
    data.n_data = n_data
    data.total_income = total_income
    data.total_purchase = total_purchase
    data.total_net = total_income - total_purchase

    return {
        "request_time":str(datetime_jakarta()),
        "status_code":status_code,
        "message":"Success get transaction data",
        "content":data.dict()
    }
from pydantic import BaseModel

class TransactionData(BaseModel):
    requestTime:str = None
    trxType:str
    amount:str
    desc:str
    trxMethod:str
    trxId:str
from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from bson import ObjectId
import json
class ObjectStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):    
        if not v:
            return v            
        return str(v)

class TransactionData(BaseModel):
    trxType:str
    amount:str
    desc:str
    trxMethod:str
    requestTime:datetime = None
    trxId:str = None

class TransactionDataDb(TransactionData):
    id:ObjectStr = Field(... , alias="_id")
    requestTime : ObjectStr = None

class TransactionDataShow(BaseModel):
    n_data : int = None
    total_puchase : int = None
    total_income  : int = None
    total_net : int = None
    content :List[TransactionDataDb] = []
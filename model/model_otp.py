from pydantic import BaseModel
from datetime import datetime

class OtpBase(BaseModel):
    otpValue:str = None
    otpExpired:datetime = None
    otpReceiver:str = None
    otpVerifed:bool = False
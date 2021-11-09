from pydantic.main import BaseModel


class DefaultResponse(BaseModel):
    request_time:str
    status_code:int
    message:str

class DefaultResponseContent(BaseModel):
    request_time:str = None
    status_code:int = None
    message:str = None
    content:dict  = None
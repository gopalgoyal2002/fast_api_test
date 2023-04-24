from pydantic import BaseModel

class askquestion(BaseModel):
    quesiton:str
    index:str
    topk:int
    threshold:int

class askfromgpt(BaseModel):
    quesiton:str
    index:str
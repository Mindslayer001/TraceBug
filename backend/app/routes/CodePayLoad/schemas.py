from pydantic import BaseModel

class CodePayLoadIn(BaseModel):
    code: str

class CodePayLoadOut(BaseModel):
    code: str
    length: int
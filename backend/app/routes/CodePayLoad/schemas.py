from typing import Optional
from pydantic import BaseModel

class CodePayLoadIn(BaseModel):
    code: str

class CodePayLoadOut(BaseModel):
    code: str
    length: int
    message: Optional[str] = None
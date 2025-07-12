from pydantic import BaseModel

class HealthOut(BaseModel):
    message: str
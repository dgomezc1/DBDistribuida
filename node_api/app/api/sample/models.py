from pydantic import Field
from pydantic import BaseModel

class User(BaseModel):
    username: str = Field(...)

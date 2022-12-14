from typing import Union

from pydantic import Field, BaseModel

available_types = Union[str, dict, list, int, float, bool]

class Base(BaseModel):
    key: str = Field(
        ...,
        description="Key of value",
        min_length=1,
        example='key_name'
    )

class Read(Base):
    pass

class Write(Base):
    value: available_types = Field(
        ...,
        description="Value to be save"
    )

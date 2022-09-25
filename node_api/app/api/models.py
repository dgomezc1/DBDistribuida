from typing import Literal, Union

from pydantic import Field, BaseModel

available_types = Union[str, dict, list, int, float, bool]

class Replication(BaseModel):
    replication_url: str = Field(default="")
    is_restore: bool = Field(default=False)
    node_url: str = Field(default="")
    insert_type: Literal[0,1] = Field(default=0)

class Base(Replication):
    key: str = Field(
        ...,
        description="Key of value",
        min_length=1,
        max_length=40,
        example='99800b85d3383e3a2fb45eb7d0066a4879a9dad0'
    )

class Read(Base):
    pass

class Write(Base):
    value: available_types = Field(
        ...,
        description="Value to be save"
    )

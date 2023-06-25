from typing import Optional, List

from orjson import orjson
from pydantic import BaseModel, Field


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Xls24dNftTypeAttribute(BaseModel):
    trait_type: str
    description: Optional[str]
    value: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson.dumps


class Xls24dNftType(BaseModel):
    """
    The Filegr NFT Type. For now we will use the art.v0 and use the open graph image as image part which is mandatory
    """
    schema_: str = Field(
        default="ipfs://QmNpi8rcXEkohca8iXu7zysKKSJYqCvBJn3xJwga8jXqWU",
        alias='schema')
    nft_type: str = Field(
        default="art.v0",
        alias="nftType")
    name: str
    description: str
    image: str
    file: Optional[str]
    attributes: Optional[List[Xls24dNftTypeAttribute]]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        # allow_population_by_field_name = True
        # fields = {
        #     'schema_': 'schema'
        # }

    def add_attribute(self,
                      trait_type: str,
                      value: str,
                      description: Optional[str]
                      ):
        if self.attributes is None:
            self.attributes = []

        self.attributes.append(
            Xls24dNftTypeAttribute(trait_type=trait_type,
                                   description=description,
                                   value=value)
        )

from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class MemoFormat(Enum):
    PDF = 'pdf'
    TXT = 'txt'
    CSV = 'csv'
    JSON = 'json'
    YAML = 'yaml'
    PNG = 'img/png'
    JPEG = 'img/jpeg'
    JPG = 'img/jpg'
    WEBP = 'img/webp'
    ZIP = 'zip'
    GZ = 'gz'


class MyMemo(BaseModel):
    memo: str
    memo_format: MemoFormat
    memo_type: Optional[str]


class MyMemos(BaseModel):
    __root__: List[MyMemo]

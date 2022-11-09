from __future__ import annotations
from pathlib import Path
from typing import Type
import os


class MyFileIO:

    @classmethod
    def create_dir(cls: Type[MyFileIO], path: str, recursive: bool = False) -> bool:
        folder_path = Path(path)
        if not folder_path.exists():
            if recursive:
                os.makedirs(path)
            else:
                os.mkdir(path)
        return True

    @classmethod
    def write_to_file(cls: Type[MyFileIO], path: str, content: str, overwrite: bool = True) -> bool:
        file = open(path, "w")
        try:
            file.write(content)
            return True
        finally:
            if file:
                file.close()

    @classmethod
    def read_from_file(cls: Type[MyFileIO], path: str) -> str:
        file = open(path, "r")
        try:
            content = file.read()
            return content
        finally:
            file.close()

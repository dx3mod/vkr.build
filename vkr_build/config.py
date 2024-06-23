import tomllib
from pathlib import Path
from sys import stderr

from pydantic import BaseModel, Field


class DocumentConfiguration(BaseModel):
    chapter_prefix: str = Field(default="Глава ")
    toc_title: str = Field(default="Оглавление")

    files: list[Path]
    output: Path = Field(default=Path("output.pdf"))

    css: Path = Field(default=Path("custom.css"))


def read_config(path: Path) -> DocumentConfiguration:
    try:
        with open(path, "rb") as config_file:
            contents = tomllib.load(config_file)
            return DocumentConfiguration.model_validate(contents)
    except FileNotFoundError:
        print(f"Не удалось найти конфигурационный файл '{path}'!", file=stderr)

    exit(1)

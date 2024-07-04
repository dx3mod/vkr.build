import tomllib
from pathlib import Path
from sys import stderr

from pydantic import BaseModel, Field


class DocumentConfiguration(BaseModel):
    class TableOfContents(BaseModel):
        title: str = Field(default="Оглавление")

    class Chapter(BaseModel):
        prefix: str = Field(default="Глава")

    toc: TableOfContents = Field(default=TableOfContents())
    chapter: Chapter = Field(default=Chapter())

    files: list[Path] = Field(default=[])
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

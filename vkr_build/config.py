import tomllib
from pathlib import Path
from sys import stderr

from pydantic import BaseModel, Field


class DocumentConfiguration(BaseModel):
    start_page: int = Field(default=2)
    chapter_prefix: str = Field(default="Глава ")
    font_mono: str = Field(default="monospace")
    avoid_figure: bool = Field(default=True)
    toc_title: str = Field(default="Оглавление")

    files: list[Path]
    output: Path = Field(default=Path("output.pdf"))

    css: Path | None = Field(default=None)


def read_config(path: Path) -> DocumentConfiguration:
    try:
        with open(path, "rb") as config_file:
            contents = tomllib.load(config_file)
            return DocumentConfiguration.model_validate(contents)
    except FileNotFoundError:
        print(f"Не удалось найти конфигурационный файл '{path}'!", file=stderr)

    exit(1)

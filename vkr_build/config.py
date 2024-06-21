from pathlib import Path
from sys import stderr
from pydantic import BaseModel, Field
import tomllib


class DocumentConfiguration(BaseModel):
    start_page: int = Field(default=2)
    chapter_prefix: str = Field(default="Глава ")
    font_mono: str = Field(default="monospace")
    avoid_figure: bool = Field(default=True)


def read_config(path: Path) -> DocumentConfiguration:
    try:
        with open(path, "rb") as config_file:
            contents = tomllib.load(config_file)
            return DocumentConfiguration.model_validate(contents)
    except FileNotFoundError:
        print(f"Не удалось найти конфигурационный файл '{path}'!", file=stderr)

    exit(1)

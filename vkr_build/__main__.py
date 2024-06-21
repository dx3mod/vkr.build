from pathlib import Path
from typing import Annotated
import typer

from vkr_build.config import read_config


def main(
    config_path: Annotated[
        Path, typer.Option(help="Путь до файла конфигурации.")
    ] = Path("document.toml")
):
    config = read_config(config_path)
    print(f"{config_path} {config}")


if __name__ == "__main__":
    typer.run(main)

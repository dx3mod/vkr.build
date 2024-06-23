import logging
import multiprocessing
from pathlib import Path
from sys import stderr
import sys
from typing import Annotated

import pydantic
import pypandoc
import typer
import weasyprint
from bs4 import Stylesheet
from vkr_build.config import read_config
from vkr_build.document_builder import DocumentBuilder


def read_file(entry: Path):
    if entry.suffix in (".html", ".md"):
        print("[READ]", entry)

        with open(entry, "r") as file:
            return file.read()
    return ""


def read_files(filenames: list[Path]):
    """Читает HTML/Markdown файлы в одну HTML-строку."""

    raw_sources = map(read_file, filenames)

    return pypandoc.convert_text(
        "\n\n".join(raw_sources),
        "html",
        format="markdown+smart",
        extra_args=["-V", "lang=ru"],
    )


def main(
    config_path: Annotated[
        Path, typer.Option(help="Путь до файла конфигурации.")
    ] = Path("document.toml")
):
    try:
        config = read_config(config_path)

        source = read_files(config.files)

        document = DocumentBuilder(source, config=config)
        document_html = document.build()

        html = weasyprint.HTML(
            string=str(document_html),
            base_url=".",
            encoding="utf-8",
            url_fetcher=weasyprint.default_url_fetcher,
        )

        stylesheets = []

        if config.css.exists():
            print("[CSS]", config.css)
            stylesheets.append(weasyprint.CSS(filename=config.css))

        logger = logging.getLogger("weasyprint")
        logger.addHandler(logging.StreamHandler(sys.stdout))

        print("[WEASYPRINT]", config.output)
        html.write_pdf(config.output, stylesheets=stylesheets)

        exit(0)

    except pydantic.ValidationError as error:
        print(error.json(indent=2), file=stderr)

    exit(1)


def run():
    typer.run(main)

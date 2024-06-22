import multiprocessing
from pathlib import Path
from sys import stderr
from typing import Annotated
import pydantic
import pypandoc
import typer
import weasyprint

from vkr_build.config import read_config
from vkr_build.document_builder import DocumentBuilder


def read_file(entry: Path):
    if entry.suffix in (".html", ".md"):
        print("[RENDER]", entry)

        with open(entry, "r") as file:
            return file.read()
    return ""


def read_files(filenames: list[Path]):
    """Читает HTML/Markdown файлы в одну HTML-строку."""

    with multiprocessing.Pool(processes=4) as pool:
        results = pool.map(read_file, filenames)
        raw_source = "\n\n".join(results)

    return pypandoc.convert_text(raw_source, "html", format="md")


def main(
    config_path: Annotated[
        Path, typer.Option(help="Путь до файла конфигурации.")
    ] = Path("document.toml")
):
    try:
        config = read_config(config_path)

        source = read_files(config.files)

        document = DocumentBuilder(source)
        document_html = document.build()

        html = weasyprint.HTML(
            string=str(document_html),
            base_url=".",
            encoding="utf-8",
            url_fetcher=weasyprint.default_url_fetcher,
        )

        print("[WEASYPRINT] output.pdf")
        html.write_pdf("output.pdf")

        exit(0)

    except pydantic.ValidationError as error:
        print(error.json(indent=2), file=stderr)

    exit(1)


def run():
    typer.run(main)

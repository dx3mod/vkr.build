import argparse
import logging
import sys
import time
from pathlib import Path

import pydantic
import pypandoc
import weasyprint

from vkr_build.config import read_config
from vkr_build.document_builder import DocumentBuilder


def read_file(entry: Path):
    if entry.suffix in (".html", ".md"):
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


cli_parser = argparse.ArgumentParser(
    prog="vkr-build",
    description="Автоматизированное решение вёрстки курсовых/дипломных работ.",
)

cli_parser.add_argument(
    "-c", "--config-path", dest="config_path", type=Path, default=Path("document.toml")
)


def run():
    args = cli_parser.parse_args()

    try:
        config = read_config(args.config_path)

        print("Файлы:")
        for filename in config.files:
            print(" ", filename)

        # Чтение файлов

        reading_files_time = time.time()
        print("Конвертация файлов... ", end="")
        sys.stdout.flush()

        source = read_files(config.files)

        print(time.time() - reading_files_time, "секунд")

        # Процессинг файлов

        document_processing_time = time.time()
        print("Процессинг документа... ", end="")
        sys.stdout.flush()

        document = DocumentBuilder(source, config=config)
        document_html = document.build()

        print(time.time() - document_processing_time, "секунд")

        # Генерация PDF-файла

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

        print("Output:", config.output)

        start_weasyprint_time = time.time()
        html.write_pdf(config.output, stylesheets=stylesheets)

        print(
            "Время компиляции PDF-документа заняло",
            time.time() - start_weasyprint_time,
            "секунд.",
        )

        exit(0)

    except pydantic.ValidationError as error:
        print(error.json(indent=2), file=sys.stderr)

    exit(1)

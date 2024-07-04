import logging
import os
import sys
import time
from pathlib import Path

import pydantic
import pypandoc
import weasyprint

from vkr_build.config import read_config
from vkr_build.document_builder import DocumentBuilder
from vkr_build.preprocess_stages.images import ImagesPreprocessStage
from vkr_build.validators.toc import TableOfContentsValidator
from vkr_build.validators.validator import DocumentValidator

from .cli import cli_parser

VALIDATORS = [TableOfContentsValidator()]


def search_files(root: Path):
    return sorted(
        map(
            Path,
            filter(
                lambda filename: filename.endswith(".md") or filename.endswith(".html"),
                os.listdir(root),
            ),
        )
    )


def collect_files_to_html(filenames: list[Path]):
    """Читает HTML/Markdown файлы в одну HTML-строку."""

    def read_file(entry: Path):
        if entry.suffix in (".html", ".md"):
            with open(entry, "r") as file:
                return file.read()
        return ""

    raw_sources = map(read_file, filenames)

    return pypandoc.convert_text(
        "\n\n".join(raw_sources),
        "html",
        format="markdown+smart",
        extra_args=["-V", "lang=ru", "--no-highlight"],
    )


def run():
    args = cli_parser.parse_args()

    try:
        config = read_config(args.config_path)

        filenames = config.files or search_files(Path("."))

        print("Файлы:")
        for filename in filenames:
            print(" ", filename)

        print()

        # Чтение файлов

        reading_files_time = time.time()
        print("Конвертация файлов... ", end="")
        sys.stdout.flush()

        source_html = collect_files_to_html(filenames)

        print(time.time() - reading_files_time, "секунд")

        # Процессинг файлов

        document_processing_time = time.time()
        print("Процессинг документа... ", end="")
        sys.stdout.flush()

        document = DocumentBuilder(source_html, config=config)
        document.add_preprocess_stage(ImagesPreprocessStage())

        document_soup = document.build()

        print(time.time() - document_processing_time, "секунд")

        # Валидация

        print()
        print("Ошибки:")

        for validator in VALIDATORS:
            messages = validator.validate(
                DocumentValidator.Document(
                    soup=document_soup, table_of_contents=document.table_of_contents
                )
            )

            for message in messages:
                print(" ", message)

        print("  ...")
        print()

        # Компиляция

        if args.validate_only:
            return

        stylesheets = []

        if config.css.exists():
            print("Использованы стили:", config.css)
            stylesheets.append(weasyprint.CSS(filename=config.css))

        logger = logging.getLogger("weasyprint")
        logger.addHandler(logging.StreamHandler(sys.stdout))

        print("Файл сохранён по пути:", config.output)

        start_weasyprint_time = time.time()

        html = weasyprint.HTML(
            string=str(document_soup),
            base_url=".",
            encoding="utf-8",
            url_fetcher=weasyprint.default_url_fetcher,
        )

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

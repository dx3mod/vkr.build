from abc import ABC, abstractmethod
from typing import NamedTuple

from bs4 import BeautifulSoup

from vkr_build.toc import TableOfContents


class DocumentValidator(ABC):
    class Document(NamedTuple):
        soup: BeautifulSoup
        table_of_contents: TableOfContents

    @abstractmethod
    def validate(self, document: Document) -> list[str]: ...


class DocumentValidationErrors(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

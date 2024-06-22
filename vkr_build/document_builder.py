import os
from pathlib import Path
from typing import Collection
from bs4 import BeautifulSoup, Tag
from pydantic import BaseModel

from vkr_build.utils import STYLES_PATH


class Header(BaseModel):
    title: str
    header_id: str


class SubSection(Header):
    pass


class Section(Header):
    subsections: list[SubSection]


class Chapter(Header):
    numbering: bool
    sections: list[Section]


class TableOfContents:
    def __init__(self) -> None:
        self._chapters: list[Chapter] = []

    def add_chapter(self, title: str, id: str, numbering: bool):
        self._chapters.append(
            Chapter(title=title, header_id=id, sections=[], numbering=numbering)
        )

    def add_section(self, title: str, id: str):
        self._chapters[-1].sections.append(
            Section(title=title, header_id=id, subsections=[])
        )

    def add_subsection(self, title: str, id: str):
        self._chapters[-1].sections[-1].subsections.append(
            SubSection(
                title=title,
                header_id=id,
            )
        )


class DocumentBuilder:
    def __init__(self, /, source: str) -> None:
        self._content_html = BeautifulSoup(source, "html.parser")
        self._toc = TableOfContents()

    def build(self):
        self._build_toc()
        self._preprocess_images()

        page = BeautifulSoup()

        page.head.append(  # type: ignore
            page.new_tag(
                "link", rel="stylesheet", href=str(STYLES_PATH.joinpath("vkr.css"))
            )
        )

        page.head.append(page.new_tag("meta", charset="UTF-8"))  # type: ignore

        toc_header = page.new_tag(
            "h1", attrs={"id": "оглавление", "class": "non-numbering"}
        )
        toc_header.append("Оглавление")

        page.body.append(toc_header)  # type: ignore

        page.body.append(self._content_html)  # type: ignore

        return page

    def _build_toc(self):
        for header in self._content_html.select("h1, h2, h3"):

            title = header.text.strip()
            classes = header.get("class") or ""

            header.attrs["id"] = title.lower().replace(" ", "-")
            header_id = header.attrs["id"]

            match header.name:
                case "h1":
                    self._toc.add_chapter(
                        title, header_id, "non-numbering" not in classes
                    )
                case "h2":
                    self._toc.add_section(title, header_id)
                case "h3":
                    self._toc.add_subsection(title, header_id)

            if not header.has_key("class"):
                header["class"] = ""

    def _preprocess_images(self):
        for image_tag in self._content_html.select("img"):
            image_tag["style"] = image_tag.get("style") or ""

            if image_tag.has_attr("width"):
                width = image_tag.attrs["width"]
                width = f"{width}px" if not width.endswith(("px", "%")) else width

                image_tag["style"] += f"width: {width};"

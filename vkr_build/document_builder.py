from bs4 import BeautifulSoup

from vkr_build.config import DocumentConfiguration
from vkr_build.toc import TableOfContents
from vkr_build.utils import STYLES_PATH


class DocumentBuilder:
    def __init__(self, /, source: str, config: DocumentConfiguration):
        self._content_html = BeautifulSoup(source, "html.parser")
        self._config = config

        self._toc = TableOfContents()

        self._chapter_counter = 1
        self._appendix_counter = 1

        self._section_counter = 1
        self._subsection_counter = 1

        self._numbering = True

    def build(self):
        self._preprocess_headers()
        self._preprocess_images()

        page = BeautifulSoup()

        # Head

        page.head.append(page.new_tag("meta", charset="UTF-8"))  # type: ignore
        page.head.append(  # type: ignore
            page.new_tag(
                "link", rel="stylesheet", href=str(STYLES_PATH.joinpath("vkr.css"))
            )
        )

        # Оглавление

        toc_title = page.new_tag("h1", attrs={"id": "оглавление"})
        toc_title.append(self._config.toc_title)

        page.body.append(toc_title)  # type: ignore

        toc_ul = self._render_toc(page)
        page.body.append(toc_ul)  # type: ignore

        # Тело

        page.body.append(self._content_html)  # type: ignore

        return page

    def _preprocess_headers(self):
        for header in self._content_html.select("h1, h2, h3"):
            title = header.text.strip()
            classes = header.get("class") or ""

            if header.name == "h1":
                self._numbering = "non-numbering" not in classes

            match header.name:
                case "h1":
                    self._reset_section_counter()

                    if "appendix" in classes:
                        title = (
                            f"Приложение {chr(64 + self._appendix_counter)}. {title}"
                        )
                        self._appendix_counter += 1
                    elif self._numbering:
                        title = f"{self._config.chapter_prefix} {self._chapter_counter}. {title}"
                        self._chapter_counter += 1
                case "h2":
                    self._subsection_counter = 1

                    if self._numbering:
                        title = f"{self._chapter_counter - 1}.{self._section_counter} {title}"
                        self._section_counter += 1
                case "h3":
                    if self._numbering:
                        title = f"{self._chapter_counter - 1}.{self._section_counter- 1}.{self._subsection_counter} {title}"

            header.attrs["id"] = title.lower().replace(" ", "-")
            header_id = header.attrs["id"]

            header.string = title

            match header.name:
                case "h1":
                    self._toc.add_chapter(title, header_id)
                case "h2":
                    self._toc.add_section(title, header_id)
                case "h3":
                    self._toc.add_subsection(title, header_id)

    def _reset_section_counter(self):
        self._section_counter = 1
        self._subsection_counter = 1

    def _preprocess_images(self):
        for image_tag in self._content_html.select("img"):
            image_tag["style"] = image_tag.get("style") or ""

            if image_tag.has_attr("width"):
                width = image_tag.attrs["width"]
                width = f"{width}px" if not width.endswith(("px", "%")) else width

                image_tag["style"] += f"width: {width};"

    def _render_toc(self, page: BeautifulSoup):
        toc_ul = page.new_tag("ul")

        def new_li_a_tag(title: str, header_id: str, /, bold=False):
            li = page.new_tag("li")
            a = page.new_tag("a", attrs={"href": f"#{header_id}"})

            if bold:
                b = page.new_tag("b")
                b.append(title)
                a.append(b)
            else:
                a.append(title)

            li.append(a)

            return li

        for chapter in self._toc.chapters:
            chapter_li = new_li_a_tag(chapter.title, chapter.header_id, bold=True)

            section_ul = page.new_tag("ul")
            for section in chapter.sections:
                section_li = new_li_a_tag(section.title, section.header_id)

                subsection_ul = page.new_tag("ul")
                for subsection in section.subsections:
                    subsection_ul.append(
                        new_li_a_tag(subsection.title, subsection.header_id)
                    )

                section_li.append(subsection_ul)
                section_ul.append(section_li)

            chapter_li.append(section_ul)
            toc_ul.append(chapter_li)

        return toc_ul

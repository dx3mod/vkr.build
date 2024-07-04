from bs4 import BeautifulSoup

from vkr_build.preprocess_stages.stage import PreprocessStage
from vkr_build.toc import TableOfContents

NON_NUMBERING_TITLES = [
    "Введение",
    "Заключение",
    "Список литературы",
    "Список источников",
    "Список использованных источников",
    "Список использованных\nисточников",
]


class NumberingPreprocessStage(PreprocessStage):
    def __init__(self, /, chapter_prefix: str) -> None:
        self._chapter_prefix = chapter_prefix.strip() + " "

        self._chapter_counter = 1
        self._appendix_counter = 1

        self._section_counter = 1
        self._subsection_counter = 1

        self._numbering = True
        self.toc = TableOfContents()

    def process(self, soup: BeautifulSoup):
        for header in soup.select("h1, h2, h3"):
            title = header.text.strip()
            classes = header.get("class") or ""

            if header.name == "h1":
                if title in NON_NUMBERING_TITLES:
                    self._numbering = False
                else:
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
                        title = (
                            f"{self._chapter_prefix}{self._chapter_counter}. {title}"
                        )
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
                    self.toc.add_chapter(title, header_id)
                case "h2":
                    self.toc.add_section(title, header_id)
                case "h3":
                    self.toc.add_subsection(title, header_id)

    def _reset_section_counter(self):
        self._section_counter = 1
        self._subsection_counter = 1

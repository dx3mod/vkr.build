from pydantic import BaseModel


class Header(BaseModel):
    title: str
    header_id: str


class SubSection(Header):
    pass


class Section(Header):
    subsections: list[SubSection]


class Chapter(Header):
    sections: list[Section]


class TableOfContents:
    def __init__(self) -> None:
        self.chapters: list[Chapter] = []

    def add_chapter(self, title: str, id: str):
        self.chapters.append(Chapter(title=title, header_id=id, sections=[]))

    def add_section(self, title: str, id: str):
        self.chapters[-1].sections.append(
            Section(title=title, header_id=id, subsections=[])
        )

    def add_subsection(self, title: str, id: str):
        self.chapters[-1].sections[-1].subsections.append(
            SubSection(
                title=title,
                header_id=id,
            )
        )

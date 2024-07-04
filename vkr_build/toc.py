from bs4 import BeautifulSoup
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

    def render(self, document: BeautifulSoup):
        toc_ul = document.new_tag("ul")

        def new_li_a_tag(title: str, header_id: str, /, bold=False):
            li = document.new_tag("li")
            a = document.new_tag("a", attrs={"href": f"#{header_id}"})

            if bold:
                b = document.new_tag("b")
                b.append(title)
                a.append(b)
            else:
                a.append(title)

            li.append(a)

            return li

        for chapter in self.chapters:
            chapter_li = new_li_a_tag(chapter.title, chapter.header_id, bold=True)

            section_ul = document.new_tag("ul")
            for section in chapter.sections:
                section_li = new_li_a_tag(section.title, section.header_id)

                subsection_ul = document.new_tag("ul")
                for subsection in section.subsections:
                    subsection_ul.append(
                        new_li_a_tag(subsection.title, subsection.header_id)
                    )

                section_li.append(subsection_ul)
                section_ul.append(section_li)

            chapter_li.append(section_ul)
            toc_ul.append(chapter_li)

        return toc_ul

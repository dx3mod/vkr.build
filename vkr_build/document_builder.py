import weasyprint
from bs4 import BeautifulSoup

from vkr_build.config import DocumentConfiguration
from vkr_build.preprocess_stages.numbering import NumberingPreprocessStage
from vkr_build.preprocess_stages.stage import PreprocessStage
from vkr_build.utils import STYLES_PATH
from vkr_build.validators.validator import DocumentValidator


class DocumentBuilder:
    def __init__(self, source_html: str, /, config: DocumentConfiguration):
        self._source_html = source_html
        self._document_config = config

        self._soup = BeautifulSoup(source_html, "html.parser")
        self._preprocess_stages: list[PreprocessStage] = []

    def add_preprocess_stage(self, stage: PreprocessStage):
        self._preprocess_stages.append(stage)

    def build(self):
        self.table_of_contents = self._preprocess_numbering()

        for preprocess_stage in self._preprocess_stages:
            preprocess_stage.process(self._soup)

        # Create document

        document = BeautifulSoup()

        ## Head

        document.head.append(document.new_tag("meta", charset="UTF-8"))  # type: ignore
        document.head.append(  # type: ignore
            document.new_tag(
                "link", rel="stylesheet", href=str(STYLES_PATH.joinpath("vkr.css"))
            )
        )

        ## Оглавление

        toc_title = document.new_tag("h1", attrs={"id": "оглавление"})
        toc_title.append(self._document_config.toc.title)
        document.body.append(toc_title)  # type: ignore

        toc_ul = self.table_of_contents.render(document)
        document.body.append(toc_ul)  # type: ignore

        ## Body

        document.body.append(self._soup)  # type: ignore

        return document

    def _preprocess_numbering(self):
        stage = NumberingPreprocessStage(
            chapter_prefix=self._document_config.chapter.prefix
        )
        stage.process(self._soup)
        return stage.toc

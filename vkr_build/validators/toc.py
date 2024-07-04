from vkr_build.validators.validator import DocumentValidator


class TableOfContentsValidator(DocumentValidator):
    def validate(self, document: DocumentValidator.Document) -> list[str]:
        messages = []

        chapter_titles = [
            chapter.title for chapter in document.table_of_contents.chapters
        ]

        if document.table_of_contents.chapters[0].title != "Введение":
            messages.append("Отсутствует глава 'Введение'!")

        try:
            conclusion_chapter_index = chapter_titles.index("Заключение")

            if len(chapter_titles) <= (
                conclusion_chapter_index + 1
            ) or not chapter_titles[conclusion_chapter_index + 1].startswith("Список"):
                messages.append(
                    "Отсутствует глава 'Список используемых источников'! Она должна идти после Заключения!"
                )

        except ValueError:
            messages.append("Отсутствует глава 'Заключение'!")

        return messages

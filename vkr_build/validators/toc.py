from vkr_build.validators.validator import DocumentValidator


class TableOfContentsValidator(DocumentValidator):
    def validate(self, document: DocumentValidator.Document) -> list[str]:
        messages = []

        if document.table_of_contents.chapters[0].title != "Введение":
            messages.append("Отсутствует глава 'Введение'!")

        if "Заключение" not in map(
            lambda x: x.title, document.table_of_contents.chapters
        ):
            messages.append("Отсутствует глава 'Заключение'!")

        return messages

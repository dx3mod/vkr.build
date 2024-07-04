from vkr_build.validators.validator import DocumentValidator


class TableOfContentsValidator(DocumentValidator):
    def validate(self, document: DocumentValidator.Document) -> list[str]:
        messages = []

        if document.table_of_contents.chapters[0].title != "Введение":
            messages.append("Отсутствует глава 'Введение'!")

        if document.table_of_contents.chapters[-2].title != "Заключение":
            messages.append("Отсутствует глава 'Заключение'!")

        if not document.table_of_contents.chapters[-1].title.startswith("Список"):
            messages.append("Отсутствует глава 'Список используемых источников'!")

        return messages

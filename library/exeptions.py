class BookExistsError(Exception):
    """Исключение для ошибки существования ID в базе данных."""

    def __init__(self, book):
        self.message = f"Книга '{book}' уже существует."
        super().__init__(self.message)

    def __str__(self):
        return self.message


class BookNotExistsError(Exception):
    """Исключения занятого ID(для отладки)"""

    def __init__(self):
        self.message = f"В базе такой книги не существует."

    def __str__(self):
        return self.message

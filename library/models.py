import json
import os
from typing import List

from library.exeptions import BookExistsError


class DataBase:
    """Класс базы данных-JSON файл."""

    _actual_id: int = 1  # Атрибут класса - счетчик ID записей в базе.

    def __init__(self, file_name: str):
        """При инициализации принимает 1 параметр - Имя JSON файла."""
        self.file_name = file_name

    def create(self):
        """Функция для создания файла базы данных.
        Возвращает экземпляр класса базы данных."""

        if not os.path.exists(self.file_name):
            with open(self.file_name, mode='w', encoding="UTF-8") as data_file:
                data_file.write('')
        return self

    def get_all(self):
        """Функция возвращает все записи из базы данных,
         возвращает список словарей, если не найдены - None"""

        with open(self.file_name, mode='r', encoding="UTF-8") as data_file:
            data_str: str = data_file.read()
            if data_str.strip():
                data: List[dict] = json.loads(data_str)
                return data
            return None

    def get(self, book_id: int):
        """Функция возвращает запись из базы запись с id == book_id,
         возвращает запись, если не найдена - None"""

        data: List[dict] = self.get_all()
        if data:
            for book in data:
                if book["id"] == book_id:
                    del book["id"]
                    return Book(**book)
        return None

    def delete(self, book_id: int):
        """Удаляет из базы данных запись с id == book_id,
         возвращает запись, если не найдена - None"""

        data: List[dict] = self.get_all()
        for i in range(len(data)):
            if data[i]["id"] == book_id:
                book = data.pop(i)
                self.write(books_list=data)
                return book
        return None

    def change_status(self, book_id: int, new_status: str):
        """Изменяет статус записи с id == book_id,
        возвращает запись, если не найдена - None"""

        data: List[dict] = self.get_all()
        for i in range(len(data)):
            if data[i]["id"] == book_id:
                data[i]["status"] = new_status
                self.write(books_list=data)
                return data[i]
        return None

    def search(self, key_word: str = None, year: int = None):
        """Ищет записи по ключевому слову или году издания,
        ключевое слово сопоставляется с title and author.
        Возвращает список записей или None если ничего не нашлось"""

        data: List[dict] = self.get_all()
        search_result: list = []
        if key_word:
            for book in data:
                if book["title"].lower() == key_word.lower() or book["author"].lower() == key_word.lower():
                    search_result.append(book)
        elif year:
            for book in data:
                if book["year"] == year:
                    search_result.append(book)
        return search_result or None

    @classmethod
    def update_actual_id(cls, obj: 'DataBase'):
        """Класс метод для обновления счетчика id до максимального
         значения записей из базы данных, если они есть.
         Это гарантирует актуальность счетчика ID при перезапуске программы."""

        data: List[dict] = obj.get_all()
        if data:
            ides: List[int] = sorted([int(book["id"]) for book in data])
            if ides:
                DataBase._actual_id = int(ides[-1]) + 1
        else:
            DataBase._actual_id = 1

    def write(self, book: dict = None, books_list: List[dict] = None):
        """Перезаписывает записи в базу данных.
        Принимает book- новая запись, books_list- список всех записей."""

        data: List[dict] = self.get_all()
        if book:  # Если передана одна новая запись book
            book_with_id: dict = {"id": self._actual_id}  # Присваивается уникальный ID
            DataBase._actual_id += 1  # Счетчик ID увеличивается
            book_with_id.update(book)  # К словарю с id добавляются данные book

            if data:  # Если в базе были записи
                data.append(book_with_id)  # В список записей добавляется новая запись
            else:
                data = [book_with_id]  # Если база пуста то новая запись оборачивается в список

        elif books_list:  # Если передан список записей
            data = books_list  # Подменяем данные для записи переданным списком
        elif isinstance(books_list, list) and not len(books_list):
            data = []  # Если books_list пуст подменяем данные пусты списком

        with open(self.file_name, mode="w", encoding="UTF-8") as data_file:
            json.dump(data, data_file, ensure_ascii=False, indent=4)

    def is_exist(self, book: 'Book'):
        """Проверяет существует ли данная книга в базе данных.
        Проверяет 3 поля объекта book title, author, year на равенство с аналогичными полями в базе.
        Возбуждает исключение, если такая книга есть в базе. Возвращает True/False"""

        try:
            data_books: List[dict] = self.get_all()
            if data_books:
                for data_book in data_books:  # Проверяем не существует ли в базе эта книга
                    if data_book["title"] == book.title \
                            and data_book["author"] == book.author \
                            and data_book["year"] == book.year:
                        raise BookExistsError(book)

        except BookExistsError as e:
            #print(e)
            return True
        return False


class Book:
    """Класс книги. Принимает 4 параметра."""

    def __init__(self, title: str, author: str, year: int, status: str):
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def __str__(self):
        return " | ".join([str(v) for v in self.__dict__.values()])

    def save(self, database: DataBase):
        """Сохраняет экземпляр класса вызывая нужные методы экземпляра класса базы данных.
        Принимает экземпляр класса базы данных.
        Проверяет в базе данных существование дубликата.
        Возвращает свой экземпляр или None."""

        if not database.is_exist(self):  # Проверяет на существование записи с такими же данными
            database.write(book=self.__dict__)
            return self
        return None

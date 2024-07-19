import sys
from time import sleep
from typing import List
from library.env import STATUSES, MENU, DATABASE, CONSENSUS, OUT_MENU
from library.models import Book, DataBase

database = DataBase(DATABASE).create()


def clear_terminal():
    """Выводит 100 пустых строк для имитации очистки терминала."""
    print("\n" * 100)


def return_to_main_menu(func) -> None:
    """Диалоговая функция. Запрашивает у пользователя
    вариант продолжения или возврата в главное меню."""

    sleep(0.5)
    print("Вы хотите повторить операцию или выйти в главное меню?")
    show_menu(OUT_MENU)
    answer: int = validate_interval(1, 2)
    clear_terminal()
    if answer == 1:
        func()
    elif answer == 2:
        menu()


def print_line() -> None:
    """Функция - разделитель. Разделяет этапы общения
    в пользовательском интерфейсе выводом 50ти знаков - """
    print("-" * 50)


def show_menu(menu: dict) -> None:
    """Выводит в терминал переданное menu."""
    for stat in menu.items():
        print(". ".join(stat))


def validate_interval(start: int, end: int) -> int:
    """Валидирует ввод пользователя в зависимости от количества пунктов меню.
    От start до end."""

    while True:
        menu_item: str = input(f"Введите цифру от {start} до {end}: ")

        if menu_item.strip().isdigit() \
                and start <= int(menu_item) <= end:
            print_line()
            return int(menu_item)

        print("Не корректный ввод")
        print_line()


def validate_books_id() -> int:
    """Проверяет корректность ввода id"""
    while True:
        book_id: str = input("Введите ID книги: ")
        if book_id.strip().isdigit():
            return int(book_id)
        print("Не корректный ввод, попробуйте еще раз!")
        print_line()


def delete_book() -> None:
    """Управляет процессом удаления записи из базы данных."""
    data: list | None = database.get_all()
    if data:
        print("Какую книгу вы бы хотели удалить?")
        show_books(is_main=False)
        book_id: int = validate_books_id()
        book = database.get(book_id=book_id)

        # Блок подтверждения удаления
        if book:
            print(f"Вы действительно хотите удалить книгу: {book} ?")
        show_menu(CONSENSUS)
        answer: int = validate_interval(1, 2)
        if answer == 1:
            book = database.delete(book_id)
            if book:
                print("Книга удалена успешно!")
            else:
                print("В базе нет такой книги!")

    else:
        print("В базе данных еще нет книг!")
        print_line()
    return_to_main_menu(delete_book)


def get_books_word(count: int) -> str:
    """Возвращает корректно слагаемое слово книга в зависимости от количества."""

    if 11 <= count % 100 <= 19:
        return "книг"
    last_digit = count % 10
    if last_digit == 1:
        return "книга"
    elif 2 <= last_digit <= 4:
        return "книги"
    else:
        return "книг"


def print_books(data: list) -> None:
    """Выводит в консоль информацию о книге"""

    for book in data:
        print(" | ".join([f"{k}: {v}" for k, v in book.items()]))
    print_line()


def show_books(is_main: bool = True):
    """Выводит в консоль список книг.
    Если is_main True, значит функция вызывается из главного меню. Нужно вызвать функцию выбора дальнейшего действия"""

    data: List[dict] | None = database.get_all()
    if data:
        books_count = len(data)
        print(f"В базе сохранено {books_count} {get_books_word(books_count)}:")
        for book in data:
            print(" | ".join([f"{k}: {v}" for k, v in book.items()]))
        print_line()

    else:
        print("В базе данных еще нет сохраненных книг...")
        print_line()
    if is_main:
        return_to_main_menu(show_books)


def add_book() -> None:
    """Добавление записи с валидацией полей."""

    title: str = input("Введите название книги: ")
    author: str = input("Введите автора книги: ")
    print("Введите год издания книги.")
    year: int = validate_interval(1500, 2024)

    print("Выберите статус книги.")
    show_menu(STATUSES)
    status_index: int = validate_interval(1, 2)
    status: str = STATUSES[str(status_index)]

    book = Book(
        title=title,
        author=author,
        year=year,
        status=status
    )
    book = book.save(database)
    if isinstance(book, Book):
        print("Книга успешно сохранена!!!")
        print_line()
    else:
        print("Что-то пошло не так, обратитесь к администратору!")
        print_line()
    return_to_main_menu(add_book)


def validate_search_input():
    """Проверяет ввод пользователя ключевого слова поиска или года издания."""

    while True:
        key: str = input("Введите ключевое слово или год издания: ")
        if key:
            if key.isdigit():
                return int(key)
            return key.lower()
        print("Вы должны ввести хоть что-то!")
        print_line()


def search_book():
    """Поиск записи по ключевому слову или году издания."""

    print("Вы можете искать книгу по Названию, Автору или Году издания.")
    key: str | int = validate_search_input()
    if isinstance(key, int):
        data:List[dict] = database.search(year=key)
    else:
        data:List[dict] = database.search(key_word=key)

    if data:
        print(f"Найдено {len(data)} {get_books_word(len(data))}")
        print("Результат поиска:")
        print_books(data)
        print_line()

    else:
        print("По вашему запросу ничего не найдено...")
        print_line()
    return_to_main_menu(search_book)


def changing_status_book():
    """Изменение статуса книги"""

    data:List[dict] = database.get_all()

    if data:  #  Блок демонстрации записей и выбора для именения
        print("В какой книге вы бы хотели изменить статус?")
        show_books(is_main=False)
        book_id: int = validate_books_id()
        book = list(filter(lambda d: d['id'] == book_id, data))

        if book:  #  Блок подтверждения раемерений
            print(f"Вы действительно хотите изменить статус книги: {book[0]} ?")
            show_menu(CONSENSUS)
            answer: int = validate_interval(1, 2)

            if answer == 1:  #  Блок выбора нового статуса и схранения
                print("Выберите новый статус книги.")
                show_menu(STATUSES)
                status_index: int = validate_interval(1, 2)
                status: str = STATUSES[str(status_index)]
                book = database.change_status(book_id=book_id, new_status=status)
                if book:
                    print("Статус успешно изменен!")
        else:
            print("В базе нет такой книги!")
    else:
        print("В базе данных еще нет записей.")

    return_to_main_menu(changing_status_book)


#  Словарь главного меню
MENU_FUNCS: dict = {
    1: add_book,
    2: delete_book,
    3: search_book,
    4: show_books,
    5: changing_status_book,
    6: sys.exit
}


def menu():
    """Главное меню. Вывод и выбор пункта"""
    print("Выберите пункт из меню.")
    show_menu(MENU)
    menu_item: int = validate_interval(1, 6)
    MENU_FUNCS[menu_item]()


if __name__ == "__main__":
    DataBase.update_actual_id(database)
    menu()

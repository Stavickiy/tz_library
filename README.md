# Система управления базой данных книг

## Обзор

Этот проект представляет собой простую систему управления базой данных книг, реализованную на Python. Для хранения информации о книгах, включая их название, автора, год издания и статус, используется JSON-файл в качестве базы данных. Система позволяет пользователям добавлять, удалять, искать книги и обновлять их статус.

## Оглавление
- [Установка](#установка)
- [Использование](#использование)
- [Модели](#модели)
  - [DataBase](#database)
  - [Book](#book)
- [Разработчики](#лицензия)

## Установка

1. Клонируйте репозиторий:
    ```sh
    git clone https://github.com/your-username/book-database.git
    ```
2. Перейдите в каталог проекта:
    ```sh
    cd book-database
    ```
3. Убедитесь, что у вас установлен Python версии 3.6 или выше.

4. Зависимостей как токовых нет, скрипт написан на чистом Python.

## Использование

Для запуска приложения выполните основной скрипт:
```sh
python main.py
```

Система предложит меню с вариантами добавления, удаления, поиска, просмотра и обновления статуса книг. Следуйте инструкциям на экране для выполнения нужных действий.


## Модели
### DataBase
Этот класс управляет взаимодействием с JSON-файлом, который служит базой данных. Он предоставляет методы для создания, чтения, обновления и удаления записей о книгах.

### Book
Этот класс представляет собой модель книги.

## Разработчики

- [Евгений Ставицкий](https://t.me/Eugenius71991) — Python Developer
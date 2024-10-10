import sql_db


class BookManager:
    def __init__(self, connection, login):
        self.connection = connection
        self.login = login

    def add_book(self):
        if self.login is None:
            print("Вы должны войти в систему, чтобы добавить книги.")
            return

        name_of_book = input("Введите название книги: ")
        author_of_book = input("Введите автора книги: ")
        year_of_book = input("Введите год издания книги: ")
        user_id = sql_db.check_user_login(self.connection, self.login.user)
        sql_db.add_book(self.connection, name_of_book, author_of_book, year_of_book, user_id)
        print(f"Книга '{name_of_book}' авторства {author_of_book} успешно добавлена.")

    def remove_book(self):
        if self.login is None:
            print("Вы должны войти в систему, чтобы удалить книги.")
            return

        book_id = input("Введите ID книги для удаления: ")
        sql_db.remove_book(self.connection, book_id)

    def show_user_books(self):
        if self.login is None:
            print("Вы должны войти в систему, чтобы просмотреть ваши книги.")
            return

        user_id = sql_db.check_user_login(self.connection, self.login.user)
        user_books = sql_db.get_user_books(self.connection, user_id)
        if user_books:
            print("Ваши книги:")
            for book in user_books:
                print(book)
        else:
            print("У вас еще нет добавленных книг.")

    def show_all_books(self):
        if self.login is None:
            print("Вы должны войти в систему, чтобы просмотреть все книги.")
            return

        sql_db.show_all_books(self.connection)

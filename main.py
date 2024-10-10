import sql_db


class UserRegistration:
    def __init__(self):
        self.name = ""
        self.surname = ""
        self.age = 0
        self.username = ""
        self.password = ""

    @staticmethod
    def get_valid_name(prompt):
        while True:
            name = input(prompt).lower()
            if name.isalpha():
                return name.capitalize()
            else:
                print("Пожалуйста, введите корректное имя.")

    @staticmethod
    def get_valid_age():
        while True:
            try:
                age = int(input("Введите ваш возраст: "))
                if 0 < age < 120:
                    return age
                else:
                    print("Пожалуйста, введите корректный возраст от 1 до 120.")
            except ValueError:
                print("Пожалуйста, введите корректное число.")

    @staticmethod
    def get_valid_username():
        while True:
            username = input("Введите ваше имя пользователя: ")
            if username.strip() and not sql_db.check_user_exists(username):
                return username
            else:
                print("Некорректное имя пользователя или оно уже занято. Попробуйте снова.")

    @staticmethod
    def get_valid_password():
        while True:
            try:
                password = input('Пожалуйста, введите свой пароль (Пароль должен содержать цифры и буквы, не менее 6 символов): ')
                # Проверка на наличие и букв, и цифр, и длины пароля
                if any(char.isdigit() for char in password) and any(char.isalpha() for char in password) and len(
                        password) >= 6:
                    return password
                else:
                    print('Пароль должен содержать как буквы, так и цифры, и быть длиной не менее 6 символов.')
            except Exception as e:
                print(f'Произошла ошибка: {e}')

    def register(self):
        self.name = self.get_valid_name("Введите ваше имя: ")
        self.surname = self.get_valid_name("Введите вашу фамилию: ")
        self.age = self.get_valid_age()
        self.username = self.get_valid_username()  # Используем метод для валидации имени пользователя
        self.password = self.get_valid_password()

        check_password = input('Введите ваш пароль еще раз: ')
        while self.password != check_password:
            print('Пароли не совпадают, попробуйте еще раз.')
            check_password = input('Введите ваш пароль еще раз: ')

        print('Пароль подтвержден.')
        sql_db.insert_customer(self.name, self.surname, self.age, self.username, self.password)
        print(f"Привет {self.username}! Вы успешно зарегистрированы.")
        return True


class UserLogin:
    def __init__(self, connection):
        self.user = ""
        self.password = ""
        self.connection = connection  # Сохраняем соединение

    def authorize(self):
        while True:
            self.user = input("Введите ваше имя пользователя: ")
            self.password = input("Введите ваш пароль: ")
            # Передаем соединение в check_user_credentials
            if sql_db.check_user_credentials(self.connection, self.user, self.password):
                print("Авторизация успешна!")
                return True  # Успешный вход
            else:
                print("Неверное имя пользователя или пароль. Пожалуйста, попробуйте снова.")


def display_menu():
    menu = [
        '1 - Регистрация',
        '2 - Вход',
        '3 - Добавить книгу',
        '4 - Удалить книгу',
        '5 - Показать ваши книги',
        '6 - Показать все книги',
        '7 - Выход'
    ]

    print("\n[Меню]:")
    for option in menu:
        print(option)


def main():
    interface = True
    is_logged_in = False  # Флаг для проверки, вошел ли пользователь в систему
    login = None  # Сохраняем информацию о входе пользователя

    try:
        connection = sql_db.connect_db()  # Устанавливаем соединение
        connection.autocommit = True

        while interface:
            display_menu()

            try:
                choice = int(input('\nВаш выбор: '))
                if choice == 1:
                    registration = UserRegistration()
                    if registration.register():  # Проверка успешной регистрации
                        print(f"Привет {registration.username}! Вы успешно зарегистрированы.")
                elif choice == 2:
                    login = UserLogin(connection)  # Передаем соединение
                    if login.authorize():  # Проверка успешной авторизации
                        print(f"Добро пожаловать {login.user}!")
                        is_logged_in = True  # Устанавливаем флаг, если пользователь вошел

                elif choice == 3:
                    if is_logged_in:
                        name_of_book = input("Введите название книги: ")
                        author_of_book = input("Введите автора книги: ")
                        year_of_book = input("Введите год издания книги: ")
                        user_id = sql_db.check_user_login(connection, login.user)  # Получаем ID пользователя
                        sql_db.add_book(connection, name_of_book, author_of_book, year_of_book,
                                        user_id)  # Передаем ID пользователя
                        print(f"Книга '{name_of_book}' авторства {author_of_book} успешно добавлена.")
                    else:
                        print("Вы должны войти в систему, чтобы добавить книги.")

                elif choice == 4:
                    if is_logged_in:
                        book_id = input("Введите ID книги для удаления: ")
                        sql_db.remove_book(connection, book_id)  # Передаем соединение и ID книги
                    else:
                        print("Вы должны войти в систему, чтобы удалить книги.")


                elif choice == 5:
                    if is_logged_in:
                        user_id = sql_db.check_user_login(connection, login.user)  # Получаем ID пользователя
                        user_books = sql_db.get_user_books(connection, user_id)  # Передаем ID для получения книг
                        if user_books:  # Если книги найдены
                            print("Ваши книги:")
                            for book in user_books:
                                print(book)
                        else:
                            print("У вас еще нет добавленных книг.")

                elif choice == 6:
                    if is_logged_in:
                        sql_db.show_all_books(connection)  # Передаем соединение
                    else:
                        print("Вы должны войти в систему, чтобы просмотреть все книги.")
                elif choice == 7:
                    print("До свидания!")
                    interface = False
                else:
                    print("Пожалуйста, введите корректный вариант.")

            except ValueError:
                print("Неверный ввод. Пожалуйста, введите число от 1 до 7.")

    except Exception as ex:
        print('[ERROR] Ошибка при работе с PostgreSQL:', ex)

    finally:
        if connection:
            connection.close()
            print('[INFO] Соединение с PostgreSQL закрыто.')


if __name__ == "__main__":
    main()

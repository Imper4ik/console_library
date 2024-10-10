import os
from user import UserRegistration, UserLogin
from book import BookManager
import sql_db  # Импортируем функции для работы с БД


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
    is_logged_in = False
    login = None

    try:
        connection = sql_db.connect_db()  # Устанавливаем соединение
        connection.autocommit = True

        while interface:

            display_menu()

            try:
                choice = int(input('\nВаш выбор: '))

                if choice == 1:
                    registration = UserRegistration()
                    registration.register()  # Регистрация
                elif choice == 2:
                    login = UserLogin(connection)
                    if login.authorize():
                        print(f"Добро пожаловать {login.user}!")
                        is_logged_in = True

                book_manager = BookManager(connection, login)

                if choice == 3:
                    if is_logged_in:
                        book_manager.add_book()  # Добавить книгу
                    else:
                        print("Вы должны войти в систему, чтобы добавить книги.")

                elif choice == 4:
                    if is_logged_in:
                        book_manager.remove_book()  # Удалить книгу
                    else:
                        print("Вы должны войти в систему, чтобы удалить книги.")

                elif choice == 5:
                    if is_logged_in:
                        book_manager.show_user_books()  # Показать книги пользователя
                    else:
                        print("Вы должны войти в систему, чтобы просмотреть свои книги.")

                elif choice == 6:
                    if is_logged_in:
                        book_manager.show_all_books()  # Показать все книги
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

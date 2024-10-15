import os

import psycopg2
import bcrypt


dotenv_host = os.getenv('host')
dotenv_user = os.getenv('user')
dotenv_password = os.getenv('password')
dotenv_dbname = os.getenv('dbname')


# Функция для подключения к PostgreSQL
def connect_db():
    return psycopg2.connect(database=dotenv_dbname, user=dotenv_user, password=dotenv_password, host=dotenv_host)


def create_tables(connection):
    with connection.cursor() as cursor:
        # Таблица для всех книг
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS LIBRARY(
            id SERIAL PRIMARY KEY,
            name_the_book VARCHAR(255) NOT NULL,
            author_the_book VARCHAR(255) NOT NULL,
            year_the_book INTEGER NOT NULL
            );
            """
        )
        print('[INFO] Таблица LIBRARY создана')

        # Таблица для информации о пользователях
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Customer_info(
            id SERIAL PRIMARY KEY,
            name_the_customer VARCHAR(255) NOT NULL,
            surname_the_customer VARCHAR(255) NOT NULL,
            age_the_customer INT NOT NULL,
            username_the_customer VARCHAR(255) NOT NULL UNIQUE,
            password_the_customer VARCHAR(255) NOT NULL
            );
            """
        )
        print('[INFO] Таблица Customer_info создана')

        # Таблица для книг пользователей
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS User_Books(
            id SERIAL PRIMARY KEY,
            name_the_book VARCHAR(255) NOT NULL,
            author_the_book VARCHAR(255) NOT NULL,
            year_the_book INTEGER NOT NULL,
            customer_id INT REFERENCES Customer_info(id) ON DELETE CASCADE
            );
            """
        )
        print('[INFO] Таблица User_Books создана')


def check_user_login(connection, username):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id FROM Customer_info WHERE username_the_customer = %s;",
            (username,)
        )
        user_id = cursor.fetchone()
        if user_id:
            # Если пользователь существует, возвращаем его ID
            return user_id[0]
        return None


def check_user_exists(username):
    with connect_db() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM Customer_info WHERE username_the_customer = %s;",
                (username,)
            )
            return cursor.fetchone() is not None


def check_user_credentials(connection, username, password):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT password_the_customer FROM Customer_info WHERE username_the_customer = %s;",
            (username,)
        )
        hashed_password = cursor.fetchone()
        if hashed_password and bcrypt.checkpw(password.encode('utf-8'), hashed_password[0].encode('utf-8')):
            return True
        return False  # Возвращает False, если пользователь не найден или пароль неверный


def insert_customer(name, surname, age, username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    with connect_db() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO Customer_info(name_the_customer, surname_the_customer, age_the_customer, username_the_customer, password_the_customer)
                VALUES (%s, %s, %s, %s, %s);
                """,
                (name, surname, age, username, hashed_password)
            )
            print('[INFO] Данные пользователя успешно добавлены!')


def add_book(connection, name_of_book, author_of_book, year_of_book, customer_id):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO User_Books (name_the_book, author_the_book, year_the_book, customer_id)
            VALUES (%s, %s, %s, %s);
            """,
            (name_of_book, author_of_book, year_of_book, customer_id)
        )
        print(f'[INFO] Книга "{name_of_book}" авторства {author_of_book} добавлена в вашу библиотеку.')


def remove_book(connection, book_id):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM User_Books 
            WHERE id = %s;  -- Убедитесь, что у вас есть поле id в таблице
            """,
            (book_id,)
        )
        print(f'[INFO] Книга с ID {book_id} удалена из вашей библиотеки.')


def show_all_books(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT name_the_book, author_the_book, year_the_book FROM LIBRARY;")
        books = cursor.fetchall()
        print(f'[INFO] Книги в библиотеке:')
        for book in books:
            print(book)


def get_user_books(connection, user_id):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT name_the_book, author_the_book, year_the_book 
            FROM User_Books 
            WHERE customer_id = %s;  -- Используйте ID пользователя
            """,
            (user_id,)
        )
        return cursor.fetchall()


def main():
    try:
        connection = connect_db()
        connection.autocommit = True
        create_tables(connection)  # Создаем таблицы, если их еще нет
    except Exception as ex:
        print('[ERROR] Ошибка при работе с PostgreSQL:', ex)
    finally:
        if connection:
            connection.close()
            print('[INFO] Соединение с PostgreSQL закрыто.')


if __name__ == "__main__":
    main()

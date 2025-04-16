import psycopg2
from config import host, port, db_name, db_user, db_password


def create_connect():
    try:
        # Подключение к базе данных
        db_conn = psycopg2.connect(
            host=host,
            port=port,
            database=db_name,
            user=db_user,
            password=db_password
        )
        print(f"[INFO] Успешное подключение к базе данных '{db_name}'")
        return db_conn  # Возврат соединения
    except Exception as e:
        # Обработка ошибок
        print(f'[INFO] Ошибка при работе с PostgreSQL: {e}')
        return None  # Возврат None при ошибке

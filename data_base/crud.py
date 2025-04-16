def create_table(db_conn):
    try:
        if db_conn is not None:
            with db_conn.cursor() as cursor:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS tasks (
                        id SERIAL PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        description TEXT,
                        status INT
                    )
                    """
                )
                db_conn.commit()
                print("[INFO] Таблица 'tasks' успешно создана.")
        else:
            print("[ERROR] Не удалось создать таблицу: нет соединения с БД.")
    except Exception as e:
        print(f'[ERROR] Ошибка при добавлении задачи: {e}')


def insert_task(db_conn, title, description, status):
    try:
        if db_conn is not None:
            # Проверка, что status — 0 или 1
            if status not in (0, 1):
                print("[ERROR] Status должен быть 0 или 1.")
                return

            with db_conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO tasks (title, description, status) VALUES (%s, %s, %s)
                """, (title, description, status))
            db_conn.commit()
            print("[INFO] Задача успешно добавлена.")
    except Exception as e:
        print(f"[ERROR] Ошибка при добавлении задачи: {e}")


def update_task(db_conn, task_id, title, description, status):
    try:
        if db_conn is not None:
            # Проверка task_id и status
            if not isinstance(task_id, int) or task_id <= 0:
                print("[ERROR] task_id должен быть положительным целым числом.")
                return
            if status not in (0, 1):
                print("[ERROR] Status должен быть 0 или 1.")
                return

            with db_conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE tasks
                    SET title=%s, description=%s, status=%s
                    WHERE id=%s
                """, (title, description, status, task_id))
            db_conn.commit()
            print("[INFO] Задача успешно обновлена.")
    except Exception as e:
        print(f"[ERROR] Ошибка при обновлении задачи: {e}")


def delete_task(db_conn, task_id):
    try:
        if db_conn is not None:
            # Проверка task_id
            if not isinstance(task_id, int) or task_id <= 0:
                print("[ERROR] task_id должен быть положительным целым числом.")
                return

            with db_conn.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM tasks
                    WHERE id=%s
                """, (task_id,))
            db_conn.commit()
            print("[INFO] Задача успешно удалена.")
    except Exception as e:
        print(f"[ERROR] Ошибка при удалении задачи: {e}")


def read_task(db_conn):
    try:
        if db_conn is not None:
            with db_conn.cursor() as cursor:
                cursor.execute("SELECT * FROM tasks")
                return cursor.fetchall()
    except Exception as e:
        print(f'[ERROR] Ошибка при добавлении задачи: {e}')

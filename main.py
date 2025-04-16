from data_base.crud import *
from data_base.db_connection import create_connect

menu = ['create_table', 'insert_task', 'read_task', 'update_task', 'delete_task', 'Exit']

if __name__ == "__main__":
    db_connection = create_connect()  # Создание подключения

    while True:
        print(*[f'{i + 1}. {func}' for i, func in enumerate(menu)], sep='\n')
        choice = input('Напиши сюда какую функцию хочешь выполнить : ').strip().lower()
        
        if choice == '1':
            create_table(db_connection)  # Создание таблицы

        elif choice == '2':
            title = input("Введите заголовок задачи: ")
            description = input("Введите описание задачи: ")
            status = int(input("Введите статус задачи (например, 0 - не выполнена, 1 - выполнена): "))
            insert_task(db_connection, title, description, status)

        elif choice == '3':
            tasks = read_task(db_connection)
            for task in tasks:
                print(task)

        elif choice == '4':
            title = input("Введите заголовок задачи для обновления: ")
            new_description = input("Введите новое описание задачи: ")
            new_status = int(input("Введите новый статус задачи: "))
            update_task(db_connection, title, new_description, new_status)

        elif choice == '5':
            title = input("Введите заголовок задачи для удаления: ")
            delete_task(db_connection, title)

        elif choice == '6' or choice == 'exit':
            print('Пока')
            break  # Выход из цикла

        else:
            print('Неправильный выбор. Пожалуйста, выберите функцию из списка.')

    if db_connection:
        db_connection.close()  # Закрытие соединения

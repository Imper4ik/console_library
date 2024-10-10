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
                if any(char.isdigit() for char in password) and any(char.isalpha() for char in password) and len(password) >= 6:
                    return password
                else:
                    print('Пароль должен содержать как буквы, так и цифры, и быть длиной не менее 6 символов.')
            except Exception as e:
                print(f'Произошла ошибка: {e}')

    def register(self):
        self.name = self.get_valid_name("Введите ваше имя: ")
        self.surname = self.get_valid_name("Введите вашу фамилию: ")
        self.age = self.get_valid_age()
        self.username = self.get_valid_username()
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
        self.connection = connection

    def authorize(self):
        while True:
            self.user = input("Введите ваше имя пользователя: ")
            self.password = input("Введите ваш пароль: ")
            if sql_db.check_user_credentials(self.connection, self.user, self.password):
                print("Авторизация успешна!")
                return True
            else:
                print("Неверное имя пользователя или пароль. Пожалуйста, попробуйте снова.")

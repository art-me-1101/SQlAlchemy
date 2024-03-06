from flask import Flask
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/mars_explorer.db")
    capitan = User()
    capitan.surname = 'Scott'
    capitan.name = 'Ridley'
    capitan.age = 21
    capitan.position = 'captain'
    capitan.speciality = 'research engineer'
    capitan.address = 'module_1'
    capitan.email = 'scott_chief@mars.org'
    user1 = User()
    user1.surname = 'Max'
    user1.name = 'Lowwer'
    user1.age = 18
    user1.position = 'help_me'
    user1.speciality = 'research doctor'
    user1.address = 'qwerty123'
    user1.email = 'qwerty123@chess.org'
    user2 = User()
    user2.surname = 'Quanty'
    user2.name = 'Lazer'
    user2.age = 45
    user2.position = 'inspector'
    user2.speciality = 'research inspector'
    user2.address = 'module_228'
    user2.email = 'kfc@sql.org'
    user3 = User()
    user3.surname = 'Web'
    user3.name = 'Api'
    user3.age = 52
    user3.position = 'main.py'
    user3.speciality = 'pilot'
    user3.address = '13_queue'
    user3.email = '😁😰💣@sun.ru'
    db_sess = db_session.create_session()
    db_sess.add(capitan)
    db_sess.add(user1)
    db_sess.add(user2)
    db_sess.add(user3)
    db_sess.commit()
    app.run()


if __name__ == '__main__':
    main()


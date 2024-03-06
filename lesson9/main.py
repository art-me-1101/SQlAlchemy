import datetime
from flask import Flask
from data import db_session
from data.users import User
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/mars_explorer.db")
    job1 = Jobs()
    job1.team_leader = 1
    job1.job = 'deployment of residential modules 1 and 2'
    job1.work_size = 15
    job1.collaborators = '2, 3'
    job1.start_date = datetime.datetime.now()
    job1.is_finished = False
    db_sess = db_session.create_session()
    db_sess.add(job1)
    db_sess.commit()
    app.run()


if __name__ == '__main__':
    main()

from flask import Flask, render_template, url_for

from data import db_session
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/mars_explorer.db")
    app.run()


@app.route('/')
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs)
    return render_template("works_log.html", style_file=url_for(
        'static', filename='css/style.css'), jobs=jobs)


if __name__ == '__main__':
    main()

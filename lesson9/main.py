from flask import Flask, render_template, redirect, request, abort, jsonify, make_response
from flask_login import LoginManager, logout_user, login_required, current_user
from flask_login import login_user
from flask_restful import Api

from data import db_session
from data.departments import Department
from data.job_api import blueprint
from data.jobs import Jobs
from data.users import User
from forms.department import DepartForm
from forms.job import JobForm
from forms.login import LoginForm
from forms.user import RegisterForm
from data.jobs_resourse import JobsListResource, JobsResource

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)
api.add_resource(JobsListResource, '/api/v2/jobs')

api.add_resource(JobsResource, '/api/v2/jobs/<int:job_id>')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


def main():
    db_session.global_init("db/mars_explorer.db")
    app.register_blueprint(blueprint)
    app.run()


@app.route('/')
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs)
    return render_template("works_log.html", jobs=jobs, title='Главная страница')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        if form.age.data <= 0:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Введён неправильный возраст")
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
            age=form.age.data,
            speciality=form.speciality.data,
            address=form.address.data,
            position=form.position.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/make_job', methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs()
        jobs.job = form.title.data
        jobs.collaborators = form.collaborators.data
        jobs.work_size = form.work_size.data
        jobs.is_finished = form.is_finished.data
        current_user.jobs.append(jobs)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('new_job.html', title='Добавление работы',
                           form=form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = JobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id).filter(
            (Jobs.user == current_user) | (current_user.id == 1)).first()
        if jobs:
            form.title.data = jobs.job
            form.work_size.data = jobs.work_size
            form.collaborators.data = jobs.collaborators
            form.is_finished.data = jobs.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id).filter(
            (Jobs.user == current_user) | (current_user.id == 1)).first()
        if jobs:
            jobs.job = form.title.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
            jobs.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('new_job.html',
                           title='Редактирование работы',
                           form=form
                           )


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id).filter(
        (Jobs.user == current_user) | (current_user.id == 1)).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/make_depart', methods=['GET', 'POST'])
@login_required
def add_depart():
    form = DepartForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        depart = Department()
        depart.title = form.title.data
        depart.members = form.members.data
        depart.email = form.email.data
        current_user.departments.append(depart)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/depart_list')
    return render_template('new_depart.html', title='Добавление департамента',
                           form=form)


@app.route('/depart_list')
def depart_list():
    db_sess = db_session.create_session()
    departs = db_sess.query(Department)
    return render_template("depart_list.html", departs=departs, title='Список департаментов')


@app.route('/depart/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_depart(id):
    form = DepartForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        depart = db_sess.query(Department).filter(Department.id == id).filter(
            (Department.user == current_user) | (current_user.id == 1)).first()
        if depart:
            form.title.data = depart.title
            form.members.data = depart.members
            form.email.data = depart.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        depart = db_sess.query(Department).filter(Department.id == id).filter(
            (Department.user == current_user) | (current_user.id == 1)).first()
        if depart:
            depart.title = form.title.data
            depart.members = form.members.data
            depart.work_size = form.email.data
            db_sess.commit()
            return redirect('/depart_list')
        else:
            abort(404)
    return render_template('new_depart.html',
                           title='Редактирование департамента',
                           form=form
                           )


@app.route('/depart_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def depart_delete(id):
    db_sess = db_session.create_session()
    depart = db_sess.query(Department).filter(Department.id == id).filter(
        (Department.user == current_user) | (current_user.id == 1)).first()
    if depart:
        db_sess.delete(depart)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/depart_list')


if __name__ == '__main__':
    main()

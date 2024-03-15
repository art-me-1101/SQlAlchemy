import flask
from flask import make_response, jsonify, request, redirect

from . import db_session
from .jobs import Jobs
from .users import User

blueprint = flask.Blueprint(
    'job_api',
    __name__,
    template_folder='templates'
)

@blueprint.route('/api/job')
def get_job():
    return "Обработчик в job_api"


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(
                    only=('id', 'job', 'team_leader', 'work_size', 'collaborators', 'start_date', 'is_finished'))
                    for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_job(job_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(job_id)
    if not jobs:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'jobs':
                jobs.to_dict(
                    only=('id', 'job', 'team_leader', 'work_size', 'collaborators', 'start_date', 'is_finished'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['job', 'team_leader', 'collaborators', 'work_size', 'is_finished']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    jobs = Jobs(
        job=request.json['job'],
        team_leader=request.json['team_leader'],
        collaborators=request.json['collaborators'],
        work_size=request.json['work_size'],
        is_finished=request.json['is_finished']
    )
    db_sess.add(jobs)
    db_sess.commit()
    return redirect(f'http://localhost:5000/api/jobs/{jobs.id}')


@blueprint.route('/api/jobs/refactor/<int:job_id>', methods=['POST'])
def refactor_job(job_id):
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['job', 'team_leader', 'collaborators', 'work_size', 'is_finished']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    job.job = request.json['job']
    job.team_leader = request.json['team_leader']
    job.collaborators = request.json['collaborators']
    job.work_size = request.json['work_size']
    job.is_finished = request.json['is_finished']
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'id': job.id})


@blueprint.route('/api/jobs/<int:news_id>', methods=['DELETE'])
def delete_jobs(news_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(news_id)
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(
                    only=('id', 'job', 'team_leader', 'work_size', 'collaborators', 'start_date', 'is_finished'))
                    for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(Jobs).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'users':
                user.to_dict(
                    only=('id', 'job', 'team_leader', 'work_size', 'collaborators', 'start_date', 'is_finished'))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['name', 'surname', 'age', 'speciality', 'position', 'address', 'email', 'password']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    user = User(
        name=request.json['name'],
        surname=request.json['surname'],
        age=request.json['age'],
        speciality=request.json['speciality'],
        position=request.json['position'],
        address=request.json['address'],
        email=request.json['email']
    )
    user.set_password(request.json['password'])
    db_sess.add(user)
    db_sess.commit()
    return redirect(f'http://localhost:5000/api/jobs/{user.id}')


@blueprint.route('/api/users/refactor/<int:user_id>', methods=['POST'])
def refactor_user(user_id):
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['name', 'surname', 'age', 'speciality', 'position', 'address', 'email', 'password']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    user.name = request.json['name']
    user.surname = request.json['surname']
    user.age = request.json['age']
    user.speciality = request.json['speciality']
    user.position = request.json['position']
    user.address = request.json['address']
    user.email = request.json['email']
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'id': user.id})


@blueprint.route('/api/jobs/<int:user_id>', methods=['DELETE'])
def delete_news(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})
import flask

blueprint = flask.Blueprint(
    'job_api',
    __name__,
    template_folder='templates'
)

@blueprint.route('/api/job')
def get_job():
    return "Обработчик в job_api"

from flask.blueprints import Blueprint
from flask_restx import Api
from apps.user.namespaces.user_namespace import user_namespace


user_blueprint = Blueprint(
    'api', __name__, 
    template_folder='templates/user', 
    url_prefix='/api')


api = Api(
        user_blueprint,
        title='User', 
        version='1.0',
        description='User Information'
    )

api.add_namespace(user_namespace)

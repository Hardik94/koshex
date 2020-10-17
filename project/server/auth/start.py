from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project.server.errors import RootException, AuthException
auth_blueprint = Blueprint('Init', __name__)

class InitAPI(MethodView):
    def get(self):
        try:
            responseObject = {
                'status': 'success',
                'message': 'Welcome, Koshex Application Running.',
            }
            return make_response(jsonify(responseObject)), 201
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return make_response(jsonify(responseObject)), 401

# define the API resources
init_view = InitAPI.as_view('init_api')

# add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/',
    view_func=init_view,
    methods=['GET']
)

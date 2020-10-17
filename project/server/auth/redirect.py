from flask import Blueprint, request, make_response, jsonify, redirect
from flask.views import MethodView
from sqlalchemy import func, desc, text

from project.server.models import Urls, Metadata, db
from project.server.errors import RootException, AuthException
from project.server import url_shortner

import os
auth_blueprint = Blueprint('Meta', __name__)

class DetailAPI(MethodView):
    def get(self, **kwargs):
        try:

            keyword = ""
            if len(kwargs['shorten']) != 6:
                keyword = ""
            else:
                keyword = kwargs['shorten']

            if keyword:
                org_url = Urls.query.filter(Urls.shorten==keyword).first()
                if org_url:
                    mtdata = Metadata(url_id=org_url.id)
                    db.session.add(mtdata)
                    db.session.commit()
                    return redirect(org_url.origional, 302)
                else:
                    responseObject = {
                        'status': 'fail',
                        'message': "Couldn't find the requested resources.",
                    }
                    return make_response(jsonify(responseObject)), 201
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'Please add valid url.'
                }
                return make_response(jsonify(responseObject)), 201
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return make_response(jsonify(responseObject)), 401


detail_view = DetailAPI.as_view('detail_api')
auth_blueprint.add_url_rule(
    '/',
    view_func=detail_view,
    methods=['GET']
)

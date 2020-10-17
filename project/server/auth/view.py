
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from sqlalchemy import func, desc, text

from project.server.models import Urls, Metadata, db
from project.server.errors import RootException, AuthException
from project.server import url_shortner
import os
auth_blueprint = Blueprint('App', __name__)



class ShortenAPI(MethodView):
    """
    Shotening Url Resource
    """
    def post(self):
        try:
            post_data = request.get_json()
            if post_data:
                new_url = url_shortner.make_shorten(post_data['url'])
                unpath = os.path.basename(new_url)
                entry = Urls.query.filter_by(shorten=unpath).first()
                if entry:
                    mtdata = Metadata(url_id=entry.id)
                    db.session.add(mtdata)
                    db.session.commit()
                else:
                    url = Urls(shorten=unpath, origional=post_data['url'])
                    Metadata(u=url)
                    db.session.add(url)
                    db.session.commit()
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully created short url.',
                    "data": {
                        "updated_url": new_url
                    }
                }
                return make_response(jsonify(responseObject)), 201
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'Please add some url.',
                }
                return make_response(jsonify(responseObject)), 201
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return make_response(jsonify(responseObject)), 401

class SearchAPI(MethodView):
    def get(self):
        try:
            param_data = request.args.to_dict()
            result = Urls.query.filter(Urls.origional.ilike("%"+param_data['key']+"%")).all()
            if result:
                data = []
                for item in result:
                    data.append({'org': item.origional, 'shorten': "https://tinyurl.com/" + item.shorten})
                responseObject = {
                    'status': 'success',
                    'message': 'Requested data Found.',
                    "data": data
                }
                return make_response(jsonify(responseObject)), 201
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'No data Found.'
                }
                return make_response(jsonify(responseObject)), 201
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return make_response(jsonify(responseObject)), 401

class DetailAPI(MethodView):
    def get(self, **kwargs):
        try:

            total_count = Metadata.query.join(Urls, Metadata.url_id==Urls.id).filter(Urls.shorten==kwargs['shorten']).count()

            sql = text("select date_part('hour', metadata.created_at) AS hour, count(metadata.id) as total from metadata inner join urls on urls.id=metadata.url_id where shorten='{shorten}' group by date_part('hour', metadata.created_at) order by date_part('hour', metadata.created_at) desc limit 10;".format(**kwargs))
            result = db.engine.execute(sql)
            hourly = [{'Hour': row[0], "Hits": row[1]} for row in result]

            responseObject = {
                'status': 'success',
                'message': 'Requested data Found.',
                "data": {
                    'total_hits': total_count,
                    'Hourly_hits': hourly
                }
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
shorten_view = ShortenAPI.as_view('shorten_api')
detail_view = DetailAPI.as_view('detail_api')
search_view = SearchAPI.as_view('search_api')

# add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/create',
    view_func=shorten_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/search',
    view_func=search_view,
    methods=['GET']
)
auth_blueprint.add_url_rule(
    '/<shorten>',
    view_func=detail_view,
    methods=['GET']
)

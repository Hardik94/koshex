from project.server import app
from flask import Blueprint, request, make_response, jsonify

class RootException(Exception):
    status_code = 200

    def __init__(self, message=None, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
        # if self.payload == 'TIMEOUT':
        #     self.message = "Server Connection Read time out, Please retry after sometime."

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class AuthException(Exception):
    status_code = 401

    def __init__(self, message=None, status_code=None, payload=None):
        Exception.__init__(self)
        if message is not None:
            self.message = message
        else:
            self.message = "Auth token is incorrect."
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class ResourceAuthException(Exception):
    status_code = 403

    def __init__(self, message=None, status_code=None, payload=None):
        Exception.__init__(self)
        # print("Entered")
        if message is not None:
            self.message = message
        else:
            self.message = "this user doesn't have sufficient permission to access the API."
        if status_code is not None:
            self.status_code = status_code
        else:
            self.status_code = ResourceAuthException.status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(RootException)
def handle_root_exception(error):
    '''Return a custom message and 400 status code'''
    # return {'message': 'Authentication token invalid'}, 400
    responseObject = {
        'status': 'fail',
        'message': error.message if error.message else 'Server is busy, Please try again after some time.' 
    }
    return make_response(jsonify(responseObject)), 200


@app.errorhandler(AuthException)
def handle_auth_exception(error):
    '''Return a auth message and 401 status code'''
    responseObject = {
        'status': 'fail',
        'message': "Bearer token malformed." if error.payload==1 else ("Provide a valid auth token" if error.payload==2 else error.message)
    }
    return make_response(jsonify(responseObject)), 401

@app.errorhandler(ResourceAuthException)
def handle_resource_auth_exception(error):
    '''Return a custom message and 200 status code'''
    print("entered")
    responseObject = {
        'status': 'fail',
        'message': error.message
    }
    return make_response(jsonify(responseObject)), error.status_code

import datetime
from project.server import app, db, bcrypt
import logging, copy

logger = logging.getLogger()

class Urls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    origional = db.Column(db.String(1000), unique=False, nullable=False)
    shorten = db.Column(db.String(1000), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

class Metadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    url_id = db.Column(db.Integer, db.ForeignKey('urls.id'), nullable=False)
    u = db.relationship('Urls', backref=db.backref('url', lazy=True))

class User():
    def __init__(self, email, password, role, username):
        self.email = email
        self.password = bcrypt.generate_password_hash(password, app.config.get('BCRYPT_LOG_ROUNDS')).decode()
        self.user = username
        self.role = role
        self.active = 1

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7, seconds=0),
                'iat': datetime.datetime.utcnow(),
                'data': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            # is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            is_blacklisted_token = False
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                # return payload['sub']
                return payload['data']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'



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


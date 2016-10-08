from marshmallow import fields, post_load, Schema
from sqlalchemy.dialects.postgresql import BIGINT, TEXT

from application import app, db

# TODO(stfinancial): Add required fields when the time comes.
class UserSchema(Schema):
	user_id = fields.Integer()
	username = fields.String()
	password = fields.String()
	
	@post_load
	def make_user(self, data):
		return User(**data)

class User(db.Model):
	user_id = db.Column('user_id', BIGINT, primary_key=True)
	username = db.Column('username', TEXT(), unique=True, nullable=False)
	password = db.Column('password', TEXT())
	
	def __init__(self, *args, **args):
		# TODO(stfinancial): Raise exception if this doesn't exist?
		self.user_id = kwargs.get('user_id')
		self.username = kwargs.get('username')
		self.password = kwargs.get('password')

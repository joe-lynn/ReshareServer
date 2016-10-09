from marshmallow import fields, post_load, Schema
from sqlalchemy.dialects.postgresql import BIGINT, TEXT

from application import app, db
from models.rental import RentalSchema

# TODO(stfinancial): Add required fields when the time comes.
class UserSchema(Schema):
	user_id = fields.Integer()
	username = fields.String()
	password = fields.String()
	
	rentals = fields.Nested(RentalSchema, many=True)
	ownerships = fields.Nested(RentalSchema, many=True)

	@post_load
	def make_user(self, data):
		return User(**data)

class User(db.Model):
	user_id = db.Column('user_id', BIGINT, primary_key=True)
	username = db.Column('username', TEXT(), unique=True, nullable=False)
	password = db.Column('password', TEXT(), nullable=False)
	
	rentals = db.relationship('Rental', backref='user', lazy='dynamic', cascade='save-update, merge, delete')
	
	def __init__(self, *args, **args):
		# TODO(stfinancial): Raise exception if this doesn't exist?
		self.user_id = kwargs.get('user_id')
		self.username = kwargs.get('username')
		self.password = kwargs.get('password')

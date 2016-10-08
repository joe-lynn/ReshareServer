import datetime as dt

from marshmallow import fields, post_load, Schema, validates_schema, ValidationError
from sqlalchemy.dialects.postgresql import BIGINT, INTEGER, TEXT
from sqlalchemy.types import DateTime

from application import app, db

MAX_COMMENT_LENGTH = 8192
MIN_COMMENT_LENGTH = 32
MAX_RATING = 5
MIN_RATING = 1

class RentalRatingSchema(Schema):
	rating_id = fields.Integer()
	rental_id = fields.Integer()
	rating = fields.Float()
	comment = fields.String()
	
	# TODO(stfinancial): Should we keep track of last edited timestamp, all revisions, creation timestamp? Or just update the timestamp every time the comment is changed?
	timestamp = fields.DateTime()
	
	@post_load
	def make_rental_rating(self, data):
		return RentalRating(**data)
	
	@validates_schema
	def validate_input(self, data):
		if 'rating' in data and data['rating'] < MIN_RATING or data['rating'] > MAX_RATING:
			raise ValidationError('Rating is invalid.')
		if 'comment' in data and data['comment'] > MAX_COMMENT_LENGTH or data['comment'] < MIN_COMMENT_LENGTH:
			# TODO(stfinancial): Return separate errors for each case to help user.
			raise ValidationError('Comment too long.')

class RentalRating(db.Model):
	rating_id = db.Column('rating_id', BIGINT, primary_key=True)
	rental_id = db.Column('rental_id', BIGINT, unique=True, nullable=False)
	rating = db.Column('rating', INTEGER, default=None)
	comment = db.Column('comment', TEXT(), default='')
	
	timestamp = db.Column('timestamp' DateTime(timezone=True), nullable=False)
	
	def __init__(self, *args, **kwargs):
		self.rental_id = kwargs.get('rental_id', 0)
		self.rating = kwargs.get('rating', None)
		self.comment = kwargs.get('comment', '')
		self.timestamp = kwargs.get('timestamp', dt.datetime.utcnow())

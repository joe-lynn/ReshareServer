import datetime as dt

from marshmallow import fields, post_load, Schema, validates_schema, ValidationError
from sqlalchemy.dialects.postgresql import BIGINT, BOOLEAN, INTEGER, REAL, TEXT
from sqlalchemy.types import DateTime

from application import app, db

# TODO(stfinancial): This value should probably be reduced
MAX_COMMENT_LENGTH = 8192
MIN_COMMENT_LENGTH = 32
MAX_RATING = 5
MIN_RATING = 1

class RentalSchema(Schema):
	rental_id = fields.Integer()
	listing_id = fields.Integer()
	owner_id = fields.Integer()
	renter_id = fields.Integer()
	
	# TODO(stfinancial): Fields for duration, late, broke, etc.
	
	start_timestamp = fields.DateTime()
	end_timestamp = fields.DateTime()
	amount_paid = fields.Float()
	
	rating = fields.Integer()
	comment = fields.String()
	comment_timestamp = fields.DateTime()
		
	@post_load
	def make_rental(self, data):
		return Rental(**data)
	
	# TODO(stfinancial): Check the timestamps are ok, owner!=renter, ids exist, etc.
	@validates_schema
	def validate_input(self, data):
		# TODO(stfinancial): Tell user what these limits actually are.
		if 'rating' in data and data['rating'] < MIN_RATING:
			raise ValidationError('Rating is below minimum')
		if 'rating' in data and data['rating'] > MAX_RATING:
			raise ValidationError('Rating is above maximum')
		if 'comment' in data and data['comment'] < MIN_COMMENT_LENGTH:
			raise ValidationError('Comment is too short.')
		if 'comment' in data and data['comment'] > MAX_COMMENT_LENGTH:
			raise ValidationError('Comment is too long.')

# TODO(stfinancial): Shouldn't be able to POST a rental with a rating already or end_timestamp/start_timestamp	
class Rental(db.Model):
	rental_id = db.Column('rental_id', BIGINT, primary_key=True)
	# TODO(stfinancial): Can these be null if a user/listing is deleted?
	listing_id = db.Column('listing_id', BIGINT)
	owner_id = db.Column('owner_id', BIGINT)
	renter_id = db.Column('renter_id', BIGINT)
	
	start_timestamp = db.Column('start_timestamp', DateTime(timezone=True), nullable=False)
	end_timestamp = db.Column('end_timestamp', DateTime(timezone=True))
	amount_paid = db.Column('amount_paid', REAL())

	rating = db.Column('rating', INTEGER, default=None)
	comment = db.Column('comment', TEXT(), default='')
	comment_timestamp = db.Column('comment_timestamp', DateTime(timezone=True), default=None)	
	
	def __init__(self, *args, **kwargs):
		# TODO(stfinancial): Reasonable defaults or raise exceptions
		self.listing_id = kwargs.get('listing_id', 0)
		self.owner_id = kwargs.get('owner_id', 0)
		self.renter_id = kwargs.get('renter_id', 0)
		self.start_timestamp = kwargs.get('start_timestamp', dt.datetime.utcnow())
		self.end_timestamp = kwargs.get('end_timestamp', None)
		self.amount_paid = kwargs.get('amount_paid', 0)
		self.rating = kwargs.get('rating', None)
		self.comment = kwargs.get('comment', '')
		self.comment_timestamp = kwargs.get('coment_timestamp', None)

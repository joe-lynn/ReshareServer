import datetime as dt

from marshmallow import fields, post_load, Schema, validates_schema, ValidationError
from sqlalchemy.dialects.postgresql import BIGINT, BOOLEAN, INTEGER, REAL, TEXT
from sqlalchemy.types import DateTime

from application import app, db
from models.rental_rating import RentalRatingSchema

class RentalSchema(Schema):
	rental_id = fields.Integer()
	listing_id = fields.Integer()
	owner_id = fields.Integer()
	renter_id = fields.Integer()
	
	# TODO(stfinancial): Fields for duration, late, broke, etc.
	
	start_timestamp = fields.DateTime()
	end_timestamp = fields.DateTime()
	amount_paid = fields.Float()
	
	ratings = fields.Nested(RentalRatingSchema, many=True)
	
	@post_load
	def make_rental(self, data):
		return Rental(**data)
	
	# TODO(stfinancial): Check the timestamps are ok, owner!=renter, ids exist, etc.
	@validates_schema
	def validate_input(self, data):
		return

# TODO(stfinancial): Shouldn't be able to POST a rental with a rating already or end_timestamp/start_timestamp	
class Rental(db.Model):
	rental_id = db.Column('rental_id', BIGINT, primary_key=True)
	listing_id = db.Column('listing_id', BIGINT)
	owner_id = db.Column('owner_id', BIGINT)
	renter_id = db.Column('renter_id', BIGINT)
	
	start_timestamp = db.Column('start_timestamp', DateTime(timezone=True), nullable=False)
	end_timestamp = db.Column('end_timestamp', DateTime(timezone=True))
	amount_paid = db.Column('amount_paid', REAL())
	
	# TODO(stfinancial): Not sure if I want cacade delete or not.
	ratings = db.relationship('RentalRating', backref='rental', lazy='dynamic', cascade='save-update, merge')
	
	def __init__(self, *args, **kwargs):
		# TODO(stfinancial): Reasonable defaults or raise exceptions
		self.listing_id = db.Column('listing_id', 0)
		self.owner_id = db.Column('owner_id', 0)
		self.renter_id = db.Column('renter_id', 0)
		self.start_timestamp = db.Column('start_timestamp', dt.datetime.utcnow())
		self.end_timestamp = db.Column('end_timestamp', None)
		self.amount_paid = db.Column('amount_paid', 0)

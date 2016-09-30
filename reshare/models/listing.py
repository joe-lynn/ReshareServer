import datetime as dt

from marshmallow import fields, post_load, Schema
from sqlalchemy.dialects.postgresql import BIGINT, BOOLEAN, INTEGER, REAL, TEXT, VARCHAR
from sqlalchemy.types import DateTime

from application import app, db
from models.listing_category import describes

# TODO(stfinancial): I want to move away from using UUID, and switch to SERIAL type.
# TODO(stfinancial): Need to see whether to set as_string
class ListingSchema(Schema):
	# Add validations here, see: https://marshmallow.readthedocs.io/en/latest/quickstart.html#serializing-objects-dumping
	listing_id = fields.Integer() # TODO(stfinancial): Check if this can support the BigInteger type
	price_per_hour = fields.Float()
	price_per_day = fields.Float()
	price_per_week = fields.Float()
	maximum_time = fields.Integer()
	minimum_time = fields.Integer()
	has_delivery = fields.Boolean()
	delivery_price =  fields.Float()
	late_fee = fields.Float()
	broken_price = fields.Float()
	title = fields.String()
	description = fields.String()
	is_closed = fields.Boolean()
	creation_timestamp = fields.DateTime()
	
	@post_load
	def make_listing(self, data):
		return Listing(**data)

class Listing(db.Model):
	listing_id = db.Column('listing_id', BIGINT, primary_key=True)
	price_per_hour = db.Column('price_per_hour', REAL())
	price_per_day = db.Column('price_per_day', REAL())
	price_per_week = db.Column('price_per_week', REAL(), default=-1)
	maximum_time = db.Column('maximum_time', INTEGER)
	minimum_time = db.Column('minimum_time', INTEGER)
	
	has_delivery = db.Column('has_delivery', BOOLEAN(), default=False)
	delivery_price = db.Column('delivery_price', REAL(), default=0)
	
	late_fee = db.Column('late_fee', REAL())
	broken_price = db.Column('broken_price', REAL())
	
	title = db.Column('title', VARCHAR(512), nullable=False)
	description = db.Column('description', TEXT())
	
	is_closed = db.Column('is_closed', BOOLEAN(), default=False)
	creation_timestamp = db.Column('creation_timestamp', DateTime(timezone=True), nullable=False)
	
	addons = db.relationship('ListingAddon', backref='listing', lazy='dynamic', cascade='save-update, merge, delete')
	categories = db.relationship('ListingCategory', secondary=describes, backref='listing', lazy='dynamic', cascade='save-update, merge, delete')
	images = db.relationship('ListingImage', backref='listing', lazy='dynamic', cascade='save-update, merge, delete')
	
	def __init__(self, *args, **kwargs):
		print "Constructing instance"
		# TODO(pallarino): Need to scrub the data to make sure it works.
		# TODO(pallarino): How do I avoid SQL injection?
		# TODO(pallarino): Set reasonable defaults for these.
		self.title = kwargs.get('title', 'Empty Title')
		self.price_per_hour = kwargs.get('price_per_hour', -1)
		self.price_per_day = kwargs.get('price_per_day', -1)
		self.price_per_week = kwargs.get('price_per_week', -1)
		self.maximum_time = kwargs.get('maximum_time', 7)
		self.minimum_time = kwargs.get('minimum_time', 1)
		
		self.has_delivery = kwargs.get('has_delivery', False)
		self.delivery_price = kwargs.get('delivery_price', 0)
		
		self.late_fee = kwargs.get('late_fee', 0)
		self.broken_price = kwargs.get('broken_price', 0)
		
		self.description = kwargs.get('description', '')
		
		self.creation_timestamp = dt.datetime.utcnow()
		return
	
	def __repr__(self):
		return '<Listing %r>' % self.title


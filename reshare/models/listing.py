import datetime as dt

from marshmallow import fields, post_load, Schema, validates_schema, ValidationError
from sqlalchemy.dialects.postgresql import BIGINT, BOOLEAN, INTEGER, REAL, TEXT, VARCHAR
from sqlalchemy.types import DateTime

from application import app, db
from models.listing_addon import ListingAddonSchema
from models.listing_category import describes, ListingCategorySchema
from models.listing_image import ListingImageSchema
from models.rental import RentalSchema

MAX_DESCRIPTION_LEN = 8192
MAX_TITLE_LEN = 256

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
	delivery_price = fields.Float()
	late_fee = fields.Float()
	broken_price = fields.Float()
	title = fields.String()
	description = fields.String()
	is_closed = fields.Boolean()
	creation_timestamp = fields.DateTime()
	
	# TODO(stfinancial): Need to be able to handle these properly for both POST and PUT.
	addons = fields.Nested(ListingAddonSchema, many=True)
	images = fields.Nested(ListingImageSchema, many=True)
	categories = fields.Nested(ListingCategorySchema, many=True)
	
	# TODO(stfinancial): The biggest problem with this is if the listing changes, the rental will point to old version
	rentals = fields.Nested(RentalSchema, many=True)
	
	@post_load
	def make_listing(self, data):
		return Listing(**data)
	
	@validates_schema
	def validate_input(self, data):
		if 'description' in data and len(data['description']) > MAX_DESCRIPTION_LEN:
			raise ValidationError('Description is too long.')
		if 'title' in data and len(data['title']) > MAX_TITLE_LEN:
			raise ValidationError('Title is too long')

# TODO(stfinancial): Change these deaults to None probably
class Listing(db.Model):
	listing_id = db.Column('listing_id', BIGINT, primary_key=True)
	
	# TODO(stfinancial): Need to handle price resolution given a bunch of inputs.
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
		# TODO(stfinancial): Need to scrub the data to make sure it works.
		# TODO(stfinancial): How do I avoid SQL injection?
		# TODO(stfinancial): Set reasonable defaults for these.
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


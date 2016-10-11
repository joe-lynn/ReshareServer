
from marshmallow import fields, post_load, Schema, validates_schema, ValidationError
from sqlalchemy.dialects.postgresql import BIGINT, REAL, TEXT

from application import app, db

MAX_DESCRIPTION_LEN = 256
MIN_DESCRIPTION_LEN = 8
MAX_DETAILS_LEN = 2048
# TODO(stfinancial): Should we have a maximum price?

class ListingAddonSchema(Schema):
	addon_id = fields.Integer() # TODO(stfinancial): How is this compatible with BigInt
	listing_id = fields.Integer()
	description = fields.String()
	details = fields.String()
	price = fields.Float()
	
	@post_load
	def make_listing_addon(self, data):
		return ListingAddon(**data)
	
	@validates_schema
	def validate_input(self, data):
		if 'price' in data and data['price'] < 0:
			raise ValidationError('Invalid Price.')
		if 'description' not in data:
			raise ValidationError('Missing Description')
		if len(data['description']) > MAX_DESCRIPTION_LEN:
			raise ValidationError('Description too long.')
		if len(data['description']) < MIN_DESCRIPTION_LEN:
			raise ValidationError('Description too short.')
		if 'details' in data and len(data['details']) > MAX_DETAILS_LEN:
			raise ValidationError('Details too long.')

class ListingAddon(db.Model):
	addon_id = db.Column('addon_id', BIGINT, primary_key=True)
	listing_id = db.Column('listing_id', BIGINT, db.ForeignKey('listing.listing_id'), nullable=False)
	description = db.Column('description', TEXT(), nullable=False)
	details = db.Column('details', TEXT())
	price = db.Column('price', REAL(), default=0)
	
	def __init__(self, *args, **kwargs):
		self.listing_id = kwargs['listing_id']
		self.description = kwargs.get['description']
		self.details = kwargs.get('details', '')
		self.price = kwargs.get('price', 0)

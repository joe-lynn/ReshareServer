
from marshmallow import fields, post_load, Schema
from sqlalchemy.dialects.postgresql import BIGINT, REAL, TEXT

from application import app, db

class ListingAddonSchema(Schema):
	addon_id = fields.Integer() # TODO(stfinancial): How is this compatible with BigInt
	listing_id = fields.Integer()
	description = fields.String()
	details = fields.String()
	price = fields.Float()
	
	@post_load
	def make_listing_addon(self, data):
		return ListingAddon(**data)

# TODO(stfinancial): Need to make a decision about how to do defaults, should they be in the __init__
# or should they be set at the database level, or both?
class ListingAddon(db.Model):
	addon_id = db.Column('addon_id', BIGINT, primary_key=True)
	listing_id = db.Column('listing_id', BIGINT, db.ForeignKey('listing.listing_id'), nullable=False)
	description = db.Column('description', TEXT(), nullable=False)
	details = db.Column('details', TEXT())
	price = db.Column('price', REAL(), default=0)
	
	def __init__(self, *args, **kwargs):
		# TODO(stfinancial): Should we return false if listing_id is not provided? How can we fail?
		self.listing_id = kwargs.get('listing_id', 0)
		self.description = kwargs.get('description', '')
		self.details = kwargs.get('details', '')
		self.price = kwargs.get('price', 0)

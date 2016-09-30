from marshmallow import fields, post_load, Schema
from sqlalchemy.dialects.postgresql import BIGINT, INTEGER, TEXT

from application import app, db
from models.listing import Listing, ListingSchema

class ListingImageSchema(Schema):
	image_id = fields.Integer()
	listing_id = fields.Integer()
	url = fields.String()
	priority = fields.Integer()
	
	@post_load
	def make_listing_image(self, data):
		return ListingImage(**data)

class ListingImage(db.Model):
	image_id = db.Column('image_id', BIGINT, primary_key=True)
	listing_id = db.Column('listing_id', BIGINT, db.ForeignKey('listing.listing_id'), nullable=False)
	url = db.Column('url', TEXT, unique=True, nullable=False)
	priority = db.Column('priority', INTEGER, default=0)
	
	def __init__(self, *args, **kwargs):
		# TODO(stfinancial): Should we return false if listing_id is not provided? How can we fail?
		self.listing_id = kwargs.get('listing_id', 0)
		# TODO(stfinancial): Need to have a default URL or something?
		self.url = kwargs.get('url', '')
		self.priority = kwargs.get('priority', 0)
	
	def __repr__(self):
		return '<Listing Image %r>' % self.url


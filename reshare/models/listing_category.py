from application import app, db
from marshmallow import fields, post_load, Schema

from sqlalchemy.dialects.postgresql import BIGINT, VARCHAR

# TODO(stfinancial): Fix the name of this table.
describes = db.Table('describes',
	db.Column('listing_id', BIGINT, db.ForeignKey('listing.listing_id')),
	db.Column('category_id', BIGINT, db.ForeignKey('listing_category.category_id'))
)

class ListingCategorySchema(Schema):
	# TODO(stfinancial): Consider changing to 'id'
	category_id = fields.Integer()
	name = fields.String()
	
	@post_load
	def make_listing_category(self, data):
		return ListingCategory(**data)

class ListingCategory(db.Model):
	category_id = db.Column('category_id', BIGINT, primary_key=True)
	name = db.Column('name', VARCHAR(256), nullable=False, unique=True)
	
	# TODO(stfinancial): Not sure this is being done corretly, but we'll see.
	parent_id = db.Column('parent_id', BIGINT, db.ForeignKey('listing_category.category_id'))
	children = db.relationship('ListingCategory', backref='listing_category', lazy='dynamic')
	
	def __init__(self, *args, **kwargs):
		# Figure out how to create children in the constructor.
		self.name = kwargs.get('name', '')
	
	def __repr__(self):
		return '<ListingCategory %r>' % self.name

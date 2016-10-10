from marshmallow import fields, post_load, Schema, validates_schema, ValidationError
from sqlalchemy.dialects.postgresql import BIGINT, TEXT

from application import app, db

ROOT_CATEGORY_NAME = '#ROOT#'
MAX_CATEGORY_LENGTH = 256

# TODO(stfinancial): Fix the name of this table.
describes = db.Table('describes',
	db.Column('listing_id', BIGINT, db.ForeignKey('listing.listing_id')),
	db.Column('category_id', BIGINT, db.ForeignKey('listing_category.category_id'))
)

# TODO(stfinancial): Should the schema have the whole tree structure? What if we want to return just the name and id? Probably want either a "pre_dump" scrub of the data, or declare them as partial fields.
# TODO(stfinancial): CAN USE EXCLUDE when creating the object to exclude fields by name
class ListingCategorySchema(Schema):
	# TODO(stfinancial): Consider changing to 'id'
	category_id = fields.Integer()
	name = fields.String()
	parent_id = fields.Integer()
	# TODO(stfinancial): How do we get the root?
	# TODO(stfinancial): What is desired behavior here? Return all children? Probably
	children = fields.Nested('self', many=True)
		
	@post_load
	def make_listing_category(self, data):
		return ListingCategory(**data)

	@validates_schema
	def validate_input(self, data):
		if 'name' in data and len(data['name']) > MAX_CATEGORY_LENGTH:
			raise ValidationError('Category name is too long.')

class ListingCategory(db.Model):
	category_id = db.Column('category_id', BIGINT, primary_key=True)
	name = db.Column('name', TEXT(), nullable=False, unique=True)
	
	# TODO(stfinancial): Not sure this is being done corretly, but we'll see.
	parent_id = db.Column('parent_id', BIGINT, db.ForeignKey('listing_category.category_id'))
	children = db.relationship('ListingCategory', lazy='dynamic')
	
	def __init__(self, *args, **kwargs):
		# Figure out how to create children in the constructor.
		self.name = kwargs.get('name', '')
		# Child of the root by default.
		self.parent_id = kwargs.get('parent_id', None)
	
	def __repr__(self):
		return '<ListingCategory %r>' % self.name

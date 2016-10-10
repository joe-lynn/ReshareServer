from marshmallow import fields, post_load, Schema, validates_schema, ValidationError
from sqlalchemy.dialects.postgresql import BIGINT, TEXT

from application import app, db

MAX_CATEGORY_LENGTH = 256

# TODO(stfinancial): Fix the name of this table.
describes = db.Table('describes',
	db.Column('listing_id', BIGINT, db.ForeignKey('listing.listing_id')),
	db.Column('category_id', BIGINT, db.ForeignKey('listing_category.category_id'))
)

# TODO(stfinancial): Decide whether we want to show only 1 level of children, or all. (Exclude children in nested if not).
class ListingCategorySchema(Schema):
	# TODO(stfinancial): Consider changing to 'id'
	category_id = fields.Integer()
	name = fields.String()
	parent_id = fields.Integer()
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
	name = db.Column('name', TEXT(), nullable=False) # Not unique for now
	
	parent_id = db.Column('parent_id', BIGINT, db.ForeignKey('listing_category.category_id'))
	children = db.relationship('ListingCategory', lazy='dynamic')
	
	def __init__(self, *args, **kwargs):
		# Figure out how to create children in the constructor.
		self.name = kwargs.get('name', '')
		# Child of the root by default.
		self.parent_id = kwargs.get('parent_id', None)
	
	def __repr__(self):
		return '<ListingCategory %r>' % self.name

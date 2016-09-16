from application import app, db
from marshmallow import Schema, fields

# TODO(pallarino): Need to see whether to set as_string
class ListingSchema(Schema):
	# Add validations here, see: https://marshmallow.readthedocs.io/en/latest/quickstart.html#serializing-objects-dumping
	listing_id = fields.UUID()
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

class Listing(db.Model):
	listing_id = db.Column('listing_id', db.UUID(), primary_key=True)
	price_per_hour = db.Column('price_per_hour', db.REAL())
	price_per_day = db.Column('price_per_day', db.REAL())
	price_per_week = db.Column('price_per_week', db.REAL(), default=-1)
	maximum_time = db.Column('maximum_time', db.INTEGER)
	minimum_time = db.Column('minimum_time', db.INTEGER)
	
	has_delivery = db.Column('has_delivery', db.BOOLEAN(), default=False)
	delivery_price = db.Column('delivery_price', db.REAL(), default=0)
	
	late_fee = db.Column('late_fee', db.REAL())
	broken_price = db.Column('broken_price', db.REAL())

	title = db.Column('title', db.VARCHAR(512), nullable=False)
	description = db.Column('description', db.TEXT())
	
	is_closed = db.Column('is_closed', db.BOOLEAN(), default=False)
	creation_timestamp = db.Column('creation_timestamp', db.DateTime(timezone=True), nullable=False)

	def __init__(self, params):

	def __repr__(self):
		return '<Listing %r>' % self.listing_id
		


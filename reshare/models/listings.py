from application import app, db


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
	creation_timestamp = db.Column('creation_timestamp', timezone=True, nullable=False)

	def __init__(self, params):

	def __repr__(self):
		return '<Listing %r>' % self.listing_id
		


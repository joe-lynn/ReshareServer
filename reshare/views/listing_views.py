from flask import request
from flask_restful import Resource

from application import api, app, db
from instance.data.listings_data import fake_listings
from models.listing import Listing, ListingSchema

# TODO(stfinancial): Naming needs some serious work.

# Resource for getting multiple listings, could maybe wrap this into a single thing if we just check the parameters
class ListingsView(Resource):
	def get(self):
		# TODO(stfinancial): Handle query string (just look at request.args and process)
		try:
			listings = Listing.query.limit(10).all()
		except Exception as e:
			print e
			return 500
		schema = ListingSchema(many=True)
		result = schema.dump(listings)
		return result.data, 200 # TODO(stfinancial): Need to check for actual statuses
	
	# TODO(stfinancial): Do we use PUT instead to avoid double posts?
	def post(self):
		reqs = request.form
		schema = ListingSchema()
		listing = schema.load(reqs)
		try:
			db.session.add(listing.data)
			db.session.commit()
		except Exception as e:
			# TODO(stfinancial): Check for actual exceptions
			print e
			return 500
		return schema.dump(listing.data).data, 201 # TODO(stfinancial): Need to check for actual statuses

# Use to search for listings by ID
class ListingView(Resource):
	def get(self, listing_id):
		try:
			listing = Listing.query.get(listing_id)
		except Exception as e:
			print e
			return 500
		schema = ListingSchema()
		result = schema.dump(listing)
		return result.data, 200
	
	def delete(self, listing_id):
		listing = Listing.query.get(listing_id)
		try:
			db.session.delete(listing)
			db.session.commit()
		except Exception as e:
			# TODO(stfinancial): Handle the various exceptions properly
			print e
			return 500
		return 200

def bind_listing_views():
	api.add_resource(ListingsView, '/listings')
	api.add_resource(ListingView, '/listings/<int:listing_id>')


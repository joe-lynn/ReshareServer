
from application import api, app, db
from models.listings import ListingSchema, Listing
from instance.data.listings_data import fake_listings

from flask import request
from flask_restful import Resource

# TODO(pallarino): Naming needs some serious work.

# Resource for getting multiple listings, could maybe wrap this into a single thing if we just check the parameters
class ListingsView(Resource):
	def get(self):
		# TODO(pallarino): Handle query string (just look at request.args and process)
		listings = Listing.query.limit(10).all()
		schema = ListingSchema(many=True)
		result = schema.dump(listings)
		return result.data, 200 # TODO(pallarino): Need to check for actual statuses

# Currently this view's sole purpose is for creating listings, subject to change.
class CreateListing(Resource):
	# TODO(pallarino): Do we use PUT instead to avoid double posts?
	def post(self):
		reqs = request.form
		schema = ListingSchema()
		listing = schema.load(reqs)
		db.session.add(listing.data)
		db.session.commit()
		return 200 # TODO(pallarino): Need to check for actual statuses

# Use to search for listings by ID
class ListingView(Resource):
	def get(self, listing_id):
		listing = Listing.query.get(listing_id)
		schema = ListingSchema()
		result = schema.dump(listing)
		return result.data, 200
	
	def delete(self, listing_id):
		listing = Listing.query.get(listing_id)
		db.session.delete(listing)
		db.session.commit()
		return 200


def bind_listing_views():
	api.add_resource(ListingsView, '/listings')
	api.add_resource(CreateListing, '/listing')
	api.add_resource(ListingView, '/listing/<int:listing_id>')


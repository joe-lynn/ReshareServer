from application import api, app

from models.listings import ListingSchema, Listing

from flask import request
from flask_restful import Resource

# Add decorators to limit which http methods can be used.
class Listings(Resource):
	# Should I be using jsonify or something instead of these methods?
	def get(self):
		listings = Listing.query.limit(10).all()
		schema = ListingSchema(many=True)
		result = schema.dump(listings)
		return result.data, 200 # Need to check for actual statuses afaik

# Add decorators to limit which http methods can be used.
class Listing(Resource):
	def get(self):
		# Get the id of the listing and query the db
		# Serialize the result and return with a status

	def post(self):
		# Deserialize the incoming post (would this be in the URL or the request itself?)
		request.args # This gives me a dictionary of the parsed query string?
		# Create the Listing object
		# Add it to the database
		# Commit to the database
	
	# TODO(pallarino): Method to delete a listing from the database

api.add_resource(Listings, '/listings')
api.add_resource(Listing, '/listing')


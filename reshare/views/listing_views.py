from application import api, app, db

from models.listings import ListingSchema, Listing
from instance.data.listings_data import fake_listings

from flask import request
from flask_restful import Resource

# Add decorators to limit which http methods can be used.
class Listings(Resource):
	# Should I be using jsonify or something instead of these methods?
	def get(self):
		return fake_listings
		listings = Listing.query.limit(10).all()
		schema = ListingSchema(many=True)
		result = schema.dump(listings)
		return result.data, 200 # Need to check for actual statuses afaik

# Add decorators to limit which http methods can be used.
class ListingView(Resource):
	def get(self):
		# Get the id of the listing and query the db
		# Serialize the result and return with a status
		return "Getting ListingView"	
	
	def post(self):
		# Deserialize the incoming post (would this be in the URL or the request itself?)
		request.args # This gives me a dictionary of the parsed query string?
		# Create the Listing object
		
		
		# Add it to the database
		db.session.add(listing)
		
		# Commit to the database
		db.session.commit()
		
	# TODO(pallarino): Method to delete a listing from the database

class PostListing(Resource):
	def post(self):
		print "Posting Listing"
		reqs = request.form
		schema = ListingSchema()
		listing = schema.load(reqs)
		print listing.__class__.__name__
		print listing.data
		schema2 = ListingSchema()
		return schema2.dump(listing.data).data
		db.session.add(listing.data)
		db.session.commit()
		return 200
	def get(self):
		return 

class TestMethod(Resource):
	def get(self):
		return "Hello World"


def bind_listing_views():
	api.add_resource(TestMethod, '/')
	api.add_resource(PostListing, '/postListing')
	api.add_resource(Listings, '/listings')
	api.add_resource(ListingView, '/listing')


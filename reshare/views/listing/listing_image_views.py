from flask import request
from flask_restful import Resource

from application import api, app, db
from models.listing import Listing
from models.listing_image import ListingImage, ListingImageSchema

# TODO(stfinancial): Should this be deleting by image_id or by priority, seems weird to need to specify the global image id.
class ListingImageView(Resource):
	def delete(self, listing_id, image_id):
		return 501
	
	def get(self, listing_id, image_id):
		return 501
	
	def put(self, listing_id, image_id):
		return 501

class ListingImagesView(Resource):
	def get(self, listing_id):
		try:
			images = Listing.query.get(listing_id).images
		except Exception as e:
			print e
			return 500
		schema = ListingImageSchema(many=True)
		result = schema.dump(images)
		return result.data, 200
	
	def post(self, listing_id):
		# TODO(stfinancial): Check that listing_id actually exists.
		# TODO(stfinancial): Scrub and validate the data.
		# TODO(stfinancial): I'm thinking there should be a method to pare down to only fields which exist, then validation happens elsewhere.
		try:
			listing = Listing.query.get(listing_id)
			schema = ListingImageSchema()
			image = schema.load(request.form)
			image.data.listing_id = listing_id
			db.session.add(image.data)
			db.session.commit()
		except Exception as e:
			print e
			return 500
		return schema.dump(image.data).data, 200

def bind_views():
	api.add_resource(ListingImageView, '/listings/<int:listing_id>/images/<int:image_id>')
	api.add_resource(ListingImagesView, '/listings/<int:listing_id>/images')

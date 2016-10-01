from flask import request
from flask_restful import Resource

from application import api, app, db
from models.listing import Listing
from models.listing_image import ListingImage, ListingImageSchema

class ListingImageView(Resource):
	def delete(self, listing_id, image_id):
		return
	
	def get(self, listing_id, image_id):
		return
	
	def put(self, listing_id, image_id):
		returnr

class ListingImagesView(Resource):
	def get(self, listing_id):
		return
	
	def post(self, listing_id):
		return

def bind_listing_image_views():
	api.add_resource(ListingImageView, '/listings/<int:listing_id>/images/<int:image_id>')
	api.add_resource(ListingImagesView, '/listings/<int:listing_id>/images')

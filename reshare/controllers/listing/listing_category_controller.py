from flask import request
from flask_restful import Resource

from application import api, app, db
from models.listing import Listing
from models.listing_category import ListingCategory, ListingCategorySchema, ROOT_NAME

# TODO(stfinancial): Generic method to get resource and handle various errors
class ListingCategoryObjectController(Resource):
	# TODO(stfinancial): What is desired functionality? Delete all children, or make children children of parent?
	def delete(self, category_id):
		# TODO(stfinancial): Proper error codes here.
		try:
			category = ListingCategory.query.get(category_id)
		except Exception as e:
			print e
			return 500
		if category.name == ROOT_NAME:
			return "Cannot delete root node.", 500
		try:
			# TODO(stfinancial): Make sure this doesn't cascade (?)
			db.session.delete(category)
			db.session.commit()
		except Exception as e:
			print e
			return 500
		return 200
			
			

# TODO(stfinancial): Potentially rename this.
class ListingCategoryView(Resource):
	def delete(self, category_id):
		try:
			category = ListingCategory.query.get(category_id)
			db.session.delete(category)
			db.session.commit()
		except Exception as e:
			print e
			return 500
		return 200
	
	def get(self, category_id):
		try:
			category = ListingCategory.query.get(category_id)
			schema = ListingCategorySchema()
			result = schema.dump(category)
		except Exception as e:
			print e
			return 500
		return result.data, 200
	
	def put(self, category_id):
		return 501

class ListingCategoriesView(Resource):
	def get(self):
		return 501
	
	def post(self):
		return 501

def bind_resources():
	api.add_resource(ListingCategoryView, '/categories/<int:category_id>')
	api.add_resource(ListingCategoriesView, '/categories')

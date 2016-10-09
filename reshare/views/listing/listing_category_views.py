from flask import request
from flask_restful import Resource

from application import api, app, db
from models.listing import Listing
from models.listing_category import ListingCategory, ListingCategorySchema

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

def bind_views():
	api.add_resource(ListingCategoryView, '/categories/<int:category_id>')
	api.add_resource(ListingCategoriesView, '/categories')

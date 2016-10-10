from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from application import api, app, db
from models.listing import Listing
from models.listing_category import ListingCategory, ListingCategorySchema, ROOT_CATEGORY_NAME

# TODO(stfinancial): Need to check all these cases with tests and make sure we are returning the correct error codes as well as disallowing malicious behavior.


# TODO(stfinancial): How do we update the children of a category?

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
			# Update the parents of this node's children.
			category.children.parent = category.parent
			# TODO(stfinancial): Make sure this doesn't cascade (?)
			db.session.delete(category)
			db.session.commit()
		except Exception as e:
			print e
			return 500
		return 200

	def get(self, category_id):
		try:
			category = ListingCategory.query.get(category_id)
			# Exclude the children from the return value.
			# TODO(stfinancial): Parameter to ask for subtree.
			schema = ListingCategorySchema(exclude=('children',))
			result = schema.dump(category)
		except Exception as e:
			print e
			return 204
		return result.data, 200

	def put(self, category_id):
		# TODO(stfinancial): We just need to test how this works
		reqs = request.form
		# We can use the validate_schema to validate the input
		schema = ListingCategorySchema()
		try:
			new_category = schema.load(reqs)
			# This ensures that we cannot change the primary key value (we are modifying only the resource that the url references)
			# TODO(stfinancial): Make sure this works
			new_category.category_id = category_id
		except ValidationError as v:
			print v
			return 400
		except Exception as e:
			print e
			return 500

		try:
			#parent_category = ListingCategory.query.get()
			old_category = ListingCategory.query.get(category_id).update(new_category.data)
			db.session.commit()
		except Exception as e:
			# TODO(stfinancial): Need to check whether resource exists and then check commit error.
			print e
			return 500
		return new_category.data, 200

class ListingCategoryCollectionController(Resource):
	def get(self):
		schema = ListingCategorySchema(exclude=('children',), many=True)
		try:
			categories = ListingCategory.query.all()
		except Exception as e:
			print e
			return 500
		return schema.dump(categories).data, 200

	def post(self):
		# TODO(stfinancial): If no parent, then we need to make it a child of the root.
		reqs = request.form
		schema = ListingCategorySchema()
		try:
			category = schema.load(reqs)
			print category
		except ValidationError as v:
			print v
			return 400
		try:
			db.session.add(category.data)
			db.session.commit()
		except Exception as e:
			print e
			return 500
		return schema.dump(category.data).data, 200

def bind_resources():
	api.add_resource(ListingCategoryObjectController, '/categories/<int:category_id>')
	api.add_resource(ListingCategoryCollectionController, '/categories')
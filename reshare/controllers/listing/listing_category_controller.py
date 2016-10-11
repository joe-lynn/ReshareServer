from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from application import api, app, db
from models.listing import Listing
from models.listing_category import ListingCategory, ListingCategorySchema

# TODO(stfinancial): Need to check all these cases with tests and make sure we are returning the correct error codes as well as disallowing malicious behavior.


# TODO(stfinancial): How do we update the children of a category?

# TODO(stfinancial): Generic method to get resource and handle various errors
class ListingCategoryObjectController(Resource):
	def delete(self, category_id):
		# TODO(stfinancial): Proper error codes here.
		try:
			category = ListingCategory.query.get(category_id)
		except Exception as e:
			print e
			return 500
		try:
			# Update the parents of this node's children.
			category.children.update({'parent_id': category.parent_id})
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
			# TODO(stfinancial): Should we check if equal to 1?
			if request.args.get('flat', '1') != '0':
				schema = ListingCategorySchema(exclude=('children',))
			else:
				schema = ListingCategorySchema()
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
		except ValidationError as v:
			print v
			return 400
		except Exception as e:
			print e
			return 500
		if new_category.data.get('category_id', category_id) != category_id:
			return "Cannot modify Id", 400
		
		try:
			old_category = ListingCategory.query.get(category_id).update(new_category.data)
			db.session.commit()
		except Exception as e:
			# TODO(stfinancial): Need to check whether resource exists and then check commit error.
			print e
			return 500
		return new_category.data, 200

class ListingCategoryCollectionController(Resource):
	def get(self):
		try:
			categories = ListingCategory.query.all()
		except Exception as e:
			print e
			return 500
		# TODO(stfinancial): Unflattened doesn't work as I want, should only return root nodes and their subtree, not every node.
		if request.args.get('flat', '1') != '0':
			schema = ListingCategorySchema(exclude=('children',), many=True)
		else:
			schema = ListingCategorySchema(many=True)
		return schema.dump(categories).data, 200

	def post(self):
		# TODO(stfinancial): If no parent, then we need to make it a child of the root.
		reqs = request.form
		schema = ListingCategorySchema(exclude=('children'))
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

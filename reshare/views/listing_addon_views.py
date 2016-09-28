from flask import request
from flask_restful import Resource

from application import api, app, db
from models.listing import Listing
from models.listing_addon import ListingAddon, ListingAddonSchema

# TODO(stfinancial): This naming is a disaster, clean it up.
#	- Is "View" needed? Is it redundant?
#	- Do we need a separate class for creating a listing?
#	

class ListingAddonView(Resource):
	def delete(self, listing_id, addon_id):
		addon = ListingAddon.query.get(addon_id)
		db.session.delete(addon)
		db.session.commit()
		return 200
	
	def get(self, listing_id, addon_id):
		addon = ListingAddon.query.get(addon_id)
		schema = ListingAddonSchema()
		result = schema.dump(addon)
		return result.data, 200
	
	def put(self, listing_id, addon_id):
		reqs = request.form
		# TODO(stfinancial): Need to check if this can actually modify the primary key
		params = {}
		# TODO(stfinancial): Should we gracefully handle bad input or return error on invalid fields?
		addon = ListingAddon.query.get(addon_id)
		print addon
		print reqs
		if 'description' in reqs:
			addon.description = reqs['description']
		if 'details' in reqs:
			addon.details = reqs['details']
		if 'price' in reqs:
			addon.price = reqs['price']		
		db.session.commit()
		schema = ListingAddonSchema()
		result = schema.dump(addon)
		return result.data, 200	


class ListingAddonsView(Resource):
	def get(self, listing_id):
		addons = Listing.query.get(listing_id).addons
		schema = ListingAddonSchema(many=True)
		result = schema.dump(addons)
		return result.data, 200
	
	def post(self, listing_id):
		reqs = request.form
		# TODO(stfinancial): Should really return an error on invalid input here.
		params = {}
		params['listing_id'] = listing_id
		params['description'] = reqs.get('description', '')
		params['details'] = reqs.get('details', '')
		params['price'] = reqs.get('price', 0)
		schema = ListingAddonSchema()
		addon = schema.load(params)
		db.session.add(addon.data)
		db.session.commit()
		return 200

def bind_listing_addon_views():
	api.add_resource(ListingAddonView, '/listings/<int:listing_id>/addons/<int:addon_id>')
	api.add_resource(ListingAddonsView, '/listings/<int:listing_id>/addons')

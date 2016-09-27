from flask import request
from flask_restful import Resource

from application import api, app, db
from models.listing import Listing
from models.listing_addon import ListingAddon, ListingAddonSchema

# TODO(stfinancial): This naming is a disaster, clean it up.
#	- Is "View" needed? Is it redundant?
#	- Do we need a separate class for creating a listing?
#	
class CreateListingAddon(Resource):
	# TODO(stfinancial): Do we use PUT instead to avoid double posts?
	def post(self, listing_id):
		return

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
		# TODO(stfinancial): Need to update only those fields that actually exist, check that this won't do wacky things if bad parameters are provided
		db.session.query(ListingAddon).filter(ListingAddon.addon_id == addon_id).update(reqs)
	

class ListingAddonsView(Resource):
	def get(self, listing_id):
		addons = Listing.query.get(listing_id).addons
		schema = ListingAddonSchema(many=True)
		result = schema.dump(addons)
		return result.data, 200
	
	def post(self, listing_id):
		reqs = request.form
		# TODO(stfinancial): Should really return an error on invalid input here.
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
	api.add_resource(ListingAddonView, '/listing/<int:listing_id>/addon/<int:addon_id>')
	api.add_resource(ListingAddonsView, '/listing/<int:listing_id>/addons')

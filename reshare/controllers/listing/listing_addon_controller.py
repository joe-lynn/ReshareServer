from flask import request
from flask_restful import Resource

from application import api, app, db
from models.listing import Listing
from models.listing_addon import ListingAddon, ListingAddonSchema

# TODO(stfinancial): This naming is a disaster, clean it up.
#	- Is "View" needed? Is it redundant?
#	- Do we need a separate class for creating a listing?
#	

# TODO(stfinancial): Are these controllers or views?
class ListingAddonObjectController(Resource):
	def delete(self, listing_id, addon_id):
		try:
			addon = ListingAddon.query.get(addon_id)
		except Exception as e:
			# TODO(stfinancial): Handle the various kinds of errors
			print e
			return 500
		try:
			db.session.delete(addon)
			db.session.commit()
		except Exception as e:
			print e
			return 500
		return 200
	
	# TODO(stfinancial): Why even require the addon_id?
	def get(self, listing_id, addon_id):
		try:
			addon = ListingAddon.query.get(addon_id)
			schema = ListingAddonSchema()
			result = schema.dump(addon)
		except Exception as e:
			print e
			return 500
		return result.data, 200
	
	def put(self, listing_id, addon_id):
		# TODO(stfinancial): At a certain point it may be faster to just copy valid fields
		reqs = request.form
		schema = ListingAddonSchema()
		try:
			new_addon = schema.load(reqs)
		except ValidationError as v:
			print v
			return 400
		except Exception as e:
			print e
			return 500
		if new_addon.data.get('listing_id', listing_id) != listing_id:
			return "Cannot modify listing id", 400
		if new_addon.data.get('addon_id', addon_id) != addon_id:
			return "Cannot modify addon id", 400
		try:
			old_addon = ListingAddon.query.get(addon_id).update(new_addon.data)
			db.session.commit()
		except Exception as e:
			print e
			return 500
		return new_addon.data, 200

class ListingAddonCollectionController(Resource):
	def get(self, listing_id):
		try:
			addons = Listing.query.get(listing_id).addons #.all()
			schema = ListingAddonSchema(many=True)
			result = schema.dump(addons)
		except Exception as e:
			print e
			return 500
		return result.data, 200
	
	def post(self, listing_id):
		reqs = request.form
		schema = ListingAddonSchema()
		try:
			addon = schema.load(reqs)
			db.session.add(addon.data)
			db.session.commit()
		except ValidationError as v:
			print v
			return 400
		except Exception as e:
			print e
			return 500
	# TODO(stfinancial): Delete to get rid of all addons for a listing.

def bind_resources():
	api.add_resource(ListingAddonObjectController, '/listings/<int:listing_id>/addons/<int:addon_id>')
	api.add_resource(ListingAddonCollectionController, '/listings/<int:listing_id>/addons')

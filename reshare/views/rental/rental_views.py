from flask import request
from flask_restful import Resource

from application import api, app, db
from models.rental import Rental

# TODO(stfinancial): Should we also be taking in a listing_id as well, or is /rental/<rental_id> ok?
class RentalView(Resource):
	def delete(self, rental_id):
		return 501
	
	def get(self, rental_id):
		return 501
	
	def put(self, rental_id):
		return 501

class RentalsView(Resource):
	def get(self):
		# TODO(stfinancial): Not even sure if this should be implemented.
		return 501
	
	def post(self):
		return 501
	
def bind_views():
	api.add_resource(RentalView, '/rentals/<int:rental_id>')
	api.add_resource(RentalsView, '/rentals')

import requests
import unittest

# TODO(stfinancial): Move to a testing constants file.

SERVER_ADDRESS = 'http://ec2-52-53-152-157.us-west-1.compute.amazonaws.com'

class TestListing(unittest.TestCase):
	def testPostListing(self):
		data = {'price_per_hour':5, 'maximum_time':5, 'minimum_time':1, 'delivery_price':10, 'title':'Test Title', 'description':'Titles for rent'}
		r = requests.post(SERVER_ADDRESS + '/listings', data)
		self.assertEqual(r.status_code, 201)
		self.assertTrue(r.json()['listing_id'] > 0)
		self.assertTrue(r.json()['price_per_hour'] == 5)
		r = requests.delete(SERVER_ADDRESS + '/listings/' + str(r.json()['listing_id']))
		self.assertEqual(r.status_code, 200)
	
	def testPostBadInput(self):
		data = {'price_per_hr':5}
		r = requests.post(SERVER_ADDRESS + '/listings', data)

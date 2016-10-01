import requests
import unittest

# TODO(stfinancial): Move to a testing constants file.

SERVER_ADDRESS = 'http://ec2-52-53-152-157.us-west-1.compute.amazonaws.com'

class TestListingViews(unittest.TestCase):
	def testPostListing(self):
		data = {'price_per_hour':5, 'maximum_time':5, 'minimum_time':1, 'delivery_price':10, 'title':'Test Title', 'description':'Titles for rent'}
		r = requests.post(SERVER_ADDRESS + '/listings', data)
		print r.content

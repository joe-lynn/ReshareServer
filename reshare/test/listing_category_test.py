import requests
import unittest

from constants.testing_constants import SERVER_ADDRESS

# TODO(stfinancial): Move to constants
CATEGORIES_ADDRESS = SERVER_ADDRESS + '/categories'

ROOT = {'name': 'root'}
CHILD_1 = {'name': 'child1'}
CHILD_2 = {'name': 'child2'}
GRANDCHILD_1 = {'name': 'grandchild1'}
GRANDCHILD_2 = {'name': 'grandchild2'}
GRANDCHILD_3 = {'name': 'grandchild3'}

INVALID_PARENT = {'name': 'ip', 'parent_id': 123456789}

def GetById(category_id):
	return CATEGORIES_ADDRESS + '/' + str(category_id)

# TODO(stfinancial): We will probably want some assertRaises on bad input.
class TestListingCategory(unittest.TestCase):
	# Test posting, deleting, and getting a category.
	def testPostCategory(self):
		r = requests.post(CATEGORIES_ADDRESS, ROOT)
		self.assertEqual(r.status_code, 200)
		self.assertIsNone(r.json()['parent_id'])
		root_id = r.json().get('category_id', 0)
		self.assertTrue(root_id > 0)
		r = requests.delete(GetById(root_id))
		self.assertEqual(r.status_code, 200)
		r = requests.get(GetById(root_id))
		self.assertEqual(r.json(), {})
	
	# Test that children are assigned new parent_id on parent being deleted
	def testUpdateParentOnDelete(self):
		r = requests.post(CATEGORIES_ADDRESS, ROOT)
		root_id = r.json()['category_id']
		child_node = CHILD_1.copy()
		child_node['parent_id'] = root_id
		r = requests.post(CATEGORIES_ADDRESS, child_node)
		child_id = r.json()['category_id']
		grandchild_node = GRANDCHILD_1.copy()
		grandchild_node['parent_id'] = child_id
		r = requests.post(CATEGORIES_ADDRESS, grandchild_node)
		gc_id = r.json()['category_id']
		r = requests.delete(GetById(child_id))
		r = requests.get(GetById(gc_id))
		self.assertEqual(r.json()['parent_id'], root_id)
	
	# Test that we can't modify the category id.
	def testChangeId(self):
		r = requests.post(CATEGORIES_ADDRESS, ROOT)
		root_id = r.json()['category_id']
		r = requests.put(GetById(root_id), {'category_id': root_id + 10000})
		self.assertEqual(r.status_code, 500)
	
	# Test that the parent must exist.
	def testParentMustExist(self):
		# TODO(stfinancial): What is the desired behavior here? Fail or null parent?
		r = requests.post(CATEGORIES_ADDRESS, INVALID_PARENT)
		self.assertEqual(r.status_code, 500)	
		
		

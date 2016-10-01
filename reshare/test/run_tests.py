import unittest
from listing_views_test import TestListingViews

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TestListingViews)
	unittest.TextTestRunner(verbosity=2).run(suite)

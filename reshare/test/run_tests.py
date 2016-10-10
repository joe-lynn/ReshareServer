import unittest

from listing_test import TestListing
from listing_category_test import TestListingCategory

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TestListing)
	suite = unittest.TestLoader().loadTestsFromTestCase(TestListingCategory)
	unittest.TextTestRunner(verbosity=2).run(suite)


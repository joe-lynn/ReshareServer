from controllers.listing.listing_addon_controller import bind_resources as br_listing_addon
from controllers.listing.listing_category_controller import bind_resources as br_listing_category
from controllers.listing.listing_image_controller import bind_resources as br_listing_image
from controllers.listing.listing_controller import bind_resources as br_listing

def bind_resources():
	br_listing()
	br_listing_addon()
	br_listing_category()
	br_listing_image()

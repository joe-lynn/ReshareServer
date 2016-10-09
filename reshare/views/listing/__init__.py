from views.listing.listing_addon_views import bind_views as bv_listing_addon
from views.listing.listing_category_views import bind_views as bv_listing_category
from views.listing.listing_image_views import bind_views as bv_listing_image
from views.listing.listing_views import bind_views as bv_listing

def bind_views():
	bv_listing()
	bv_listing_addon()
	bv_listing_category()
	bv_listing_image()

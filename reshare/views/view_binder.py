from views.listing_addon_views import bind_listing_addon_views
from views.listing_views import bind_listing_views

def bind_views():
	bind_listing_views()
	bind_listing_addon_views()

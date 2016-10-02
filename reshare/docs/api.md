# Public API #
## Listings ##
**By Query String**

To receive the listings. Currently there are no criteria to filter upon, but filtering by date, distance, category, and id will be coming soon. Results in the form of:

`[{"listing_id": 1, "description": "", "title": "thedankest", "price_per_week": -1.0, "price_per_day": -1.0, "has_delivery": false, "minimum_time": 1, "delivery_price": 0.0, "maximum_time": 7, "late_fee": 0.0, "broken_price": 0.0, "price_per_hour": -1.0, "creation_timestamp": "2016-09-30T04:23:25.709966+00:00", "is_closed": false}]`

`Call: http://ec2-52-53-152-157.us-west-1.compute.amazonaws.com/listings`

**By Id**

Gets the listing at the specified id.

`Call: http://ec2-52-53-152-157.us-west-1.compute.amazonaws.com/listings/<listing_id>`

# User API #
## Listings ##

Unimplemented as private calls.

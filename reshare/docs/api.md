## Note that Required Parameters are marked with an asterisk \(\*\) ##
# Public API #
## Listings ##

#### GET ####
**By Query String**

Currently there are no criteria to filter upon, but filtering by date, distance, category, and id will be coming soon. Results in the form of:

`[{"listing_id": 1, "description": "", "title": "thedankest", "price_per_week": -1.0, "price_per_day": -1.0, "has_delivery": false, "minimum_time": 1, "delivery_price": 0.0, "maximum_time": 7, "late_fee": 0.0, "broken_price": 0.0, "price_per_hour": -1.0, "creation_timestamp": "2016-09-30T04:23:25.709966+00:00", "is_closed": false}]`

**By Id**
Available at:

`Call: http://ec2-52-53-152-157.us-west-1.compute.amazonaws.com/listings/<listing_id>`

# User API #
## Listings ##

#### POST ####
**Not currently private**: POST parameters are as follows:

*title\*:* Title of the listing as it will be shown in the listing directory.

*description:* Text describing the listing.

*price_per_week:* Price, in USD, per week.

*price_per_day:* Price, in USD, per day.

*price_per_hour:* Price, in USD, per hour.

*has_delivery:* Whether the renter offers delivery for the listing.

*delivery_price:* Additional cost, in USD, of delivery.

*minimum_time:* The minimum amount of time for rental, corresponds to the most granular positive price.

*maximum_time:* The maximum amount of time for rental, corresponds to the least granular positive price.

*late_fee:* Fee charged, in USD, upon an item reaching late status.

*broken_price:* Price corresponding to this item being broken.

`Call: http://ec2-52-53-152-157.us-west-1.compute.amazonaws.com/listings`

#### PUT ####

Modify the listing with the given id:

`Call: http://ec2-52-53-152-157.us-west-1.compute.amazonaws.com/listings/<listing_id>`

#### DELETE ####

Delete the listing with the given id:

`Call: http://ec2-52-53-152-157.us-west-1.compute.amazonaws.com/listings/<listing_id>`

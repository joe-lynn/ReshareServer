DROP TABLE IF EXISTS listing_addon;
DROP TABLE IF EXISTS listing;

-- A listing is what a renter posts to put an item up for rent.
-- This means that items are encapsulated within listings.
CREATE TABLE listing(
	-- TODO(pallarino): Need some check constraints.
	listing_id		BIGINT	SERIAL,

	title			TEXT	NOT NULL,

	price_per_hour	REAL	DEFAULT -1,
	price_per_day	REAL	DEFAULT -1,
	price_per_week	REAL 	DEFAULT -1,
	maximum_time	INTEGER	DEFAULT 7,
	minimum_time	INTEGER	DEFAULT 1,

	-- Should delivery be a listing_addon that is simply created along with the listing
	-- if the renter chooses to check the "provide delivery" box?
	-- TODO(stfinancial): I'm thinking so.
	has_delivery	BOOLEAN	DEFAULT False,
	delivery_price	REAL	DEFAULT 0,
	late_fee		REAL	DEFAULT 0,
	broken_price	REAL	DEFAULT 0,

	description		TEXT	DEFAULT '',
	creation_timestamp	timestamp	NOT NULL,

	PRIMARY KEY listing_id
);

-- A listing addon is an optional addition to an order (e.g. cleaning/refill)
CREATE TABLE listing_addon(
	addon_id		BIGINT	SERIAL,
	listing_id		BIGINT	NOT NULL,
	description		TEXT	NOT NULL,
	details			TEXT,
	price			REAL	DEFAULT 0,

	PRIMARY KEY addon_id,
	FOREIGN KEY listing_id REFERENCES listing ON DELETE CASCADE
);
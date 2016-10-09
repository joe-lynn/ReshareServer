DROP TABLE IF EXISTS rental;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS listing_image;
DROP TABLE IF EXISTS describes;
DROP TABLE IF EXISTS listing_category;
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

-- A listing category is the category under which a listing has been placed.
-- Currently a listing may have more than one category but it might make sense to roll
-- into a single category to simplify the database for now, though in the future
-- we will probably want many properties to describe a listing.
CREATE TABLE listing_category(
	category_id		BIGINT	SERIAL,
	name			VARCHAR(256) UNIQUE NOT NULL,
	parent_id		BIGINT,

	PRIMARY KEY category_id,
	FOREIGN KEY parent_id REFERENCES listing_category
);

-- Table creating a many-to-many relationship between listings and listing categories.
CREATE TABLE describes(
	listing_id		BIGINT	SERIAL,
	category_id		BIGINT	SERIAL,

	PRIMARY KEY listing_id, category_id,
	FOREIGN KEY listing_id REFERENCES listing ON DELETE CASCADE,
	FOREIGN KEY category_id REFERENCES listing_category
);

-- Table describing the images on a listing. The images will be stored on the web
-- server. Priority is defined as the order in which a image is listed. The lower, the earlier.
CREATE TABLE listing_image(
	image_id		BIGINT	SERIAL,
	listing_id		BIGINT	SERIAL,

	url			TEXT	UNIQUE NOT NULL,
	priority		INTEGER	DEFAULT 0,
	
	FOREIGN KEY listing_id REFERENCES listing,
);

CREATE TABLE user(
	user_id		BIGINT	SERIAL,
	username	TEXT	UNIQUE	NOT NULL,
	password	TEXT	NOT NULL,

	PRIMARY KEY user_id,
);

CREATE TABLE rental(
	rental_id		BIGINT	SERIAL,
	listing_id		BIGINT	SERIAL,
	owner_id		BIGINT	SERIAL,
	renter_id		BIGINT	SERIAL,
	
	start_timestamp		timestamp	NOT NULL,
	end_timestamp		timestamp,
	amount_paid		REAL	DEFAULT NULL,
	
	rating			INTEGER	DEFAULT NULL,
	comment			TEXT	DEFAULT '',
	comment_timestamp	timestamp	DEFAULT NULL,
	
	PRIMARY KEY rental_id,
	FOREIGN KEY listing_id REFERENCES listing,
	FOREIGN KEY owner_id REFERENCES user,
	FOREIGN KEY renter_id REFERENCES user,
);

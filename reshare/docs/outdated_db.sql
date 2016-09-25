DROP TABLE IF EXISTS rents;
DROP TABLE IF EXISTS listing_price;
DROP TABLE IF EXISTS listing_image;
DROP TABLE IF EXISTS listing_addon;
DROP TABLE IF EXISTS listing;
DROP TABLE IF EXISTS card;
DROP TABLE IF EXISTS setting;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS account_credentials;
DROP TABLE IF EXISTS account_image;
DROP TABLE IF EXISTS account;
DROP TYPE IF EXISTS price_unit;
DROP TYPE IF EXISTS privilege;

CREATE TYPE privilege AS ENUM ('user', 'mod', 'admin', 'owner');
CREATE TYPE price_unit AS ENUM ('hour', 'day');

-- TODO(pallarino): Start to include indexes.
-- TODO(pallarino): Think carefully about on delete cascade, which data will we want to keep long term.

-- Definitely missing some stuff from original file
-- There should be another type defined here but I forgot what it was
CREATE TABLE account (
	account_id	uuid		NOT NULL,
	dob			date,
	level		privilege	DEFAULT 'user',
	first_name	VARCHAR(64),
	last_name	VARCHAR(64),
	email		VARCHAR(128),
	description text,
	PRIMARY KEY (account_id)
);

CREATE TABLE account_image (
    account_id  uuid REFERENCES account ON DELETE CASCADE NOT NULL,
    image_id    uuid NOT NULL,
    image_url   text UNIQUE NOT NULL,
    PRIMARY KEY (image_id)
);

CREATE TABLE account_credentials (
    username        VARCHAR(64) NOT NULL UNIQUE,
    password_hash   INTEGER     NOT NULL UNIQUE,
    account_id      uuid        REFERENCES account ON DELETE CASCADE NOT NULL,
    PRIMARY KEY(account_id)
);

CREATE TABLE messages (
	sender_id		uuid		NOT NULL,
	receiver_id		uuid		NOT NULL,
	message_hash	INTEGER 	NOT NULL,
	sent_time		timestamptz	NOT NULL,
	message			text		NOT NULL,
	PRIMARY KEY (message_hash, sent_time),
	FOREIGN KEY (sender_id) REFERENCES account,
	FOREIGN KEY (receiver_id) REFERENCES account
);

CREATE TABLE setting (
	email_on_message	BOOLEAN		DEFAULT false,
	account_id			uuid		NOT NULL,
	PRIMARY KEY (account_id),
	FOREIGN KEY (account_id) REFERENCES account
);

CREATE TABLE card (
	last_4_digits	VARCHAR(4)	NOT NULL,
	name_on_card	VARCHAR(64)	NOT NULL,
	expiration		VARCHAR(4)	NOT NULL,
	next_token		INTEGER,
	cc_id			uuid		NOT NULL,
	account_id		uuid		REFERENCES account ON DELETE CASCADE NOT NULL,
	PRIMARY KEY (cc_id)
);

/* 
 * A listing is an item, and this is what a renter posts when they want
 * to rent out an item.
 */
CREATE TABLE listing (
	listing_id	uuid,

	-- TODO(pallarino): Checks for pricing constraints
	-- Pricing Information
	price_per_hour	REAL,
	price_per_day	REAL,
	price_per_week	REAL	DEFAULT -1,
	maximum_time	INTEGER, -- Corresponds to the highest nonzero price.
	minimum_time	INTEGER, -- Corresponds to the lowest nonzero price.
	
	-- Use negative price as no delivery?
	has_delivery	BOOLEAN DEFAULT False,
	delivery_price	REAL	DEFAULT 0,	
	
	-- Fields about late listings
	late_fee	REAL,
	broken_price	REAL,
	
	-- Fields corresponding to user inserted text
	title		VARCHAR(512)	NOT NULL,
	description	text,
	
	-- Fields that will likely not be exposed to the user
	is_closed	BOOLEAN		DEFAULT False,
	creation_timestamp  timestamptz NOT NULL,
	
	-- TODO(pallarino): Fields for holding data post rental
	-- E.g. which addons were taken(separate entry?), was delivery used, etc.

	-- Most likely will index on listing_id
	PRIMARY KEY (listing_id)
);

/*
 * User defined additions to listings. These will be selected by the rentee
 * if they so choose.
 */
CREATE TABLE listing_addon {
	addon_id	uuid		NOT NULL,
	listing_id	uuid		NOT NULL,
	name		VARCHAR(128)	NOT NULL,

	-- Current default is single flat price for an addon.
	price		REAL		NOT NULL,
	
	FOREIGN KEY(listing_id) REFERENCES listing ON DELETE CASCADE,
	PRIMARY KEY(addon_id)
};

/*
 * Image corresponding to a listing.
 */
CREATE TABLE listing_image (
	listing_id	uuid NOT NULL,
	image_id	uuid NOT NULL,
	
	-- URL on the web server containing the image.
	image_url	uuid UNIQUE NOT NULL,
	
	-- Priority is the position at which the picture is shown for a listing.
	priority	INTEGER,
	
	FORIEGN KEY(listing_id) REFERENCE listing ON DELETE CASCADE,
	PRIMARY KEY(image_id)
);

CREATE TABLE listing_price (
	listing_id		uuid		REFERENCES listing ON DELETE CASCADE NOT NULL,
	price_id        uuid        NOT NULL,
	dollar_per_unit	REAL,
	unit			price_unit	NOT NULL,
	PRIMARY KEY (price_id)
);

CREATE TABLE rents (
	account_id		uuid		NOT NULL,
	listing_id		uuid		NOT NULL,
	rental_id		uuid		NOT NULL,
	start_timestamp timestamptz 	NOT NULL,
	end_timestamp	timestamptz,
	amount_paid		REAL,
	broken			BOOLEAN 	DEFAULT false,
	PRIMARY KEY (rental_id),
	FOREIGN KEY (account_id) REFERENCES account,
	FOREIGN KEY (listing_id) REFERENCES listing
);

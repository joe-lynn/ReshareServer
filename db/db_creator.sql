DROP TABLE IF EXISTS rents;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS listing_price;
DROP TABLE IF EXISTS listing;
DROP TABLE IF EXISTS card;
DROP TABLE IF EXISTS setting;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS account;
DROP TYPE IF EXISTS price_unit;
DROP TYPE IF EXISTS privilege;

CREATE TYPE privilege AS ENUM ('user', 'mod', 'admin', 'owner');
CREATE TYPE price_unit AS ENUM ('hour', 'day');

-- Definitely missing some stuff from original file
-- There should be another type defined here but I forgot what it was
CREATE TABLE account(
	account_id	uuid		NOT NULL,
	username	VARCHAR(64) NOT NULL	UNIQUE,
	dob			date,
	level		privilege	DEFAULT 'user',
	first_name	VARCHAR(64),
	last_name	VARCHAR(64),
	email		VARCHAR(128),
	description bytea,
	profile_pic	bytea,
	PRIMARY KEY (account_id)
);

CREATE TABLE messages (
	sender_id		uuid		NOT NULL,
	receiver_id		uuid		NOT NULL,
	message_hash	INTEGER 	NOT NULL,
	sent_time		timestamptz	NOT NULL,
	message			bytea		NOT NULL,
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

CREATE TABLE listing (
	listing_id		uuid			NOT NULL,
	price			REAL			NOT NULL,
	broken_price	REAL,
	images			bytea, -- Need to move this to its own table
	description		bytea,
	name			VARCHAR(256)	NOT NULL,
	PRIMARY KEY (listing_id)
);

CREATE TABLE listing_price (
	listing_id		uuid		REFERENCES listing ON DELETE CASCADE NOT NULL,
	dollar_per_unit	REAL,
	unit			price_unit	NOT NULL,
	PRIMARY KEY (listing_id, unit)
);

CREATE TABLE posts (
	listing_id			uuid		NOT NULL,
	account_id			uuid		NOT NULL,
	creation_timestamp	timestamptz	NOT NULL,
	FOREIGN KEY (listing_id) REFERENCES listing,
	FOREIGN KEY (account_id) REFERENCES account,
	PRIMARY KEY (listing_id, account_id)
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

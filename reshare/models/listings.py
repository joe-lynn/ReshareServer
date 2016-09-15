from application import app, db


class Listing(db.Model):
	listing_id = db.Column(db.UUID, primary_key=True)
	


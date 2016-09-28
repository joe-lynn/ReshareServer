from application import db
from models import listing_category
from models import listing_addon
from models import listing

db.drop_all()
db.create_all()

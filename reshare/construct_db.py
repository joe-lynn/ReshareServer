from application import db
from models import listings

db.drop_all()
db.create_all()

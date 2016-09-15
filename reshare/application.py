from flask import Flask
from instance.db_config import items_config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(items_config['user'], items_config['password'], items_config['host'], items_config['port'], items_config['db_name']
db = SQLAlchemy(app)

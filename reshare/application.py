from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from instance.db_config import items_config

app = Flask(__name__)
api = Api(app)

print items_config

# This might be postgresql+psycopg2
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(items_config['user'], items_config['password'], items_config['host'], items_config['port'], items_config['db_name'])
print app.config['SQLALCHEMY_DATABASE_URI']
db = SQLAlchemy(app)



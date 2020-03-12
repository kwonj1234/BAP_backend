import os 
from models import ORM
from flask_app import app

PATH = os.path.dirname(__file__)
DBPATH = os.path.join(PATH, "data", "recipes.db")

ORM.dbpath = DBPATH

app.run(debug=True)
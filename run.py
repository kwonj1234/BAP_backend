import os 
from flask_app import app
from models import ORM, Recipe, User, Saved_Recipes, Recipe_Instructions


PATH = os.path.dirname(__file__)
DBPATH = os.path.join(PATH, "data", "recipes.db")

ORM.dbpath = DBPATH
Recipe.dbpath = DBPATH
Recipe_Instructions.dbpath = DBPATH
# Recipe_Ingredients.dbpath = DBPATH
User.dbpath = DBPATH
Saved_Recipes.dbpath = DBPATH

if __name__ == "__main__":
    app.run(debug=True)
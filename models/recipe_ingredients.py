import sqlite3
from .ORM import ORM

class Recipe_Ingredients(ORM):
    tablename = "recipe_ingredients"
    dbpath = "data/recipes.db"
    fields = ["pk", "name", "amount", "unit", "recipe_pk"]

    def __init__(self, **kwargs):
        self.pk = kwargs.get("pk")
        self.name = kwargs.get("name")
        self.amount = kwargs.get("amount")
        self.unit = kwargs.get("unit")
        self.recipe_pk = kwargs.get("recipe_pk")
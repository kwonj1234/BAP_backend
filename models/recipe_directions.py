import sqlite3
from .ORM import ORM

class Recipe_Directions(ORM):
    tablename = "recipe_directions"
    dbpath = "data/recipes.db"
    fields = ["pk", "direction", "duration", "recipe_pk"]

    def __init__(self, **kwargs):
        self.pk = kwargs.get("pk")
        self.direcion = kwargs.get("direction")
        self.duration = kwargs.get("duration")
        self.recipe_pk = kwargs.get("recipe_pk")
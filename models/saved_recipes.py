import sqlite3
from .ORM import ORM

class Saved_Recipes(ORM):
    tablename = "saved_recipes"
    dbpath = ""
    fields = ["pk", "user_pk", "recipe_pk"]

    def __init__(self, **kwargs):
        self.pk = kwargs.get("pk")
        self.user_pk = kwargs.get("user_pk")
        self.recipe_pk = kwargs.get("recipe_pk")
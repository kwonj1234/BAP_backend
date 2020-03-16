import sqlite3
from .ORM import ORM

class Recipe_Instructions(ORM):
    tablename = "recipe_instructions"
    dbpath = ""
    fields = ["pk", "instruction", "duration", "recipe_pk"]

    def __init__(self, **kwargs):
        self.pk = kwargs.get("pk")
        self.instruction = kwargs.get("instruction")
        self.duration = kwargs.get("duration")
        self.recipe_pk = kwargs.get("recipe_pk")
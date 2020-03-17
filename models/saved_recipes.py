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
    
    @classmethod
    def no_repeat_saves(cls, user_pk, recipe_pk):
        with sqlite3.connect(cls.dbpath) as conn:
            cur = conn.cursor()
            sql = f"""SELECT pk FROM {cls.tablename} 
                WHERE user_pk = ? and recipe_pk = ?"""
            cur.execute(sql, (user_pk, recipe_pk))
            repeat = cur.fetchone()
            if repeat is None:
                return False
            return True
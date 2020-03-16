import sqlite3
from .ORM import ORM

class Recipe(ORM):
    tablename = "recipe"
    dbpath = ""
    fields = ["pk", "name", "source", "culture", "img_path", "serving_size", "total_time", "ingredients"]

    def __init__(self, **kwargs):
        self.pk = kwargs.get("pk")
        self.name = kwargs.get("name")
        self.source = kwargs.get("source")
        self.culture = kwargs.get("culture")
        self.img_path = kwargs.get("img_path")
        self.serving_size = kwargs.get("serving_size")
        self.total_time = kwargs.get("total_time")
        self.ingredients = kwargs.get("ingredients")
    
    @classmethod
    def no_repeat_recipe(cls, source):
        with sqlite3.connect(cls.dbpath) as conn:
            cur = conn.cursor()
            sql = f"""SELECT pk FROM {cls.tablename} WHERE source == ?"""
            cur.execute(sql, (source,))
            repeat = cur.fetchone()
            if repeat is None:
                return False
            return True
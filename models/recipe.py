import sqlite3
from .ORM import ORM

class Recipe(ORM):
    tablename = "recipe"
    dbpath = ""
    fields = ["pk", "name", "url", "culture", "img_path", "serving_size", "total_time"]

    def __init__(self, **kwargs):
        self.pk = kwargs.get("pk")
        self.name = kwargs.get("name")
        self.url = kwargs.get("url")
        self.culture = kwargs.get("culture")
        self.img_path = kwargs.get("img_path")
        self.serving_size = kwargs.get("serving_size")
        self.total_time = kwargs.get("total_time")
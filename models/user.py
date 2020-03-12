import sqlite3
from .ORM import ORM

class User(ORM):
    tablename = "user"
    dbpath = "data/recipes.db"
    fields = ["pk", "username", "password", "email"]

    def __init__(self, **kwargs):
        self.pk = kwargs.get("pk")
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")
        self.email = kwargs.get("email")
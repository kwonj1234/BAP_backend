import sqlite3
from .ORM import ORM

class User(ORM):
    tablename = "user"
    dbpath = "data/recipes.db"
    fields = ["pk", "username", "password", "salt", "fname", "lname", "email"]

    def __init__(self, **kwargs):
        self.pk = kwargs.get("pk")
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")
        self.salt = kwargs.get("salt")
        self.fname = kwargs.get("fname")
        self.lname = kwargs.get("lname")
        self.email = kwargs.get("email")
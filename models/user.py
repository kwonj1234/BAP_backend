import sqlite3
from .ORM import ORM

class User(ORM):
    tablename = "user"
    dbpath = ""
    fields = ["pk", "username", "password", "salt", "fname", "lname", "email"]

    def __init__(self, **kwargs):
        self.pk = kwargs.get("pk")
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")
        self.salt = kwargs.get("salt")
        self.fname = kwargs.get("fname")
        self.lname = kwargs.get("lname")
        self.email = kwargs.get("email")

    @classmethod
    def no_repeat_username(cls, username): #make sure people don't have duplicate usernames
        with sqlite3.connect(cls.dbpath) as conn:
            cur = conn.cursor()

            sql = f"""SELECT * FROM {cls.tablename} WHERE username = {username}"""
            cur.execute(sql)
            current_user = cur.fetchone()
            print(current_user)
            if current_user:
                return True
            return False
    
    @classmethod 
    def no_repeat_email(cls, email):
        with sqlite3.connect(cls.dbpath) as conn:
            cur = conn.cursor()

            sql = f"""SELECT * FROM {cls.tablename} WHERE email = {email}"""
            cur.execute(sql)
            current_email = cur.fetchone()
            if current_email:
                return False
            return True


import sqlite3, os
from random import random
from .ORM import ORM
from ._utils import generate_token
import os

class User(ORM):
    tablename = "user"
    dbpath = ""
    fields = ["pk", "username", "password", "salt", "fname", "lname", "email", "token"]

    def __init__(self, **kwargs):
        self.pk = kwargs.get("pk")
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")
        self.salt = kwargs.get("salt")
        self.fname = kwargs.get("fname")
        self.lname = kwargs.get("lname")
        self.email = kwargs.get("email")
        self.token = kwargs.get("token")

    @classmethod
    def no_repeat_username(cls, username): #make sure people don't have duplicate usernames
        with sqlite3.connect(cls.dbpath) as conn:
            cur = conn.cursor()
            # try:
            #     sql = f"""SELECT pk FROM {cls.tablename} WHERE username == ?"""
            #     cur.execute(sql, (username,))
            #     repeat = cur.fetchone()
            #     return True
            # except sqlite3.OperationalError:
            #     return False
            sql = f"""SELECT pk FROM {cls.tablename} WHERE username == ?"""
            cur.execute(sql, (username,))
            repeat = cur.fetchone()
            if repeat is None:
                return False
            return True
    
    @classmethod 
    def no_repeat_email(cls, email):
        with sqlite3.connect(cls.dbpath) as conn:
            cur = conn.cursor()
            # try:
            #     sql = f"""SELECT pk FROM {cls.tablename} WHERE email == ?"""
            #     cur.execute(sql, (email,))
            #     return True
            # except sqlite3.OperationalError:
            #     return False
            sql = f"""SELECT pk FROM {cls.tablename} WHERE email == ?"""
            cur.execute(sql, (email,))
            repeat = cur.fetchone()
            if repeat is None:
                return False
            return True
    
    def create_token(self):
        repeat = True
        self.token = generate_token()

        with sqlite3.connect(self.dbpath) as conn:
            cur = conn.cursor()

            # Make sure token is unique
            while repeat is True:
                sql = f"""SELECT pk FROM {self.tablename} WHERE token == ?"""
                cur.execute(sql, (self.token,))
                instance = cur.fetchone()

                if instance is None:
                    repeat = False
                else:
                    self.token = generate_token()
            
            # Assign token to user
            sql = f"""UPDATE {self.tablename} SET token = "{self.token}"
                WHERE pk = {self.pk}"""
            cur.execute(sql)
    
    def del_token(self):
        with sqlite3.connect(self.dbpath) as conn:
            cur = conn.cursor()
            sql = f"""UPDATE {self.tablename} SET token="" 
                WHERE pk={self.pk}"""
            cur.execute(sql)

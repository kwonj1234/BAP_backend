import sqlite3
import os

DIR = os.path.dirname(__file__)
DBPATH = os.path.join(DIR, 'recipes.db')

def schema(dbpath = DBPATH):
    with sqlite3.connect(dbpath) as connection:
        c = connection.cursor()

        dropsql = """DROP TABLE IF EXISTS ?;"""
        for table in ["user", "saved_recipes", "recipe", "recipe_ingredients", "recipe_directions", "ingredient", "prep_time"]:
            c.execute(dropsql, (table))

        # create users table
        sql = """CREATE TABLE user (
            pk INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR,
            password VARCHAR(256),
            salt VARCHAR,
            fname VARCHAR,
            lname VARCHAR,
            email VARCHAR);"""
        c.execute(sql)

        # create a saved recipes table for every user
        sql = """CREATE TABLE saved_recipes (
            pk INTEGER PRIMARY KEY AUTOINCREMET,
            user_pk INTEGER,
            recipe_pk INTEGER,
            FOREIGN KEY (recipe_pk) REFERENCES recipe.pk,
            FOREIGN KEY (user_pk) REFERENCES user.pk);"""
        c.execute(sql)

        # create recipe book table
        # total_time in seconds
        sql = """CREATE TABLE recipe (
            pk INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR,
            url VARCHAR,
            culture VARCHAR,
            img_path VARCHAR,
            serving_size INTEGER
            total_time INTEGER);"""
        c.execute(sql)

        # create table for ingredients for a recipe
        sql = """CREATE TABLE recipe_ingredients (
            pk INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR,
            amount FLOAT,
            unit VARCHAR(12),
            recipe_pk INTEGER,
            FOREIGN KEY (recipe_pk) REFERENCES recipe.pk);"""
        c.execute(sql)

        # create table for recipe directions
        sql = """CREATE TABLE recipe_directions (
            pk INTEGER PRIMARY KEY AUTOINCREMENT,
            direction TEXT,
            duration INTEGER,
            recipe_pk INTEGER,
            FOREIGN KEY (recipe_id) REFERENCES recipe.pk);"""
        c.execute(sql)

        # create ingredients table
        sql = """CREATE TABLE ingredient (
            pk INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR,
            flavor VARCHAR);"""
        c.execute(sql)
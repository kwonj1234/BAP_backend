import sqlite3
import os

DIR = os.path.dirname(__file__)
DBPATH = os.path.join(DIR, 'recipes.db')

def schema(dbpath = DBPATH):
    with sqlite3.connect(dbpath) as connection:
        c = connection.cursor()

        dropsql = """DROP TABLE IF EXISTS ?;"""
        for table in ["recipe", "recipe_ingredients", "recipe_directions", "ingredient", "prep_time"]:
            c.execute(dropsql, (table))

        #create recipe book table
        sql = """CREATE TABLE recipe (
            pk INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR,
            culture VARCHAR,
            img_path VARCHAR,
            serving_size INTEGER);"""
        c.execute(sql)

        #create table for ingredients for a recipe
        sql = """CREATE TABLE recipe_ingredients (
            pk INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR,
            amount FLOAT,
            unit VARCHAR(12),
            recipe_pk INTEGER,
            FOREIGN KEY (recipe_pk) REFERENCES recipe.pk;"""
        c.execute(sql)

        #create table for recipe directions
        sql = """CREATE TABLE recipe_directions (
            pk INTEGER PRIMARY KEY AUTOINCREMENT,
            step INTEGER,
            direction TEXT,
            seconds_since_start INTEGER,
            recipe_pk INTEGER,
            FOREIGN KEY (recipe_id) REFERENCES recipe.pk);"""
        c.execute(sql)

        #create ingredients table
        sql = """CREATE TABLE ingredient (
            pk INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR,
            flavor VARCHAR);"""
        c.execute(sql)
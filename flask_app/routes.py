from models import scrape_me, hash_password, User, Saved_Recipes, Recipe, Recipe_Directions, Recipe_Ingredients
from flask import Flask, request, jsonify
import os
from flask_cors import CORS



# import sys
# sys.path.append('../recipe-scrapers')
# from recipe_scrapers import scrape_me

app = Flask(__name__)
CORS(app)

@app.route("/get_url", methods = ["POST"])
def get_recipe_from_url():
    data = request.get_json()
    recipe = scrape_me(f'{data["recipe_url"]}')

    # Get rid of blank spaces
    recipe_instructions = [
        instruction for instruction in recipe.instructions().split('\n')
        if len(instruction) > 0
    ]
    
    return jsonify({
        "recipeTitle"       : recipe.title(),
        "recipeTime"        : recipe.total_time(),
        "recipeYields"      : recipe.yields(),
        "recipeIngredients" : recipe.ingredients(),
        "recipeInstructions": recipe_instructions,
        "recipeImage"       : recipe.image()
    })

@app.route("/create_user", methods = ["POST"])
def create_user():
    data = request.get_json()

    # Make sure another user does not have the username
    if User.no_repeat_username(data["username"]):
        return jsonify({
            "response" : "Username already in use"
        })
    
    # Make sure another user does not have the email
    if User.no_repeat_email(data["email"]):
        return jsonify({
            "response" : "E-mail already in use"
        })
    
    # Salt and hash the password
    salt_pw = os.urandom(64)
    hashed_pw = hash_password(data["password"], salt_pw)

    user = User(
        pk = None,
        username = data["username"], 
        password = hashed_pw, 
        salt = salt_pw, 
        fname = data["fname"],
        lname = data["lname"],
        email = data["email"]
    )
    user.save()
    return jsonify({
        "response" : "Account successfully created"
    })

@app.route("/login", methods = ["POST"])
def authenticate():
    data = request.get_json()

    user = User.select_one(f"""WHERE username = ?""", (data["username"],))
    input_password = hash_password(data["password"], user.salt)

    if input_password == user.password:
        return jsonify({
            "pk"       : user.pk,
            "username" : user.username,
            "password" : data["password"],
            "fname"    : user.fname,
            "lname"    : user.lname,
            "email"    : user.email
        })
    else: 
        return jsonify({
            "response" : "Username or Password is incorrect"
        })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
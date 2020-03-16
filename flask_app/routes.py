from models import scrape_me, hash_password, generate_token, time_step, User, Saved_Recipes, Recipe, Recipe_Instructions
from flask import Flask, request, jsonify
import os
from flask_cors import CORS

# import sys
# sys.path.append('../recipe-scrapers')
# from recipe_scrapers import scrape_me

app = Flask(__name__)
CORS(app)

@app.route("/create_user", methods = ["POST"])
def create_user():
    data = request.get_json()

    # Make sure another user does not have the username
    if User.no_repeat_username(data["username"]):
        return jsonify({
            "response" : "Username already in use"
        })

    # Make sure password and confirmPassword matches since user cannot 
    # see passwords
    if data["password1"] != data["password2"]:
        return jsonify({
            "response" : "Passwords do not match"
        })
    # Make sure another user does not have the email
    if User.no_repeat_email(data["email"]):
        return jsonify({
            "response" : "E-mail already in use"
        })
    
    # Salt and hash the password
    salt_pw = os.urandom(64)
    hashed_pw = hash_password(data["password1"], salt_pw)
    # Create a unique token for this user, to be used in session storage

    user = User(
        pk = None,
        username = data["username"], 
        password = hashed_pw, 
        salt = salt_pw, 
        fname = data["fname"],
        lname = data["lname"],
        email = data["email"],
        token = ""
    )
    user.save()

    return jsonify({
        "response" : "Account successfully created"
    })

@app.route("/login", methods = ["POST"])
def authenticate():
    data = request.get_json()

    user = User.select_one(f"""WHERE username = ?""", (data["username"],))
    # Error handling in case username does not exist
    if user is False:
        return jsonify({
            "response" : "Username or Password is incorrect"
        })
    # Salt and hash input password and compare it to saved password
    input_password = hash_password(data["password"], user.salt)
    if input_password == user.password:
        user.create_token()
        return jsonify({
            "token" : user.token
        })
    else: 
        return jsonify({
            "response": "Username or Password is incorrect",
            "token"   : ""
        })

@app.route("/token/<token>", methods = ["GET"])
def token_auth(token):
    # Get user data
    user = User.select_one(f"""WHERE token = ?""", (token,))
    user_data = {
        "pk"       : user.pk,
        "username" : user.username,
        "fname"    : user.fname,
        "lname"    : user.lname,
        "token"    : user.token
    }

    # Get user saved recipes    
    user_recipes = {}

    saved_recipes = Saved_Recipes.select_all(
        """WHERE user_pk = ?""",
        (user.pk,)
    )
    
    for saved_recipe in saved_recipes:
        recipe = Recipe.select_one("""WHERE pk = ?""", (saved_recipe.recipe_pk))
        # make ingredients text into a list of lists
        recipe_ingredients = [
            ingredient for ingredient in recipe.recipe_ingredients.split("\n")
        ]
        user_recipes[recipe.name] = {
            "name"        : recipe.name,
            "time"        : recipe.total_time,
            "yields"      : recipe.serving_size,
            "ingredients" : recipe_ingredients,
            "instructions": [],
            "image"       : recipe.img_path,
            "url"         : recipe.source
        }
        
        instructions = Recipe_Instructions.select_all(
            """WHERE recipe_pk = ? ORDER BY pk ASC""", (recipe.pk,)
        )
        for each_step in instructions:
            step = [each_step.duration, each_step.instruction]
            user_recipes[recipe.name]["instructions"].append(step)
    
    return jsonify({
        "userData"   : user_data,
        "userRecipes": user_recipes
    })

@app.route("/logout", methods = ["POST"])
def logout():
    data = request.get_json()

    user = User.select_one(f"""WHERE pk = ?""", (data["pk"],))
    user.del_token()
    return jsonify({
        "response" : "Successfully Logged Out"
    })

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
        "name"       : recipe.title(),
        "time"        : recipe.total_time(),
        "yields"      : recipe.yields(),
        "ingredients" : recipe.ingredients(),
        "instructions": recipe_instructions,
        "image"       : recipe.image(),
        "url"         : data["recipe_url"]
    })

@app.route("/save_recipe_to_user", methods = ["POST"])
def save_recipe_to_user():
    data = request.get_json()

    # Check if recipe is already in database
    if Recipe.no_repeat_recipe(data["recipe"]["url"]):
        recipe = Recipe.select_one(
            """WHERE source = ?""", 
            (data["recipe"]["url"],)
        )
    else:
        recipe_ingredients_text = "\n".join(
            data["recipe"]["ingredients"]
        )

        recipe = Recipe(
            pk = None, 
            name = data["recipe"]["name"], 
            source = data["recipe"]["url"], 
            culture = "",
            img_path = data["recipe"]["image"],
            serving_size = data["recipe"]["yields"],
            total_time = data["recipe"]["time"],
            recipe_ingredients = recipe_ingredients_text
        )
        recipe.save()

        recipe = Recipe.select_one(
            """WHERE source = ?""", 
            (data["recipe"]["url"],)
        )

        for instruction in data["recipe"]["instructions"]:
            recipe_instruction = Recipe_Instructions(
                pk = None,
                instruction = instruction,
                duration = time_step(instruction),
                recipe_pk = recipe.pk
            )
            recipe_instruction.save()

    save_recipe_to_user = Saved_Recipes(
        pk = None, 
        user_pk = data["userPk"],
        recipe_pk = recipe.pk
    )
    save_recipe_to_user.save()

    return jsonify({
        "response" : "Recipe saved"
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
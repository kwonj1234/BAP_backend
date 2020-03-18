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
    # Initalize list. This list will be a list of dictionaries
    user_recipes = []
    saved_recipes = Saved_Recipes.select_all(
        """WHERE user_pk = ?""",
        (user.pk,)
    )
    for saved_recipe in saved_recipes:
        # Get recipe from database used recipe_pk in saved_recipe table
        recipe = Recipe.select_one("""WHERE pk = ?""", (saved_recipe[2],))

        # Initalize a list for the recipe instructions
        recipe_instructions = []
        # Get all instructions for this recipe
        instructions = Recipe_Instructions.select_all(
            """WHERE recipe_pk = ? ORDER BY pk ASC""", (recipe.pk,)
        )
        # For every step in the instructions, organize it to send 
        # to frontend and append to instructions
        total_time = 0
        for each_step in instructions:
            # each_step[0] - pk
            # each_step[1] - instruction
            # each_step[2] - duration
            # each_step[3] - recipe_pk
            step = [each_step[2], each_step[1]]
            recipe_instructions.append(step)
            total_time += each_step[2]
        
        # make ingredients text into a list of lists
        # REMEMBER ingredients are separated by newline characters
        recipe_ingredients = [
            ingredient for ingredient in recipe.ingredients.split("\n")
        ]
        # If the scraped website does not provide an estimation on time it
        # takes to finish the recipe, use the estimated time for each step
        # and sum it to create an estimation
        if recipe.total_time == 0:
            recipe.total_time = total_time
        # Append dictionary of recipe data to list of recipes, 
        # initalize list for instructions
        user_recipes.append({
            "name"        : recipe.name,
            "time"        : recipe.total_time,
            "yields"      : recipe.serving_size,
            "ingredients" : recipe_ingredients,
            "instructions": recipe_instructions,
            "image"       : recipe.img_path,
            "url"         : recipe.source
        })
    
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
        [time_step(instruction), instruction] 
        for instruction in recipe.instructions().split('\n')
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
        # Turn list of ingredients into single block of text separated
        # by new line characters so that it can be easily saved into 
        # the database
        recipe_ingredients_text = "\n".join(
            data["recipe"]["ingredients"]
        )
        # Create recipe class then save it
        recipe = Recipe(
            pk = None, 
            name = data["recipe"]["name"], 
            source = data["recipe"]["url"], 
            culture = "",
            img_path = data["recipe"]["image"],
            serving_size = data["recipe"]["yields"],
            total_time = data["recipe"]["time"],
            ingredients = recipe_ingredients_text
        )
        recipe.save()
        # Reach into database and pull the same recipe that you just saved
        # so that this one has the pk
        recipe = Recipe.select_one(
            """WHERE source = ?""", 
            (data["recipe"]["url"],)
        )
        # Use the recipe pk to save the recipe's instructions into the 
        # instructions table
        for instruction in data["recipe"]["instructions"]:
            recipe_instruction = Recipe_Instructions(
                pk = None,
                instruction = instruction[1],
                duration = instruction[0],
                recipe_pk = recipe.pk
            )
            recipe_instruction.save()
    # If recipe is already saved to this user send this response
    if Saved_Recipes.no_repeat_saves(data["userPk"], recipe.pk):
        return jsonify({
            "response" : "Recipe is already in your RecipeBox"
        })
    # If recipe is not saved to the user, create an entry in
    # saved_recipes table
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
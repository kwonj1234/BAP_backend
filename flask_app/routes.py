from models import scrape_me, hash_password, generate_token, time_step, User, Saved_Recipes, Recipe, Recipe_Instructions
from flask import Flask, request, jsonify
import math
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
            "pk"          : recipe.pk,
            "name"        : recipe.name,
            "time"        : recipe.total_time//60,
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
    
    if recipe.total_time() == 0:
        total_time = sum(
            # Divide by 60 because time is in seconds but the frontend will
            # display time in hours and minutes
            [instruction[0] for instruction in recipe_instructions]
        )//60
    else:
        total_time = recipe.total_time()

    return jsonify({
        "name"        : recipe.title(),
        "time"        : total_time,
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
    # If the recipe is not in the database, save it to database
    else:
        # Turn list of ingredients into single block of text separated
        # by new line characters so that it can be easily saved into 
        # the database
        recipe_ingredients_text = "\n".join(
            data["recipe"]["ingredients"]
        )
        # Create recipe class then save it
        # Remember in the database, time is in seconds
        recipe = Recipe(
            pk = None, 
            name = data["recipe"]["name"], 
            source = data["recipe"]["url"], 
            culture = "",
            img_path = data["recipe"]["image"],
            serving_size = data["recipe"]["yields"],
            total_time = data["recipe"]["time"]*60, 
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

@app.route("/delete_recipe_from_user", methods = ["POST"])
def delete_recipe_from_user():
    data = request.get_json()
    saved_recipe = Saved_Recipes.select_one(
        """WHERE user_pk = ? and recipe_pk = ?""",
        (data["user_pk"], data["recipe_pk"])
    )
    saved_recipe.delete()
    return jsonify({
        "response" : ""
    })

@app.route("/plan_meal", methods = ["POST"])
def plan_meal():
    data = request.get_json()
    # Sort recipes by their total time to finish
    data["planMeal"].sort(key=lambda recipe: recipe["time"], reverse=True)
    # Initialize a list to insert instructions into and recipes
    instructions = []
    recipes = []
    # Total time for recipe will be recipe that takes longest. In the sorted
    # list, it will be the first recipe
    time = data["planMeal"][0]["time"]*60
    # For each instruction in each recipe add the time step where the 
    # instruction is done and add it to the list of instructions then
    # sort the list of instruction by the time step
    for i in range(len(data["planMeal"])):
        recipe = {}
        recipe["index"] = i
        recipe["name"] = data["planMeal"][i]["name"]
        recipes.append(recipe)
        time_difference = 0
        recipe = data["planMeal"][i]
        for j in range(len(recipe["instructions"])-1, -1, -1):
            instruction = {}
            time_difference += recipe["instructions"][j][0]
            instruction["timeStep"] = math.ceil((time - time_difference)/60)
            instruction["duration"] = recipe["instructions"][j][0]
            instruction["instruction"] = recipe["instructions"][j][1]
            instruction["recipe_index"] = i
            instructions.append(instruction)
    instructions.sort(key=lambda instruction: instruction["timeStep"])
    # # Reference recipe instructions that all other recipes instructions 
    # # will be sorted into
    # reference = data["planMeal"][0]["instructions"]
    # # Instructions for the all other recipes
    # others = [recipe["instructions"] 
    #     for recipe in data["planMeal"] 
    #     if recipe != data["planMeal"][0]
    # ]
    # # a list of indexes for every recipe in that was sent over except for
    # # reference recipe
    # indexes = [len(instructions)-1 for instructions in others]

    # # Start sorting from the last step 
    # for i in range(len(reference) - 1, -1, -1):
    #     # Set how long this step takes
    #     duration_step = reference[i][0]
    #     for j in range(len(others)):
    #         # If for that recipe you've gone through the entire list of 
    #         # instructions just pass
    #         if indexes[j] == -1:
    #             pass
    #         else:
    #             # Translation
    #             # While the duration for the step in the reference recipe is
    #             # greater than the duration in the target recipe append the 
    #             # instruction from the target recipe
    #             while (duration_step > others[j][indexes[j]][0]) and (indexes[j] > -1):
    #                 instructions.insert(0, others[j][indexes[j]])
    #                 # Subtract time taken for total time for moving on to next 
    #                 # step
    #                 duration_step -= others[j][indexes[j]][0]
    #                 # Move on to the next step in target recipe
    #                 indexes[j] -= 1
    #     # Add the instructions from the reference recipe
    #     instructions.insert(0, reference[i])
    #     # If the reference recipe is completed add the recipe of the instructions
    #     if i == 0:
    #         for j in range(len(others)):
    #             while indexes[j] > -1:
    #                 instructions.insert(0, others[j][indexes[j]])
    #                 indexes[j] -= 1

    return jsonify({
        "recipes"      : recipes,
        "instructions" : instructions
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
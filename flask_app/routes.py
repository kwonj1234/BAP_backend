from flask import Flask, request, jsonify
from flask_cors import CORS
from models import scrape_me


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

if __name__ == "__main__":
    app.run(debug=True, port=5000)
from flask import Flask, request, jsonify
from flask_cors import CORS

# import sys
# sys.path.append('../recipe-scrapers')
# from recipe_scrapers import scrape_me

app = Flask(__name__)
CORS(app)


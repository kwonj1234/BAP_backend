This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app). <br/>
This project uses [Flask](https://flask.palletsprojects.com/en/1.1.x/installation/#installation) and Python3 on the backend. <br/>
This project uses the [recipe-scrapers tool](https://github.com/hhursev/recipe-scrapers).

## RecipeDex
A simple web scraping application that allows users to create an account, scrape recipes from 56 different websites and save those recipes to their account so that they can view it in the future. RecipeDex also provides a "Plan a Meal" function that allows users to create a list of recipes they would like to cook and create an aggregated list of instructions such that the recipes will finish at the same time.

## Set Up RecipeDex
You can try out RecipeDex at recipedex.net from 10am - 6pm while servers are running.

OR 

You can find the backend code for RecipeDex [here](https://github.com/kwonj1234/recipedex_backend). Run the following lines of code to start up a Flask server locally and use recipedex.net that way.

    git clone https://github.com/kwonj1234/recipedex_backend.git &&
    cd recipedex_backend &&
    python3 run.py

OR

If you want to run everything locally.

Install RecipeDex using

    git clone https://github.com/kwonj1234/recipedex_backend.git &&   
    git clone https://github.com/kwonj1234/recipedex_frontend.git &&   
    cd recipedex_frontend && npm install

## Running locally
From the directory you cloned the two repositories, start the Flask server.

    cd recipedex_backend &&   
    python3 run.py

In a separate terminal, return to the directory you cloned the two repositories and start up the application in development mode.
 
    npm start
This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).
This project uses [Flask](https://flask.palletsprojects.com/en/1.1.x/installation/#installation) and Python3 on the backend.

This project uses the [recipe-scrapers tool](https://github.com/hhursev/recipe-scrapers).

You can view a demo of BAP [here](https://www.youtube.com/watch?v=R9Tdp4Y7H8A&feature=youtu.be).

## Set Up BAP
You can find the backend code for BAP [here](https://github.com/kwonj1234/recipebox_backend).

Assuming you have both [Node.js](https://nodejs.org/en/) and [Flask](https://flask.palletsprojects.com/en/1.1.x/installation/#installation) installed.

Install BAP using

    git clone https://github.com/kwonj1234/BAP_backend.git &&   
    git clone https://github.com/kwonj1234/BAP_frontend.git &&   
    cd recipebox_frontend && npm install

## Running locally
From the directory you cloned the two repositories, start the Flask server.

    cd BAP_backend &&   
    python3 run.py

In a separate terminal start up the application in development mode.

    cd ../BAP_frontend &&   
    npm start
# Louie

Prototype for a chat bot designed for smart cities
- This is created using WIT, Facebook, and Heroku


The bin folder is used to host the SERVER which runs on heroku.
- The server.py handles all of Facebook's messaging functions

The louie folder hosts all of the API calls and the functionality of the chatbot.
- Search.py houses the Pipeline that converges confidences, API calls, and different WIT bots to generate the best answer

The tests folder houses the tests for the chatbot and will let you know if you failed or not using codecov and a TravisCI
- Basic tests have been setup, more are needed to be added (must adhere to the format currently inplace i.e. test_XXX.py)
- Travis built with .travis.yml
- Codecov generated with codecov.yml

Procfile, runtime.txt are used to set up the heroku Server
- Procfile tells heroku what to run for a Server
- runtime.txt tells heroku which version of python to run

Run setup.py first to install the package 'louie' to be able to run this chatbot locally
- requirements.txt are what are needed to run this chatbot fully

TO TEST LOCALLY:
- Navigate to louie/louie
- Look in old_search.py
- Grab the interactive() function
- Run that to test locally aganist WIT


[![codecov](https://codecov.io/gh/tthatcher95/louie/branch/master/graph/badge.svg)](https://codecov.io/gh/tthatcher95/louie)

[![Build Status](https://travis-ci.org/tthatcher95/louie.svg?branch=master)](https://travis-ci.org/tthatcher95/louie)

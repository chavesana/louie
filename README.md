[![Build Status](https://travis-ci.org/tthatcher95/louie.svg?branch=master)](https://travis-ci.org/tthatcher95/louie)  [![codecov](https://codecov.io/gh/tthatcher95/louie/branch/master/graph/badge.svg)](https://codecov.io/gh/tthatcher95/louie)

# Louie

![](https://lh3.googleusercontent.com/gunPW3sIq6TV4MqRTxuFkqWblF0l2Xt3zVEkGmnnyV1OqZZm3wwB1xNKGtbGOsSZXmFWPdqEBpkqAJkI9USN-i0RHK7Q4rKyvuaA4LxtmTjDlNnoLE3wtGI0d7MDzZn6vsbBgZ7ZMj6VpFP3T89HzM6lu-xAR9D_JEyvs6uiwbqABweb3orHqAe8XDWI8HzTVnUeqZuhzqqF6ArkwXb4XLZ88q_ZNUcg-OId_sNxwtfgRe3vRrLucY-ScjZOadA1ZGxXOZFPuWLrmUttxsYPNbrHhScATaQ-wT45qf9tLNjU7xF2hLMOjfIAM_zE4Xh6eOPknseSRCdEPGjd3Ezq6Chz1EtUUO-Nzu-psNNPdyRBh7NvzfoK7L7VJgWomTJnLx1KUBwvQCiCqXVLqgBihWT4DVjZhjTAYbgJr9Qe-MnzqpS2cPp9mq8m5LSM8Vjn9WEEIDJJ7oUBgV52deG1DD_n2gC-YDj4HAH5HiYD7VJOEZQrofjpzamN3rjs1EvoghGz_cCL6czi8EvsdeFCygVzW7izF6i8Le6Qu7tidFDBksNpZiF4KmngKZ67evCUBGnHxwqnvD0G6tssTLizF52fXTiK6o4T6wX_jE641A=w886-h578-no)

Chatbot designed to be used in smart cities. A text string is run through a pipeline of functions to derive an answer to simple queries.

The bin folder is used to host the SERVER which runs on heroku. The server.py handles all of Facebook's messaging functions

The louie folder hosts all of the API calls and the functionality of the chatbot.
- Search.py houses the Pipeline that converges confidences, API calls, and different WIT bots to generate the best answer

The tests folder houses the tests for the chatbot and will let you know if you failed or not using codecov and a TravisCI
- Basic tests have been setup, more are needed to be added (must adhere to the format currently inplace i.e. test_XXX.py)
- Travis built with .travis.yml
- Codecov generated with codecov.yml

Procfile, runtime.txt are used to set up the heroku Server˝
- Procfile tells heroku what to run for a Server
- runtime.txt tells heroku which version of python to run

Run setup.py first to install the package 'louie' to be able to run this chatbot locally
- requirements.txt are what are needed to run this chatbot fully

TO TEST LOCALLY:
- Navigate to louie/louie
- Look in old_search.py
- Grab the interactive() function
- Run that to test locally aganist WIT

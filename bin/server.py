#!/usr/bin/env python
import os
import sys
import requests
from sys import argv
from bottle import Bottle, request, debug
import wolframalpha as wolf
import louie as lou
from louie import *

# Setup Bottle Server
debug(True)
app = Bottle()


# Facebook Messenger GET Webhook
@app.get('/webhook')
def messenger_webhook():
    """
    A webhook to return a challenge
    """
    verify_token = request.query.get('hub.verify_token')
    # check whether the verify tokens match
    if verify_token == FB_VERIFY_TOKEN:
        # respond with the challenge to confirm
        challenge = request.query.get('hub.challenge')
        return challenge
    else:
        return 'Invalid Request or Verification Token'


# Facebook Messenger POST Webhook
@app.post('/webhook')
def messenger_post():
    """
    Handler for webhook (currently for postback and messages)
    """
    print("messenger post func called")
    data = request.json
    print("data------\n",data)
    if data['object'] == 'page':
        for entry in data['entry']:
            # get all the messages
            messages = entry['messaging']
            try:
                if messages[0]:
                    # Get the first message
                    message = messages[0]
                    print(message)
                    # Yay! We got a new message!
                    # We retrieve the Facebook user ID of the sender
                    sender = message['sender']
                    fb_id = message['sender']['id']



                    # We retrieve the message content
                    text = message['message']['text']

                    message = {
                        'sender' : {'Someone' : fb_id},
                        'text' : text
                    }

                    results = lou.build_pipeline(message)
                    # Let's forward the message to the Wit.ai Bot Engine
                    # We handle the response in the function send()
                    print('MESSAGE RESPONSE = ', str(results))

                    fb_message(fb_id, str(results))

            except Exception as e:
                print('ERROR ==================================')
                print(e)
    else:
        # Returned another event
        return 'Received Different Event'
    return None


def fb_message(sender_id, text):
    """
    Function for returning response to messenger
    """
    data = {
        'recipient': {'id': sender_id },
        'message': {'text': text}
    }
    # Setup the query string with your PAGE TOKEN
    qs = 'access_token=' + FB_PAGE_TOKEN
    # Send POST request to messenger
    resp = requests.post('https://graph.facebook.com/me/messages?' + qs, json=data)
    print("content type:", type(resp.content))
    return resp.content.decode("utf-8")


def send(request, response):
    """
    Sender function
    """
    print('in send ==============================')
    # We use the fb_id as equal to session_id
    fb_id = request['session_id']
    text = response['text']

    print("text ===== ", text)

    print("Entire payload =======", response)
    # send message
    fb_message(fb_id, text.decode("utf-8"))


if __name__ == '__main__':
    # Run Server
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

#!/usr/bin/env python
import os
import sys
import requests
from sys import argv
from bottle import Bottle, request, debug
import wolframalpha as wolf

sys.path.append(os.path.abspath('..'))

import louie as lou


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
                    fb_id = message['sender']['id']
                    # We retrieve the message content
                    text = message['message']['text']
                    # Let's forward the message to the Wit.ai Bot Engine
                    # We handle the response in the function send()
                    res = lou.witclient.message(text)
                    print('MESSAGE RESPONSE = ', res)

                    if 'wikipedia_search_query' in res['entities'].keys():
                        print('[PERFORMING WOLFRAM QUERY]')
                        message_string = res['entities']['wikipedia_search_query'][0]['value']
                        lou.wolfram_query(message_string)

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


def first_entity_value(entities, entity):
    """
    Returns first entity value
    """
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val


def send(request, response):
    """
    Sender function
    """
    print('in send ==============================')
    # We use the fb_id as equal to session_id
    fb_id = request['session_id']
    text = response['text']

    print("text ===== ", text)
    # send message
    fb_message(fb_id, text.decode("utf-8"))


def get_forecast(request):
    context = request['context']
    entities = request['entities']
    loc = first_entity_value(entities, 'location')
    if loc:
        # This is where we could use a weather service api to get the weather.
        context['forecast'] = 'sunny'
        if context.get('missingLocation') is not None:
            del context['missingLocation']
    else:
        context['missingLocation'] = True
        if context.get('forecast') is not None:
            del context['forecast']
    return context

if __name__ == '__main__':
    # Run Server
    # print(os.environ['PORT'])
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

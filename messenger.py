#!/usr/bin/env python
# coding:utf-8

# Messenger API integration example
# We assume you have:
# * a Wit.ai bot setup (https://wit.ai/docs/quickstart)
# * a Messenger Platform setup (https://developers.facebook.com/docs/messenger-platform/quickstart)
# You need to `pip install the following dependencies: requests, bottle.
#
# 1. pip install requests bottle
# 2. You can run this example on a cloud service provider like Heroku, Google Cloud Platform or AWS.
#    Note that webhooks must have a valid SSL certificate, signed by a certificate authority and won't work on your localhost.
# 3. Set your environment variables e.g. WIT_TOKEN=your_wit_token
#                                        FB_PAGE_TOKEN=your_page_token
#                                        FB_VERIFY_TOKEN=your_verify_token
# 4. Run your server e.g. python examples/messenger.py {PORT}
# 5. Subscribe your page to the Webhooks using verify_token and `https://<your_host>/webhook` as callback URL.
# 6. Talk to your bot on Messenger!

import os
import requests
from sys import argv
from wit import Wit
from bottle import Bottle, request, debug
import wolframalpha as wolf

# Wit.ai parameters
WIT_TOKEN = 'FCLEILUP6T2PTIH6TSWWJYFJYKG3KL2L'
# Messenger API parameters
FB_PAGE_TOKEN = 'EAAEvbHrTo9IBAJigS9lKANutM4V3qOzcnzi86PbWufrN5NJaB1c8ZBOn1DEof3lrTPX9w3qZCpWn93G9yRLw5UrtzS4dP6HLmuAenhAjKJUXDMVP67Iq2FHr2Fc3yCyZBgF87ZAj0y1PPshW0elBivNr0vXw6UPxY5BsyZA1u3gZDZD'
# A user secret to verify webhook get request.
FB_VERIFY_TOKEN = 'hello'

# Wolfram
WOLFRAM_TOKEN = '64J9LH-5Q8357GKRK'

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
                    res = client.message(text)
                    print('MESSAGE RESPONSE = ', res)

                    if 'wikipedia_search_query' in res['entries']:
                        print('performing wolfram search-------------')
                        query_result = wolfclient.query(res['entries']['wikipedia_search_query']['value'])
                        print(query_result)
                        fb_message(fb_id, str(query_result))
                    else:
                        fb_message(fb_id, str(res['entities']))

            except Exception as e:
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



# Setup Wit Client
client = Wit(access_token=WIT_TOKEN)
wolfclient = wolf.Client(WOLFRAM_TOKEN)

if __name__ == '__main__':
    # Run Server
    # print(os.environ['PORT'])
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

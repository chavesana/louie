import unittest
import json
import ast

from wit import Wit
from louie.search import *

client = Wit(access_token = 'FCLEILUP6T2PTIH6TSWWJYFJYKG3KL2L')

def test_one():
    json_obj = client.message('When was NAU founded?')
    intents = json_obj['entities']

    if('wikipedia_search_query' in intents):
        assert True

    else:
        print('Oh no, got response: ', json_obj['entities'])
        assert False

def test_two():
    json_obj = client.message('What day is christmas?')
    intents = json_obj['entities']

    if('wikipedia_search_query' in intents):
        assert True

    else:
        print('Oh no, got response: ', json_obj['entities'])
        assert False


print('TESTS')
print()

test_confidences = [
    {'bot' : 'loc', 'confidence' : .9},
    {'bot' : 'converse', 'confidence' : .8}
]

test_entities0 = {'intent': [{'confidence': 0.55245981772807,
     'value': 'event_search'}],
   'local_search_query': [{'confidence': 0.93791,
     'suggested': True,
     'type': 'value',
     'value': 'tacos'}]}

test_entities1 = {'intent': [{'confidence': 0.99766314336621,
     'value': 'navigation'}],
   'location': [{'confidence': 0.92714,
     'suggested': True,
     'type': 'value',
     'value': 'tacos los altos'}],
   'sentiment': [{'confidence': 0.84524105713291, 'value': 'neutral'}]}

test_entities2 = {'wikipedia_search_query': [{'confidence': 0.93725333333333,
     'suggested': True,
     'type': 'value',
     'value': 'tacos los altos'}]}

context_entities = {
    "local_search_query" : "menudo",
    "location" : "campus",
    "sentiment" : "positive"
}

def test_start():
    print('TEST START')
    data = start(test_message)
    suspected_answer = "{'context': {'location': (35.188, -111.653)},'fb_id': 'user1', 'text': 'Who is JFK', 'entities': {'intent': []}}"
    if(data == suspected_answer):
        assert True

    else:
        assert False

print()

def test_bot_calls():
    print('TESTING BOT CALLS')
    suspected_answers = []
    test_dict = {'text' : 'navigate to tacos los altos'}
    suspected_answers[0] = "('loc', {'local_search_query': [{'suggested': True, 'confidence': 0.93794, 'value': 'JFK', 'type': 'value'}]})"
    suspected_answers[1] = "('event', {'local_search_query': [{'suggested': True, 'confidence': 0.93794, 'value': 'JFK', 'type': 'value'}], 'intent': [{'confidence': 0.51966856225871, 'value': 'event_search'}]})"
    suspected_answers[2] = "('fact', {'wikipedia_search_query': [{'suggested': True, 'confidence': 0.93795, 'value': 'JFK', 'type': 'value'}], 'intent': [{'confidence': 0.71001451473672, 'value': 'personq'}], 'sentiment': [{'confidence': 0.80237627996046, 'value': 'neutral'}]})"
    suspected_answers[3] = "('converse', {'wikipedia_search_query': [{'suggested': True, 'confidence': 0.93795, 'value': 'JFK', 'type': 'value'}], 'intent': [{'confidence': 0.76702998295681, 'value': 'followup'}]})"

    loc = run_loc(test_dict)
    event = run_event(test_dict)
    fact = run_fact(test_dict)
    converse = run_converse(test_dict)

    if(loc == suspected_answers[0] and event == suspected_answers[1] and fact == suspected_answers[2] and converse == suspected_answers[3]):
        assert True

    else:
        print(event)
        print(loc)
        print(fact)
        print(converse)
        assert False


print()

def test_confidences():
print('TESTING CONFIDENCE CONVERGENCE')
    locconf = get_confidences_from_entities("event", loc[1])
    convconf = get_confidences_from_entities("loc", converse[1])
    eventconf = get_confidences_from_entities("converse", event[1])
    factconf = get_confidences_from_entities('fact', fact[1])

    suspected_answers = [{'bot': 'event', 'confidence': 0.8797314436}, {'bot': 'loc', 'confidence': 0.81477845057046483}, {'bot': 'converse', 'confidence': 0.72263869665801228}, {'bot': 'fact', 'confidence': 0.83813290806322371}]

    if(locconf == suspected_answers[0] and convconf == suspected_answers[1] and eventconf == suspected_answers[2] and factconf == suspected_answers[3]):
        asset True

    else:
        print(locconf)
        print(convconf)
        print(eventconf)
        print(factconf)
        assert False

print()
def test_apis():
    print('TESTING API CALLS')
    print(user_data.data)
    loc = local_search(bot_conf_array)
    wolf = wolfram_search(bot_conf_array)

    if(loc == "('Flagstaff Pulliam Airport @ 6200 S Pulliam Dr', 0.81477845057046483)" and wolf == "('US president who held office during the Bay of Pigs Invasion of Cuba, Cuban Missile Crisis, early stages of the Vietnam War, and building of the Berlin Wall', 0.83813290806322371)"):
        assert True
    else:
        print(loc)
        print(wolf)
        assert False

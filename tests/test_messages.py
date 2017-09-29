import unittest
import json
import ast

from wit import Wit

from louie.query import wolfram_query

client = Wit(access_token = 'FCLEILUP6T2PTIH6TSWWJYFJYKG3KL2L')

def test_one():
    json_obj = client.message('When was NAU founded?')
    intents = json_obj['entities']

    if('wikipedia_search_query' in intents):
        assert True

    else:
        print('Oh no, got response: ', json_obj['entities'])
        assert False

    wolfram_query('test')

def test_two():
    json_obj = client.message('What day is christmas?')
    intents = json_obj['entities']

    if('wikipedia_search_query' in intents):
        assert True

    else:
        print('Oh no, got response: ', json_obj['entities'])
        assert False

def test_three():
    json_obj = client.message('Who is Donald Trump?')
    intents = json_obj['entities']

    if('wikipedia_search_query' in intents):
        assert True

    else:
        print('Oh no, got response: ', json_obj['entities'])
        assert False

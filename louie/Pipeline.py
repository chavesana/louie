import os
import sys

import networkx as nx
import numpy as np
import networkx as nx

from scipy.misc import imresize
from collections import defaultdict, MutableMapping, OrderedDict
from copy import deepcopy

from wit import Wit
import wolframalpha as wolf


from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
import facebook
import geocoder
from random import *

from multiprocessing import Process, Queue
import traceback
from copy import deepcopy
import wolframalpha as wolf

import louie
from louie.yelpfusion import YelpFusion

WIT_TOKEN = 'VNKUNTRL2Z4U35HVPDBUZRQAHPVALBMA'
FB_PAGE_TOKEN = 'EAAVWYdbX2BUBAJZBmlbIeZCoocO5CdRHY82VNs8drNbB0yNL5bj63K0ZCQqIqzAbrl0u2ollXrsFIiRMfebWAQmpF1sw2EsThg1TpDulsygqGkQQ7dcHZCZB6W6QGlejXKYEg0ObqZAOTXGqKe9exLf57ZCQW546Kh5W66lEOvaGjX3ffruHXXT'
FB_VERIFY_TOKEN = 'hello'
WOLFRAM_TOKEN = '64J9LH-5Q8357GKRK'
GOOGS_PLACES_TOKEN = 'AIzaSyABRaPH0tzxRT_sVBkkGr5zWkbN3y7jN9Q'
YELP_APP_ID = 'xqTzjWmr8PIUqv9gkQLWBw'
YELP_CLIENT_SECRET = '4YtXv1OVhISGWM4Eb1ji7YJc0igSEAOkvXXyiH3KA0tNKZmGhUoh9M2VAlexfIST'

context_schema = {
    "timezone" : "",
    "loc" : [],
    "keywords" : [],
    "state" : ""
}

fact_node_schema = {
    "fb_id" : "",
    "text" : "",
    "entities" : {}
}

class Pipeline(nx.DiGraph):
    """
    Manages a pipeline of functions. A directed graph where edge direction implies a
    dependencies. The that is, an AB edge implies B depends on A.

    the piline is a callable, so to run it you run  it as any other function

    >>> hello = lambda x : 'Hello {}'.format(x)
    >>> goodbye = lambda x : '{} Goodbye!'.format(x)

    >>> some_pipeline = louie.Pipeline('test')
    >>> some_pipeline.add_node(hello)
    >>> some_pipeline.add_node(goodbye)
    >>> some_pipeline.add_edge('hello', 'goodbye') # func1's reults will be piped into fun2 as input
    >>> some_pipeline('Kelvin')
    'Hello Kelvin! Goodbye!

    Attributes
    ----------
    name : str
           Label for the pipeline

    """
    def __init__(self, *args, name='generic pipline', **kwargs):
        super(Pipeline, self).__init__(*args, **kwargs)
        self.name = name

    def __call__(self, message):
        """
        """
        if not self.nodes():
            raise ValueError('Pipeline {} is an empty network.')

        for s,d,data in self.edges(data=True):
            data['data'] = None

        self.node['start']['input'] = [message]
        num_nodes = len(self.nodes())
        toponodes = list(nx.topological_sort(self))
        for s in toponodes[:-1]:
            print(s)
            node = self.node[s]
            print(node)

            # collect inputs
            if s == 'start':
                inputs = message
            else:
                in_edges = list(self.in_edges(s, data=True))
                if len(in_edges) == 1:
                    inputs = in_edges[0][2]['data']
                else:
                    inputs = [e[2]['data'] for e in in_edges]

            if isinstance(inputs, tuple):
                out = node['func'](*inputs)
            else:


                out = node['func'](inputs)

            out_edges = list(self.out_edges(s, data=True))
            if len(out_edges) == 1:
                out_edges[0][2]['data'] = out
            else:
                for e in out_edges:
                    e[2]['data'] = out

        in_edges = list(self.in_edges(toponodes[-1], data=True))
        if len(in_edges) == 1:
            inputs = in_edges[0][2]['data']
        else:
            inputs = [e[2]['data'] for e in in_edges]
            print(inputs)
        endresult = self.node[toponodes[-1]]['func'](inputs)
        return endresult


    def add_node(self, func, name ="", **kwargs):
        if not name:
            name = func.__name__
        super(Pipeline, self).add_node(name, func=func, **kwargs)

# Ease of access to each bot
bot_indices = {
    'loc' : 0,
    'fact' : 1,
    'event' : 2,
    'converse' : 3
}

numbots = len(bot_indices.keys())

# Hardcoded user_name and location
# Can be extended to any location and
# Any Facebook User
user_context = {
    'user1' : {
        'location' : (35.188,-111.653)
    }
}


def node(func):
    """
    Decorator, any function wrapped with this is allowed to be a node in the pipeline.
    Mostly syntactic sugar for actions that every node must do before and after there function
    is called.

    Parameters
    ----------
    func : The function to wraps

    Returns
    -------
    : the wrapped function
    """
    def wrapper(*args, **kwargs):
        if args and args[0] is None:
            print('NO DATA')
            return None

        try:
            ret = func(*args, **kwargs)
            return ret
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(traceback.print_exc())

    wrapper.__name__ = func.__name__
    return wrapper

@node
def start(messagedata):
    """
    the starter node, every pipeline should start with this node. Extracts all the required information
    from a facebook call containing message data. The data is reduced to a format the pipeline can work with easier. The new
    dictionary is returned and is also stored in a node representing user data.

    Parameters
    ----------
    messagedata : dict
                  dict with the information from the facebook call. Should be unmodified

    Returns
    -------
    : dict
      reformatted facebook which has all the information the pipeline needs to operate.
    """
    data = {}
    fb_id = messagedata['sender']['id']
    context = user_context.get(fb_id)
    data['context'] = context
    data['fb_id'] = fb_id
    data['text'] = messagedata['text']

    data['entities'] = {'intent':[]}
    user_data(data)
    return data

# Grabs the entiries for LOCATION bot
@node
def run_loc(data):
    """
    call the location based wit.ai bot and get the results

    Parameters
    ----------
    data : dict
           modified facebook dictionary

    Returns
    -------
    : tuple
      bot_name and result of the wit.ai call
    """

    text = user_data.data['text']
    wit_response = LOC.message(text)
    return 'loc', wit_response['entities']

# Grabs the entiries for FACT bot
@node
def run_fact(data):
    """
    call the fact based wit.ai bot and get the results

    Parameters
    ----------
    data : dict
           modified facebook dictionary

    Returns
    -------
    : tuple
      bot_name and result of the wit.ai call
    """
    text = user_data.data['text']
    wit_response = FACT.message(text)
    return 'fact', wit_response['entities']

# Grabs the entiries for EVENTS bot
@node
def run_event(data):
    """
    call the event based wit.ai bot and get the results

    Parameters
    ----------
    data : dict
           modified facebook dictionary

    Returns
    -------
    : tuple
      bot_name and result of the wit.ai call
    """
    text = user_data.data['text']
    wit_response = EVENT.message(text)
    return 'event', wit_response['entities']

# Grabs the entities for the CONVERSE bot
@node
def run_converse(data):
    """
    call the conversation based wit.ai bot and get the results

    Parameters
    ----------
    data : dict
           modified facebook dictionary

    Returns
    -------
    : tuple
      bot_name and result of the wit.ai call
    """

    text = user_data.data['text']
    wit_response = CONVERSE.message(text)
    return 'converse', wit_response['entities']

# Returns all of the bots merged together
@node
def union(vals):
    """
    joins multiple values into one homogenous structure

    Parameters
    ----------
    data : iterable
           iterable of structures to join

    Returns
    -------
    : list
      joined data
    """
    if len(edges) == 1:
        return edges['data']

    edge_data = [edge['data'] for edge in edges]
    return edge_data

# Grabs the confidence from each entities
@node
def get_confidences_from_entities(bot, entities):
    """
    extracts confidence values from a wit.ai call and returns a single
    confidence values represeting the correct answer came from this particular bot

    Parameters
    ----------
    bot : string
          name of the bot associated with the entities

    Returns
    -------
    : dict
      bot and confidence is single return value
    """
    confidences = np.array([])
    num_entities = len(entities.keys())

    # compute confidences using jank formula
    if 'intent' in entities.keys():
        intent_conf = entities['intent'][0]['confidence']
        inverse_intent_conf = 1-intent_conf
    else:
        intent_conf = 0
        inverse_intent_conf = 1


    for entity, arr in entities.items():
        for val in arr:
            if entity == 'intent':
                user_data.data['entities'][entity].append(val['value'])
            else:
                user_data.data['entities'][entity] = val['value']
                confidences = np.append(confidences, val['confidence']*inverse_intent_conf)

    confidence = intent_conf + sum(confidences**2)
    return {'bot' : bot, 'confidence' : confidence}

@node
def user_data(data):
    """
    single node for storing user information.
    TODO: repalce with a attribute on the Pipeline

    Parameters
    ----------
    data : dict
           user data struct
    """
    user_data.data = data


@node
def set_confidences(confidences):
    """
    Transforms a dict of bot confidences into a 1-D numpy array of confidences

    Parameters
    ----------
    confidences : dict
                  dictionary in bot:confidence format

    Returns
    -------
    : numpy array
      1-D array of confidences
    """
    bot_conf_arr = np.zeros(numbots)
    for conf in confidences:
        bot_conf_arr[bot_indices[conf['bot']]] = conf['confidence']
    return bot_conf_arr


@node
def local_search(confidences):
    """
    perform a local area search such as looking for local restaurants.

    Parameters
    ----------
    confidences : a 1-D array of confidences

    Returns
    -------
    : answer
      the reult fo the local area search

    : confidence
      the confidence the value is correct

    """
    key_bot = 'loc'
    confidence = 1
    answer = None
    try:
        NAU_CAMPUS = (35.188,-111.653)

        # get key components of the wit analysis
        params = louie.Params()
        params['noun'] = user_data.data['entities'].get('local_search_query')
        params['location'] = user_data.data.get('location')
        params['sentiemnt'] = user_data.data.get('sentiment')

        if params.get('sentiment') == 'positive':
            sort_by = 'rating'
        else:
            sort_by = 'best_match'

        ll = (0,0)
        if params.get('location') and 'campus' in params.get('location'):
            ll = NAU_CAMPUS
        else:
            ll = user_data.data['context']['location']

        result = yelpclient.search(params.get('noun'), location='Flagstaff, AZ', ll=ll, sort_by=sort_by)
        name = result['businesses'][0]['name']
        location = result['businesses'][0]['location']['address1']

        answer = '{} @ {}'.format(name, location)
    except Exception as e:
        print(e)
        print(traceback.print_exc())

    if not answer:
        confidence = 0

    confidence = confidences[bot_indices[key_bot]]*confidence
    return answer, confidence


@node
def wolfram_search(confidences):
    """
    perform a factual search such as asking when someone was born.

    Parameters
    ----------
    confidences : a 1-D array of confidences

    Returns
    -------
    : answer
      the reult fo the fact search

    : confidence
      the confidence the value is correct

    """
    key_bot = 'fact'
    confidence = 1
    answer = None
    try:
        query_result = wolfclient.query(str(user_data.data['text']))
        print(user_data.data['text'])

        if 'personq' in user_data.data['entities']['intent']:
            for pod in query_result.pods:
                if pod['@title'] == 'Notable facts':
                    answer = pod['subpod']['plaintext'].split('\n')[0]
        else:
            # Wolfram's way of getting the 'best' result
            answer = next(query_result.results).text

    except Exception as e:
        print(e)
        print(traceback.print_exc())

    if not answer:
        confidence = 0
    confidence = confidences[bot_indices[key_bot]]*confidence
    return answer, confidence


# Puts all the API's together and gets the best answer based on confidence
@node
def converge_api_answers(results):
    """
    conerges all the answers returned by the api calls and returns the best answer based on
    confidences.

    Parameters
    ----------
    results : iterable of answers and their confidences

    Returns
    -------
    : the optimal answer from the iterable

    """

    print(results)
    best_answer = sorted(results, key=lambda x:x[1], reverse=True)[0][0]

    if not best_answer:
        best_answer = 'no answer'
    return best_answer

# Intializes the Pipline() class
louie_query = Pipeline()

# Adds all the nodes to calculate the proper weights i.e. confidence
louie_query.add_node(start)
louie_query.add_node(run_event)
louie_query.add_node(run_converse)
louie_query.add_node(run_fact)
louie_query.add_node(run_loc)
louie_query.add_node(get_confidences_from_entities, name="event_converge")
louie_query.add_node(get_confidences_from_entities, name="converse_converge")
louie_query.add_node(get_confidences_from_entities, name="fact_converge")
louie_query.add_node(get_confidences_from_entities, name="loc_converge")
louie_query.add_node(set_confidences, name='converge_confidences')
louie_query.add_node(local_search)
louie_query.add_node(wolfram_search)
louie_query.add_node(converge_api_answers)

# Connects start to each API node
louie_query.add_edge('start', 'run_event')
louie_query.add_edge('start', 'run_loc')
louie_query.add_edge('start', 'run_converse')
louie_query.add_edge('start', 'run_fact')

# Connects each API node to the converge functions
louie_query.add_edge('run_event', 'event_converge')
louie_query.add_edge('run_loc', 'loc_converge')
louie_query.add_edge('run_converse', 'converse_converge')
louie_query.add_edge('run_fact', 'fact_converge')

# Connects each function to confidence function
louie_query.add_edge('event_converge', 'converge_confidences')
louie_query.add_edge('loc_converge', 'converge_confidences')
louie_query.add_edge('converse_converge', 'converge_confidences')
louie_query.add_edge('fact_converge', 'converge_confidences')

# Directs the API calls to the proper search i.e. local or Wikipedia
louie_query.add_edge('converge_confidences', 'wolfram_search')
louie_query.add_edge('converge_confidences', 'local_search')

# Pipes the confidences into the API function to achieve the best asnswer
louie_query.add_edge('wolfram_search', 'converge_api_answers')
louie_query.add_edge('local_search', 'converge_api_answers')

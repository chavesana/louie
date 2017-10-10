from wit import Wit
import wolframalpha as wolf

import louie
from louie.yelpfusion import YelpFusion
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory

# __all__ = ['wolfram_search', 'witclient', 'wolfclient', 'yelpclient', 'FB_PAGE_TOKEN']

WIT_TOKEN = 'PEV2QBTAEKH6YIZM6JETQAOBBJIUMTDT'

FB_PAGE_TOKEN = 'EAAVWYdbX2BUBAJZBmlbIeZCoocO5CdRHY82VNs8drNbB0yNL5bj63K0ZCQqIqzAbrl0u2ollXrsFIiRMfebWAQmpF1sw2EsThg1TpDulsygqGkQQ7dcHZCZB6W6QGlejXKYEg0ObqZAOTXGqKe9exLf57ZCQW546Kh5W66lEOvaGjX3ffruHXXT'
FB_VERIFY_TOKEN = 'hello'
WOLFRAM_TOKEN = '64J9LH-5Q8357GKRK'
GOOGS_PLACES_TOKEN = 'AIzaSyABRaPH0tzxRT_sVBkkGr5zWkbN3y7jN9Q'
YELP_APP_ID = 'xqTzjWmr8PIUqv9gkQLWBw'
YELP_CLIENT_SECRET = '4YtXv1OVhISGWM4Eb1ji7YJc0igSEAOkvXXyiH3KA0tNKZmGhUoh9M2VAlexfIST'

witclient = Wit(access_token=WIT_TOKEN)
wolfclient = wolf.Client(WOLFRAM_TOKEN)
yelpclient = YelpFusion(YELP_APP_ID, YELP_CLIENT_SECRET)

context = {}
pronouns = ["he", "she", "it", "him", "her", "its", "his", "hers", "its", "them", "they", "their", "theirs"]


def wolfram_search(wit_response):
    letters = set('abcdefghijklmnopqrstuvwxy ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    simple_value = wit_response['entities']['wikipedia_search_query'][0]['value']
    simple_question = wit_response['_text']

    query_result = wolfclient.query(str(simple_question))
    sub_pod_num = 0
    word_place = 0
    simple_question = ''.join(filter(letters.__contains__, simple_question))
    sentence = simple_question.split()

    if(context):
        for pronoun in pronouns:
            for word in sentence:
                if(pronoun == word):
                    sentence[word_place] = context['subject']
                    sentence = ' '.join(sentence)
                    return next(wolfclient.query(str(sentence)).results).text
                word_place += 1

    elif(query_result['@success'] == 'false'):
        return 'We did not find an answer for your question.'

    elif(not list(query_result.results)):
        message_subject = str(wit_response['entities']['wikipedia_search_query'][0]['value'])
        context['subject'] = message_subject
        return "What exactly do you want to know about " + message_subject + "?"

    elif(list(query_result.results)):
         return next(query_result.results).text

    else:
        print("I could not complete the search, is there another question you would like to ask?")

def yelp_search(*args, **kwargs):
    result = yelpclientself.search(*args, **kwargs)
    top_option = result
    pass

def process_nlp(wit_response):
    intents = wit_response['entities'].keys()

    if 'wikipedia_search_query' in intents:
        print('[PERFORMING WOLFRAM QUERY]')
        res = louie.wolfram_search(wit_response)
        return res

def interactive(witclient, bot_name = 'Louie'):
    # input/raw_input are not interchangeable between Python 2 and 3
    try:
        input_function = raw_input
    except NameError:
        input_function = input

    history = InMemoryHistory()
    while True:
        try:
            message = prompt('You >> ', history=history, mouse_support=True).rstrip()
        except (KeyboardInterrupt, EOFError):
            return

        wit_response = witclient.message(message, {})
        print(wit_response)
        print()
        print('{} >> '.format(bot_name), process_nlp(wit_response))

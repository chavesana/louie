from wit import Wit
import wolframalpha as wolf

import louie
from louie.yelpfusion import YelpFusion
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory

# __all__ = ['wolfram_search', 'witclient', 'wolfclient', 'yelpclient', 'FB_PAGE_TOKEN']

WIT_TOKEN = 'FCLEILUP6T2PTIH6TSWWJYFJYKG3KL2L'

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
pronouns = ['he', 'she', 'it', 'him', 'her', 'it', 'his', 'hers', 'its', 'them', 'they', 'their', 'theirs']


def wolfram_search(wit_response):
    simple_question = wit_response['entities']['wikipedia_search_query'][0]['value']
    query_result = wolfclient.query(str(simple_question))
    sub_pod_num = 0

    if(context):
        for pronoun in pronouns:
            if(pronoun in simple_question):
                simple_question.replace(pronoun, context['subject'])
                wolfram_search(simple_question)
                break

    elif(query_result['@success'] == 'false'):
        return 'We did not find an answer for your question.'

    elif(not list(query_result.results)):
        message_subject = str(wit_response['entities']['wikipedia_search_query'][0]['value'])
        context['subject'] = message_subject
        print(context['subject'])
        return "What exactly do you want to know about " + message_subject + "?"

    elif(list(query_result.results)):
         print(next(query_result.results).text)

    else:
        for pod in query_result.pods:
            for sub in pod.subpods:
                sub_pod_num += 1
                if(sub_pod_num == 6):
                    return sub['img']['@title']

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

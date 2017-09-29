from louie import wolfclient

def wolfram_search(simple_question):
    query_result = wolfclient.query(str(simple_question))
    i = 0

    if(query_result['@success'] == 'false'):
        return 'We did not find an answer for your question.'

    elif(not query_result.results):
        print('I did not find a straight forward answers, here is what I found: \n')
        for pod in query_result.pods:
            for sub in pod.subpods:
                i += 1
                if(i == 6):
                    return sub['img']['@title']
    else:
        return next(query_result.results).text

def places_search(text):
    pass

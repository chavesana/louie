from louie import wolfclient

def wolfram_search(simple_question):
    print('performing wolfram search-------------')
    query_result = wolfclient.query(str(simple_question))
    i = 0

    if(query_result['@success'] == 'false'):
        print('We did not find an answer for your question.')

    elif(query_result.results):
        print('I did not find a straight forward answers, here is what I found: \n')
        for pod in query_result.pods:
            for sub in pod.subpods:
                i += 1
                if(i == 6):
                    print(sub['img']['@title'], i)
                    break
    else:
        print(next(query_result.results).text)

from louie import wolfclient

def wolfram_search(simple_question):
    query_result = wolfclient.query(str(simple_question))
    sub_pod_num = 0

    if(query_result['@success'] == 'false'):
        return 'We did not find an answer for your question.'

    elif(list(query_result.results)):
         return next(query_result.results).text

    else:
        for pod in query_result.pods:
            for sub in pod.subpods:
                sub_pod_num += 1
                if(sub_pod_num == 6):
                    return sub['img']['@title']
                
def places_search(text):
    pass

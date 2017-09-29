from louie import wolfclient

def wolfram_query(string):
    """
    """
    query_result = wolfclient.query(string)
    return next(query_result.results).text

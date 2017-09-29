from louie import wolfclient

def wolfram_query(string):
    """
    """
    query_result = wolfclient.query()
    fb_message(fb_id, next(query_result.results).text)

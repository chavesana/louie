import argparse
import json
import pprint
import requests
import sys
import urllib

from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode

from enum import Enum
from collections import namedtuple

__all__ = ["YelpFusion", "sort", "Params"]

API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'

class Params(dict):
    """
    Subclassed dictionary that does not add values which evaluate to false. Eliminates the need
    of if/else statements all over the place for api calls with a lot of optional config
    options.
    """
    def __init__(self, *args, **kwargs):
        """
        Extend dict init to allow keys to be accessed as attributes
        """
        super(Params, self).__init__(*args, **kwargs)
        self.__dict__ = self

    def __setitem__(self, key, value):
        """
        Extend dict's __setitem__ to reject any new values which evaluate to false (e.g. empty
        sets, empty string, empty lists, None, etc.).
        """
        if key in self or value:
            dict.__setitem__(self, key, value)

sort = Params({
    'BEST_MATCH' : 'best_match',
    'RATING' : 'rating',
    'REVIEW_COUNT' : 'review_count',
    'DISTANCE' : 'distance'
})

class YelpFusion(object):

    def __init__(self, client_id, client_secret):
        self._client_id = client_id
        self._client_secret = client_secret

        # Obtain bearer token
        url = '{0}{1}'.format(API_HOST, quote(TOKEN_PATH.encode('utf8')))
        data = urlencode({
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'grant_type': GRANT_TYPE,
        })

        headers = {
            'content-type': 'application/x-www-form-urlencoded',
        }

        response = requests.request('POST', url, data=data, headers=headers)
        self._bearer_token = response.json()['access_token']


    def request(self, host, path, url_params=None):
        """Given a bearer token, send a GET request to the API.
        Args:
            host (str): The domain host of the API.
            path (str): The path of the API after the domain.
            bearer_token (str): OAuth bearer token, obtained using client_id and client_secret.
            url_params (dict): An optional set of query parameters in the request.
        Returns:
            dict: The JSON response from the request.
        Raises:
            HTTPError: An error occurs from the HTTP request.
        """
        url_params = url_params or {}
        url = '{0}{1}'.format(host, quote(path.encode('utf8')))
        headers = {
            'Authorization': 'Bearer %s' % self._bearer_token,
        }

        response = requests.request('GET', url, headers=headers, params=url_params)
        return response.json()


    def search(self, term, location='', ll=(0,0), limit=10, price=None, open_now=False,
               sort_by=sort.BEST_MATCH, radius=9000, locale=None, offset=0):
        """
        Query the Search API by a search term and location.

        Parameters
        ----------

        term : string
               The search term passed to the API.

        location : string
                   The plain text search location passed to the API. e.g. Flagstaff, AZ or an home address/
                   Must be provided if ll is not provided.

        ll : tuple
             Tuple of floats in the format (latitude, longitude), location used as the center of the
             search. If both ll and location are provided, ll takes precedence and location will
             be ignored by the specification of the Yelp API.

        sort_by : string
                  Sort the results by one of the these modes: best_match, rating, review_count
                  or distance. By default it's BEST_MATCH.
        Returns
        -------
        dict: The JSON response from the request.

        See Also
        --------
        Search Docs : https://www.yelp.com/developers/documentation/v3/business_search

        """
        url_params = Params()
        url_params['location'] = location
        url_params['latitude'] = ll[0]
        url_params['longitude'] = ll[1]
        url_params['term'] = term.replace(' ', '+'),
        url_params['limit'] = min(limit, 50)
        url_params['price'] = price
        url_params['open_now'] = open_now
        url_params['sort_by'] = sort_by
        url_params['radius'] = radius
        url_params['locale'] = locale

        return self.request(API_HOST, SEARCH_PATH, url_params=url_params)


    def get_details(self, business_id):
        """Query the Business API by a business ID.
        Args:
            business_id (str): The ID of the business to query.
        Returns:
            dict: The JSON response from the request.
        """
        business_path = BUSINESS_PATH + business_id
        return self.request(API_HOST, business_path)


    def get(self, term, location):
        """
        Queries the API by the input values from the user and only return the top result.
        Args:
            term (str): The search term to query.
            location (str): The location of the business to query.
        """
        response = self.search(term, location=location)
        businesses = response.get('businesses')
        return businesses
